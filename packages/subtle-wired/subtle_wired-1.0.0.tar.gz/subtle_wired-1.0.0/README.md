<div align="left">
  <a href="https://pypi.org/project/subtle-wired/">
    <img src="https://img.shields.io/pypi/v/subtle-wired.svg" alt="PyPi Latest Release"/>
  </a>
</div>

# subtle-wired

A simple reflection-based dependency injector. The name `subtle-wired` comes from the goal of making these connections between dependencies something subtle, light, and straightforward.

- Lazy | eager execution
- Thread-safe
- Simple to use
- Force to respect the Dependency Inversion Principle
- Python 3

## Usage example

### 1. Classes to be inserted into the container:

Every class needs to have an interface to be injected (which will ensure that the dependency inversion principle is followed):

```python
from abc import ABC
from dataclasses import dataclass
from typing import Any


@dataclass
class User:
    id: str
    name: str


class IConfig(ABC):
    def user_endpoint(self) -> str:
        pass

    def base_url(self) -> str:
        pass


class IHttpService(ABC):
    def get(self, endpoint: str, parameters: dict[str, str]) -> dict[str, Any]:
        pass


class IUserRepository(ABC):
    def get_user(self, user_id: str) -> User:
        pass


```

Below is a simplified implementation example for the previous interfaces:

```python
from subtle_wired.decorators import (
    singleton,
    factory,
    inject,
    inject_property
)


@singleton()
class Config(IConfig):
    def user_endpoint(self) -> str:
        return "/user"

    def base_url(self) -> str:
        return "https://www.backend.com/v1"


@factory(is_lazy=True)
class HttpService(IHttpService):
    def __init__(self, config: IConfig):
        self.__config = config

    def get(self, endpoint: str, parameters: dict[str, str]) -> dict[str, Any]:
        url = self.__config.base_url() + endpoint
        response = requests.get(url, params=parameters)
        return response.json()


@singleton()
class UserRepository(IUserRepository):
    @inject_property
    def __http_service(self) -> IHttpService: ...

    @inject
    def __init__(self, config: IConfig):
        self.__config = config

    def get_user(self, user_id: str) -> User:
        endpoint = self.__config.user_endpoint()
        result = self.__http_service.get(
            endpoint,
            {
                "user_id": user_id
            }
        )
        return User(
            id=result["id"],
            name=result["name"]
        )
```

Explanation:

- The `singleton` and `factory` decorators must be used in all classes that will be injected into the container:
  - `singleton` means that every time an instance of this class is requested, the instance created in the first request will be used;
  - `factory` means that every time an instance of this class is requested, a new instance will be created (note that this does not mean that the class is a factory, but rather that a factory within the container will generate it).
- The `inject` and `inject_property` decorators are decorators for searching for instances within the container:
  - `inject`, when applied to class constructors, searches for instances for the parameters of this constructor. It is not mandatory in class constructors that are within the container;
  - `inject` and `inject_property` can be applied to methods (other than the constructor) to search for instances of the method's return in the container (the difference is in usage; `inject` only implements the method, keeping its call as a function, while `inject_property` turns the method into a property of the class's objects).
- The `is_lazy` flag (which has the default value `False`) when it has the value `True` means that an instance of the class will only be created in the container the first time it is requested (whether by eager classes internal or external to the container).

### 2. Creating the container with the list of component classes:

Example of a container for dependency injection:

```python
from subtle_wired.core import Container


class MyContainer(Container):
    components = [
        Config,
        UserRepository,
        HttpService,
    ]
```

### 3. Container usage:

Example of how to use the created container:

```python
from subtle_wired.core import Injector


MyContainer()\
    .startup()

user_repository = Injector()\
    .get_instance(IUserRepository)

print("User Name:", user_repository.get_user("U123"))

```

Another way to use the instances injected by the container is to inject them into classes external to the container (this way, you don't need to use the Injector directly - but rather the inject decorator):

```python
from subtle_wired.decorators import inject


MyContainer()\
    .startup()

class OutsideTheContainer:
    @inject
    def __init__(self, user_repository: IUserRepository):
        self.__user_repository = user_repository

    def user_name(self, user_id: str) -> str:
        return self.__user_repository.get_user(user_id).name


print("User Name:", OutsideTheContainer().user_name("U123"))

```
