


## 1. Create an API Context class

```python
class DogsApiContext(RestApiContext):
    def __init__(self):
        super().__init__(
            # auth=None,
            # base_serializer=None,
            # rate_limiter=None,
            # logger=None,
            # http_handler=None
        )
```

The power of the framework stems from this class. You can provide multiple functionalities 
simply by creating classes inheriting from classes provided.


## Authenticators
By default, when no authenticator object is provided, the framework will instantiate a 
NoAuth class. Multiple authenticator options are proposed:

### HttpHeaderAuth
Create a class inheriting from the HttpHeaderAuth class and fill the get_api_key method:
```python
class DogsApiHttpHeaderAuth(HttpHeaderAuth):
    def get_api_key(self) -> str:
        # enter logic to get the key and return it
```

### UrlTokenAuth
Create a class inheriting from the UrlTokenAuth class and fill the get_token and get_new_token methods:

```python
class DogsApiHttpHeaderAuth(UrlTokenAuth):
    def get_token(self) -> str:
        # enter logic to get the token and return it

    def get_new_token(self) -> str:
        # enter logic to renew the token and return it
```

### BearerTokenAuth
Similarly to the UrlTokenAuth, create a class inheriting from the UrlTokenAuth class and fill the
get_token and get_new_token methods:

```python
class DogsApiHttpHeaderAuth(BearerTokenAuth):
    def get_token(self) -> str:
        # enter logic to get the token and return it

    def get_new_token(self) -> str:
        # enter logic to renew the token and return it
```


## Base serializers
The serializers are used to transform Python objects to other object formats and back to
Python objects. The base serializer is used as default when no other serializers are defined
for a specific entity. 

### TextSerializer
This is the most basic serializer, it just transmits text and receives text.

### JsonSerializer
It transforms from and to JSON format.
```python
class DogsApiContext(RestApiContext):
    def __init__(self):
        super().__init__(
            base_serializer=JsonSerializer(),
        )
```
### XmlSerializer
It transforms from and to XML format.
```python
class DogsApiContext(RestApiContext):
    def __init__(self):
        super().__init__(
            base_serializer=XmlSerializer(),
        )
```

## Rate limiters
The rate limiters are used to guarantee that the rate limit of the API is respected.

### Uniform rate limiter
The uniform rate limiter will make sure the requests are evenly spread out through time to respect the rate limit. It'll
use a busy wait between each request based on its configuration.
```python
class DogsApiContext(RestApiContext):
    def __init__(self):
        super().__init__(
            rate_limiter=uniform_rate_limiter(2, 3),
        )

```

### Burst rate limiter
The brust rate limiter will make all the allowed requests with no control until it meets the limit. It'll then use a
busy wait until allowed more requests.
```python
class DogsApiContext(RestApiContext):
    def __init__(self):
        super().__init__(
            rate_limiter=burst_rate_limiter(2, 3),
        )
```


## Loggers
The loggers are used to log important steps throughout the utilization of the API. They can be instantiated outside of the 
constructor of the Api Context and used throughout the rest of the application as well.

### ConsoleLogger
```python
logger: Logger = ConsoleLogger()

class DogsApiContext(RestApiContext):
    def __init__(self, logger: Logger):
        super().__init__(
            logger=logger
        )

api = DogsApiContext(logger)
```

### AdlsTableLogger (To Be Implemented)
...

### InMemoryLogger (To Be Implemented)
...

### RestEndpointLogger (To Be Implemented)
...



## Http handlers
The Http handlers are a very easy way to deal with Http errors without having to know the 
technicalities of how the request works.

To use this, you simply need to create a class and make it inherit from the class HttpResponseHandler.
This will allow you to overload any of the Http responses and let you do many things, like retry the 
request, change the headers, change the url, log the error, etc.

Here is a quick example:
```python
class DogsApiHttpResponseHandler(HttpResponseHandler):
    def on_unauthorized(
        self,
        request: RequestConfig,
        response: Response,
        request_method: Callable[[RequestConfig], Response]
    ):
        self.logger.log(f"[401]: Renewing token...")
        self.auth.renew_auth()
        self.logger.log(f"[401]: Token Renewed.")
        self.logger.log(f"Retrying query...")
        new_response = request_method(request)
        new_response.raise_for_status()
        return new_response
```

Here we are overloading the method on_unauthorized (error 401) in order to renew the token 
and retry the request after.


## Here is a full example of an API that has been implemented with this framework:

```python
import os

from ventriloctoolkit.apiwrappers.authenticator import HttpHeaderAuth, UrlTokenAuth, BearerTokenAuth
from ventriloctoolkit.decorators.ratelimiters import burst_rate_limiter
from ventriloctoolkit.utils.loggers import ConsoleLogger
from ventriloctoolkit.apiwrappers.restapiwrappers import RestApiContext, RestApiClient, ReadMixin, ListEntity,


@with_route


from src.puppet.apiwrappers.serializers import JsonSerializer


class DogsApiHttpHeaderAuth(HttpHeaderAuth):
    def __init__(self):
        super().__init__("X-Api-Key")

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
    pass


class DogsApiWrapper(RestApiClient):
    def __init__(self):
        super().__init__(
            base_url="https://api.api-ninjas.com/v1",
            api_context=DogsApiContext()
        )

        self.dogs: DogsEndpoint = DogsEndpoint(self._api_context, self._base_url)


api = DogsApiWrapper()
response = api.dogs.get_all({"name": "Golden Retriever"})
print(response)
```