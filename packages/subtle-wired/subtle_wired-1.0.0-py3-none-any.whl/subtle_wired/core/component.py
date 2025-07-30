__author__ = "Willian Antônio"

from typing import Literal, Protocol, TypedDict

InjectedType = Literal["singleton", "factory"]


class ContainerConfig(TypedDict):
    injected_type: InjectedType
    is_lazy: bool


class ContainerComponent(Protocol):
    @classmethod
    def container_config(cls) -> ContainerConfig:
        pass
