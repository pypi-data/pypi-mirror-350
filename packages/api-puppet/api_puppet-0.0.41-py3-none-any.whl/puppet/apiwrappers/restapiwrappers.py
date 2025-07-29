from abc import abstractmethod, ABC
from typing import Optional, Union, Callable, Generator, List, Dict, Type, TypeVar, Generic
from urllib.parse import quote_plus
from requests import request, Response

from .httpresponsehandler import HttpResponseHandler
from .authenticator import NoAuth, Authenticator
from .dto import RequestConfig
from ..utils.loggers import Logger, NoLogger
from .serializers import Serializer, JsonSerializer


T = TypeVar('T')


def with_route(route_suffix: str) -> Type:
    def decorator(cls: Type) -> Type:
        original_init = cls.__init__

        def __init__(self, api_context: RestApiContext, base_url: str,  **kwargs):
            adapted_base_url = f"{base_url}/{route_suffix}"
            original_init(self, api_context, adapted_base_url, **kwargs)
        cls.__init__ = __init__
        return cls
    return decorator


def with_id_route() -> Type:
    def decorator(cls: Type) -> Type:
        original_init = cls.__init__

        def __init__(self, api_context: RestApiContext, base_url: str,  **kwargs):
            adapted_base_url = f"{base_url}/{kwargs.get('id')}"
            original_init(self, api_context, adapted_base_url, **kwargs)
        cls.__init__ = __init__
        return cls
    return decorator


# Define the decorator
def with_http_response_handler(http_handler: HttpResponseHandler) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Union[str, dict]:
            # Call the original _make_request method
            response = func(*args, **kwargs)
            handler_response = http_handler.handle_request(args[0], response, func)
            return handler_response

        return wrapper

    return decorator


class RestApiContext:
    def __init__(self, authenticator=None, base_serializer: Serializer = None, rate_limiter=None, logger: Logger = None, http_handler: HttpResponseHandler = None):
        self._authenticator: Authenticator = authenticator or NoAuth()
        self._logger: Logger = logger or NoLogger()
        self._http_handler: HttpResponseHandler = http_handler or HttpResponseHandler()
        self._base_serializer: Serializer = base_serializer or JsonSerializer()

        self._rate_limiter = rate_limiter
        self._http_handler.initialize(self._authenticator, self._logger)
        self._make_request: Callable[[RequestConfig], Response] = self._make_request

    def initialize(self) -> None:
        self._logger.log("Starting API context initialization...")
        self._authenticator.initialize()
        self._logger.log("Initialized API context successfully.")

        if self._http_handler:
            self._http_handler.initialize(self._authenticator, self._logger)
            self._make_request = with_http_response_handler(self._http_handler)(self._make_request)

        self._make_request: Callable[[RequestConfig], Union[str, dict]] = self._rate_limiter(self._make_request) if self._rate_limiter else self._make_request

    def get(self, url: str, query_params: Optional[Dict[str, any]] = None, serializer: Serializer = None, request_args: dict = None):
        request_config = RequestConfig(
            http_verb="GET",
            url=url,
            query_params=query_params,
        )

        response = self._process_request(request_config, serializer=serializer, request_args=request_args)

        return response

    def post(self, url: str, body: dict, serializer: Serializer = None, request_args: dict = None):
        request_config = RequestConfig(
            http_verb="POST",
            url=url,
            body=body
        )

        response = self._process_request(request_config, serializer=serializer, request_args=request_args)

        return response

    def patch(self, url: str, body: dict, serializer: Serializer = None, request_args: dict = None):
        request_config = RequestConfig(
            http_verb="PATCH",
            url=url,
            body=body
        )

        response = self._process_request(request_config, serializer=serializer, request_args=request_args)

        return response

    def put(self, url: str, body: dict, serializer: Serializer = None, request_args: dict = None):
        request_config = RequestConfig(
            http_verb="PUT",
            url=url,
            body=body
        )

        response = self._process_request(request_config, serializer=serializer, request_args=request_args)

        return response

    def delete(self, url: str, body: dict = None, serializer: Serializer = None, request_args: dict = None):
        request_config = RequestConfig(
            http_verb="DELETE",
            url=url,
            body=body
        )

        response = self._process_request(request_config, serializer=serializer, request_args=request_args)

        return response

    def prepare_request(self, request_config: RequestConfig) -> RequestConfig:
        """
        This method can be overriden to modify the request config before the processing of said request config
        """
        return request_config

    def _process_request(self, request_config: RequestConfig, serializer: Serializer = None, request_args: dict = None):
        serializer = serializer or self._base_serializer
        request_config = self.prepare_request(request_config)
        # prepare auth
        request_config = self._authenticator.apply_auth_to_request(request_config)

        # prepare url
        url = (
            f"{request_config.url}?{'&'.join([f'{k}={quote_plus(str(v))}' for k,v in request_config.query_params.items()])}"
            if request_config.query_params
            else request_config.url
        )
        request_config.url = url
        request_config.headers.update({"Content-Type": serializer.get_content_type()})
        # serialize request body
        if request_config.body:
            serialized_body = serializer.serialize(request_config.body)
            request_config.body = serialized_body

        # make request
        response = self._make_request(request_config, request_args)

        # deserialize response
        deserialized_response = serializer.deserialize(response)
        # return response
        return deserialized_response

    def _make_request(self, request_config: RequestConfig, request_args: dict = None) -> Response:
        request_args = request_args or {}
        self._logger.log(f"{request_config.http_verb} {request_config.url}")
        response: Response = request(
            request_config.http_verb,
            request_config.url,
            headers=request_config.headers,
            data=request_config.body or {},
            **request_args
        )

        return response


