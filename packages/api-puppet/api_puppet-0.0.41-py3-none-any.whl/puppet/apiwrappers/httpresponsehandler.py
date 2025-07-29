from typing import Callable
from urllib.parse import quote_plus
from requests import Response

from .authenticator import Authenticator, NoAuth
from .dto import RequestConfig
from ..utils.loggers import Logger, NoLogger


class HttpInformationalResponses:
    def get_mappings(self):
        return {
            100: self.on_continue,
            101: self.on_switching_protocols,
            102: self.on_processing,
            103: self.on_early_hints,
        }

    def on_continue(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_switching_protocols(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_processing(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_early_hints(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_informational_response_default(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response


class HttpSuccessfulResponses:
    def get_mappings(self):
        return {
            200: self.on_ok,
            201: self.on_created,
            202: self.on_accepted,
            204: self.on_no_content,
            205: self.on_reset_content,
            206: self.on_partial_content,
            207: self.on_multi_status,
            208: self.on_already_reported,
            226: self.on_im_used,
        }

    def on_ok(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_created(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_accepted(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_no_content(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_reset_content(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_partial_content(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_multi_status(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_already_reported(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_im_used(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_successfull_response_default(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response


class HttpRedirectionMessages:

    def get_mappings(self):
        return {
            300: self.on_multiple_choices,
            301: self.on_moved_permanently,
            302: self.on_found,
            303: self.on_see_other,
            304: self.on_not_modified,
            305: self.on_use_proxy,
            306: self.on_unused,
            307: self.on_temporary_redirect,
            308: self.on_permanent_redirect,
        }

    def on_multiple_choices(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_moved_permanently(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_found(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_see_other(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_not_modified(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_use_proxy(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_unused(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_temporary_redirect(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_permanent_redirect(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_redirection_message_default(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response


class HttpClientError:
    def get_mappings(self):
        return {
            400: self.on_bad_request,
            401: self.on_unauthorized,
            402: self.on_payment_required,
            403: self.on_forbidden,
            404: self.on_not_found,
            405: self.on_method_not_allowed,
            406: self.on_not_acceptable,
            407: self.on_proxy_authentication_required,
            408: self.on_request_timeout,
            409: self.on_conflict,
            410: self.on_gone,
            411: self.on_length_required,
            412: self.on_precondition_failed,
            413: self.on_payload_too_large,
            414: self.on_uri_too_long,
            415: self.on_unsupported_media_type,
            416: self.on_range_not_satisfiable,
            417: self.on_expectation_failed,
            418: self.on_im_a_teapot,
            421: self.on_misdirected_request,
            422: self.on_unprocessable_content,
            423: self.on_locked,
            424: self.on_failed_dependency,
            425: self.on_too_early,
            426: self.on_upgrade_required,
            428: self.on_precondition_required,
            429: self.on_too_many_request,
            431: self.on_request_header_fields_too_large,
            451: self.on_unavailable_for_legal_reasons
        }

    def on_bad_request(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_unauthorized(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_payment_required(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_forbidden(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_not_found(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_method_not_allowed(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_not_acceptable(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_proxy_authentication_required(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_request_timeout(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_conflict(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_gone(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_length_required(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_precondition_failed(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_payload_too_large(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_uri_too_long(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_unsupported_media_type(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_range_not_satisfiable(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_expectation_failed(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_im_a_teapot(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_misdirected_request(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_unprocessable_content(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_locked(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_failed_dependency(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_too_early(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_upgrade_required(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_precondition_required(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_too_many_request(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_request_header_fields_too_large(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_unavailable_for_legal_reasons(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response

    def on_client_error_default(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        raise response.raise_for_status()


class HttpServerError:
    def get_mappings(self):
        return {
            500: self.on_internal_server_error,
            501: self.on_not_implemented,
            502: self.on_bad_gateway,
            503: self.on_service_unavailable,
            504: self.on_gateway_timeout,
            505: self.on_http_version_not_supported,
            506: self.on_variant_also_negotiates,
            507: self.on_insufficient_storage,
            508: self.on_loop_detected,
            510: self.on_not_extended,
            511: self.on_network_authentication_required,
        }

    def on_internal_server_error(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response
    def on_not_implemented(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response
    def on_bad_gateway(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response
    def on_service_unavailable(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response
    def on_gateway_timeout(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response
    def on_http_version_not_supported(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response
    def on_variant_also_negotiates(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response
    def on_insufficient_storage(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response
    def on_loop_detected(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response
    def on_not_extended(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response
    def on_network_authentication_required(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        return response
    def on_server_error_default(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        raise response.raise_for_status()


class HttpResponseHandler(HttpInformationalResponses, HttpSuccessfulResponses, HttpRedirectionMessages, HttpClientError, HttpServerError):
    def __init__(self):
        super(HttpInformationalResponses, self).__init__()
        super(HttpSuccessfulResponses, self).__init__()
        super(HttpRedirectionMessages, self).__init__()
        super(HttpClientError, self).__init__()
        super(HttpServerError, self).__init__()

        self._logger: Logger = None
        self._auth: Authenticator = None

    @property
    def logger(self):
        if self._logger is None:
            raise AttributeError("Attribute logger has not been assigned. Call method initialize with a Logger object before calling this method.")

        return self._logger

    @property
    def auth(self):
        if self._auth is None:
            raise AttributeError("Attribute auth has not been assigned. Call method initialize with a Logger object before calling this method.")

        return self._auth

    def initialize(self, auth: Authenticator = None, logger: Logger = None):
        self._logger: Logger = logger or NoLogger()
        self._auth: Authenticator = auth or NoAuth()

    def handle_request(self, request_config: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
        all_handlers = dict(
            HttpInformationalResponses.get_mappings(self).items()
            | HttpSuccessfulResponses.get_mappings(self).items()
            | HttpRedirectionMessages.get_mappings(self).items()
            | HttpClientError.get_mappings(self).items()
            | HttpServerError.get_mappings(self).items()
        )
        status = response.status_code
        self.logger.log(f"[{status}] {request_config.url}")
        handler = all_handlers.get(status)

        method_comes_from_base = self._find_method_origin(handler) in (
            'HttpInformationalResponses',
            'HttpSuccessfulResponses',
            'HttpRedirectionMessages',
            'HttpClientError',
            'HttpServerError',
        )

        if method_comes_from_base:
            status_category = status // 100
            status_category_default_method = {
                1: self.on_informational_response_default,
                2: self.on_successfull_response_default,
                3: self.on_redirection_message_default,
                4: self.on_client_error_default,
                5: self.on_server_error_default,
            }
            default_method = status_category_default_method.get(status_category)
            if default_method:
                return default_method(request_config, response, request_method)

        if handler:
            return handler(request_config, response, request_method)

    @staticmethod
    def _find_method_origin(method):
        func = method.__func__
        for cls in method.__self__.__class__.__mro__:
            if func.__name__ in cls.__dict__:
                return cls.__name__


# class MyHandler(HttpResponseHandler):
#     def __init__(self, auth: Auth = None, logger: Logger = None):
#         super().__init__(auth=auth, logger=logger)
#
#     def on_too_many_request(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
#         print("this is how i manage this shit")
#
#         time.sleep(5)
#         return request_method(request)
#
#     def on_unauthorized(self, request: RequestConfig, response: Response, request_method: Callable[[RequestConfig], Response]):
#         print("here i renew my token")
#         """
#         for this i need my auth object
#         """
#         self.auth.renew_auth()


# r = R()
# r.status_code = 401
#
# handler = MyHandler()
# handler.handle_request(None, r)
