import os

from ..apiwrappers.authenticator import HttpHeaderAuth
from ..decorators.ratelimiters import burst_rate_limiter
from ..utils.loggers import ConsoleLogger
from ..apiwrappers.restapiwrappers import RestApiContext, RestApiClient, ListEntity, with_route, \
    UrlRoute
from ..apiwrappers.serializers import JsonSerializer


class DogsApiHttpHeaderAuth(HttpHeaderAuth):
    def get_header_key_name(self) -> str:
        return "X-Api-Key"

    def get_api_key(self) -> str:
        return os.environ.get("DOGS_API_KEY")


class DogsApiContext(RestApiContext):
    def __init__(self):
        super().__init__(
            authenticator=DogsApiHttpHeaderAuth(),
            base_serializer=JsonSerializer(),
            rate_limiter=burst_rate_limiter(2, 2),
            logger=ConsoleLogger(),
            http_handler=None
        )


@with_route("dogs")
class DogsEndpoint(ListEntity):
    def __init__(self, api_context, base_url):
        super().__init__(api_context, base_url)


@with_route("v1")
class v1Endpoint(UrlRoute):
    def __init__(self, api_context, base_url, **kwargs):
        super().__init__(api_context, base_url, **kwargs)
        self.dogs: DogsEndpoint = DogsEndpoint(api_context, base_url)


class DogsApiWrapper(RestApiClient):
    def __init__(self):
        super().__init__(
            base_url="https://api.api-ninjas.com",
            api_context=DogsApiContext()
        )

        self.v1: v1Endpoint = v1Endpoint(self._api_context, self._base_url)


api = DogsApiWrapper()
response = api.v1.dogs.list({"name": "Golden"})
print(response)