class RestApiClient(ABC):
    def __init__(self, base_url: str, api_context: RestApiContext):
        self._base_url: str = base_url
        self._api_context: RestApiContext = api_context
        self._api_context.initialize()


class UrlRoute:
    def __init__(self, api_context, base_url, **kwargs):
        self._base_url = base_url
        self._api_context: RestApiContext = api_context

    def get_uri(self) -> str:
        return self._base_url


# Create a generic base class
UrlRouteType = TypeVar('UrlRouteType', bound=UrlRoute)


class WithIdRoute(Generic[UrlRouteType], UrlRoute):
    __entity_class__: Type[UrlRouteType] = None

    def __init__(self, api_context, base_url, **kwargs):
        if self.__entity_class__ is None:
            raise NotImplementedError(
                "The class attribute __entity_class__ has to be implemented in all classes "
                "inheriting from WithIdRoute class."
            )

        super().__init__(api_context, base_url, **kwargs)

    def by_id(self, id: str) -> UrlRouteType:
        return self.__entity_class__(self._api_context, self._base_url, id=id)


class ListEntity(UrlRoute):
    def list(self, query_params: dict = None):
        return self._api_context.get(self._base_url, query_params=query_params)


class CreateMixin(UrlRoute):
    def post(self, body: dict):
        return self._api_context.post(self._base_url, body)


class ReadMixin(UrlRoute):
    def get(self, query_params: dict = None):
        return self._api_context.get(self._base_url, query_params=query_params)


class UpdateMixin(UrlRoute):
    def patch(self, body: dict):
        return self._api_context.patch(self._base_url, body)

    def put(self, body: dict):
        return self._api_context.put(self._base_url, body)


class DeleteMixin(UrlRoute):
    def delete(self, body: dict = None):
        return self._api_context.delete(self._base_url, body=body)


class PaginatedListEntity(ListEntity, ABC):
    __serializer__: Serializer = None

    def __init__(self, api_context, base_url):
        self._base_url = base_url
        super().__init__(api_context, self._base_url)
        self._api_context: RestApiContext = api_context

    def list(
        self,
        query_params: Dict[str, any] = None,
        start_page: int = 1,
        end_page: Optional[int] = None,
        page_no_attribute_name: str = "page",
        process_response_before_returning: bool = True
    ) -> Generator[List[Dict], None, None]:
        """
        Get all pages from a REST API with pagination.

        :param query_params: Additional query parameters
        :param start_page: Optional starting page (1-based index)
        :param end_page: Optional ending page (1-based index)
        :param page_no_attribute_name: query params key value for page number
        :return: Generator that yields lists of items from each page
        """
        query_params = query_params or {}
        current_page = start_page
        while True:
            query_params[page_no_attribute_name] = current_page
            response = self._get_next(query_params=query_params)

            response_to_yield = self.response_processor(response) if process_response_before_returning else response

            yield response_to_yield

            if not self._has_next(response, current_page, end_page):
                break

            current_page += 1

    @abstractmethod
    def _has_next(self, response: dict, current_page: int, end_page: Optional[int] = None) -> bool:
        raise NotImplementedError()

    def _get_next(self, query_params: Dict[str, any] = None):
        return self._api_context.get(self._base_url, query_params=query_params, serializer=self.__serializer__)

    def response_processor(self, response):
        return response


class CursorPaginatedListEntity(ListEntity, ABC):
    def __init__(self, api_context, base_url):
        self._base_url = base_url
        super().__init__(api_context, self._base_url)
        self._api_context: RestApiContext = api_context
        self._number_of_pages_read: int = 0

    def list(
            self,
            query_params: Dict[str, any] = None,
            max_number_of_pages: Optional[int] = None,
            process_response_before_returning: bool = True
    ) -> Generator[List[Dict], None, None]:

        query_params = query_params or {}

        current_response = self._get_first(query_params)
        self._number_of_pages_read += 1
        response_to_yield = self.response_processor(current_response) if process_response_before_returning else current_response

        yield response_to_yield

        while True:
            if max_number_of_pages is not None and self._number_of_pages_read >= max_number_of_pages:
                break

            has_next = self._has_next(current_response)
            if not has_next:
                break

            next_page_uri = self._get_next_page_uri(current_response)
            current_response = self._api_context.get(next_page_uri)
            self._number_of_pages_read += 1
            response_to_yield = self.response_processor(current_response) if process_response_before_returning else current_response

            yield response_to_yield

        self._number_of_pages_read = 0

    @abstractmethod
    def _get_first(self, query_params: Dict[str, any] = None):
        raise NotImplementedError()

    @abstractmethod
    def _has_next(self, response: dict) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def _get_next_page_uri(self, response: dict) -> str:
        raise NotImplementedError()

    def response_processor(self, response):
        return response
