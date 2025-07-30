__author__ = "Willian Antônio"

from abc import ABC
from inspect import Signature, _empty, getmro, signature
from threading import Lock
from typing import Any, Callable, Optional, Type, TypeVar

from subtle_wired.core.base import Singleton
from subtle_wired.core.component import InjectedType


T = TypeVar("T", bound=ABC)


class InjectedItem(object):
    def __init__(
        self,
        interface: type,
        implementation: Type,
        injected_type: InjectedType = "singleton",
        is_lazy: bool = False,
    ):
        InjectedItem.validate_interface(interface)

        self.__interface = interface
        self.__implementation = implementation
        self.__injected_type = injected_type
        self.__is_lazy = is_lazy
        self.__instance = None
        self.__item_lock = Lock()

    @staticmethod
    def get_interface_name(interface: Type) -> Optional[str]:
        return getattr(interface, "__name__", None)

    @staticmethod
    def get_implementation_interface(
        implementation: type,
    ) -> Optional[type[ABC]]:
        interfaces = [
            base
            for base in getmro(implementation)
            if issubclass(base, ABC) and base is not ABC and base is not implementation
        ]

        return interfaces[0] if len(interfaces) > 0 else None

    @staticmethod
    def validate_implementation(implementation: type):
        interface = InjectedItem.get_implementation_interface(implementation)
        if interface is None:
            raise AttributeError(
                "Class '"
                + implementation.__name__
                + "' does not implement any interface, cannot be registered!"
            )

    @staticmethod
    def validate_interface(interface: Type):
        name = InjectedItem.get_interface_name(interface)
        if name is None:
            raise AttributeError("interface has no name!")

    @property
    def name(self) -> str:
        return self.__interface.__name__

    @property
    def interface(self) -> Type:
        return self.__interface

    @property
    def implementation(self) -> Type:
        return self.__implementation

    @property
    def is_lazy(self) -> bool:
        return self.__is_lazy

    def update_implementation(
        self,
        implementation: Type,
        injected_type: InjectedType = "singleton",
        is_lazy: bool = False,
    ):
        with self.__item_lock:
            self.__implementation = implementation
            self.__injected_type = injected_type
            self.__is_lazy = is_lazy
            self.__instance = None

    def create_instance(
        self,
        injector: "Injector",
        interface_consulted: dict[str, bool],
    ) -> Any:
        interface_consulted[self.name] = True
        with self.__item_lock:
            if self.__instance is None or self.__injected_type == "factory":
                dependencies: list[Any] = []
                sig: Signature = signature(self.__implementation.__init__)
                for param in sig.parameters:
                    if param == "self":
                        continue

                    dep_type = sig.parameters[param].annotation
                    dep_default_value = sig.parameters[param].default
                    if dep_type is not _empty:
                        dependency = injector.get_instance_recursive(
                            dep_type, dep_default_value, interface_consulted
                        )
                    elif dep_default_value is not _empty:
                        dependency = dep_default_value
                    else:
                        raise AttributeError(
                            "Parameter '"
                            + param
                            + "' (type '"
                            + self.name
                            + "') not informed, without a type and default value!"
                        )
                    dependencies.append(dependency)
                self.__instance = self.__implementation(*dependencies)
        return self.__instance

    @staticmethod
    def get_init_wrapper(
        init_function: Callable,
        injector: "Injector",
    ) -> Callable:
        def init_wrapper(self):
            interface_consulted: dict[str, bool] = {}
            interface = InjectedItem.get_implementation_interface(self.__class__)
            if interface is not None:
                name = InjectedItem.get_interface_name(interface)
                interface_consulted[name] = True

            sig: Signature = signature(init_function)
            dependencies: list[Any] = []
            for param in sig.parameters:
                if param == "self":
                    continue

                dep_type = sig.parameters[param].annotation
                dep_default_value = sig.parameters[param].default
                if dep_type is not _empty:
                    dependency = injector.get_instance_recursive(
                        dep_type, _empty, interface_consulted
                    )
                elif dep_default_value is not _empty:
                    dependency = dep_default_value
                else:
                    raise AttributeError(
                        "Parameter '"
                        + param
                        + "' not informed, without a type and default value!"
                    )
                dependencies.append(dependency)
            return init_function(self, *dependencies)

        return init_wrapper

    @staticmethod
    def get_method_wrapper(
        method_function: Callable,
        injector: "Injector",
    ) -> Any:
        def get_wrapper(self):
            interface_consulted: dict[str, bool] = {}
            interface = InjectedItem.get_implementation_interface(self.__class__)
            if interface is not None:
                name = InjectedItem.get_interface_name(interface)
                interface_consulted[name] = True

            sig: Signature = signature(method_function)
            return injector.get_instance_recursive(
                sig.return_annotation, _empty, interface_consulted
            )

        return get_wrapper


class Injector(Singleton):
    def __init__(self):
        self.interfaces: dict[str, InjectedItem] = dict()
        self.global_lock = Lock()
        super(Injector, self).__init__()

    def __get_injected_item(self, interface: Type) -> Optional[InjectedItem]:
        InjectedItem.validate_interface(interface)
        name = InjectedItem.get_interface_name(interface)
        item: InjectedItem = None
        if name in self.interfaces:
            item = self.interfaces[name]
        return item

    def __set_injected_item(
        self,
        interface: Type,
        implementation: Type,
        injected_type: InjectedType = "singleton",
        is_lazy: bool = False,
    ):
        with self.global_lock:
            item = InjectedItem(interface, implementation, injected_type, is_lazy)
            self.interfaces[item.name] = item

    def upsert_implementation(
        self,
        implementation: Type,
        injected_type: InjectedType = "singleton",
        is_lazy: bool = False,
    ):
        InjectedItem.validate_implementation(implementation)
        interface = InjectedItem.get_implementation_interface(implementation)
        assert hasattr(interface, "__init__")
        item = self.__get_injected_item(interface)
        if item is not None:
            raise AttributeError(
                "Interface '"
                + item.name
                + "' already registered for implementation '"
                + item.implementation.__name__
                + "'. Unable to register '"
                + implementation.__name__
                + "' implementation!"
            )
        else:
            self.__set_injected_item(interface, implementation, injected_type, is_lazy)

    def get_implementation(self, interface: Type) -> Type:
        item = self.__get_injected_item(interface)
        if item is not None:
            return item.implementation
        else:
            InjectedItem.validate_interface(interface)
            name = InjectedItem.get_interface_name(interface)
            raise AttributeError("Interface '" + name + "' not found!")

    def get_instance_recursive(
        self,
        interface: Type,
        default_value: Any,
        interface_consulted: dict[str, bool],
    ) -> Any:
        InjectedItem.validate_interface(interface)
        name = InjectedItem.get_interface_name(interface)
        item = self.__get_injected_item(interface)
        if name in interface_consulted:
            raise AttributeError("Circular reference for type '" + name + "'!")
        if item is not None:
            return item.create_instance(self, interface_consulted)
        elif default_value is not _empty:
            return default_value
        else:
            raise AttributeError(
                "Interface '" + name + "' and default value not found!"
            )

    def get_instance(self, interface: type[T]) -> T:
        interface_consulted: dict[str, bool] = {}
        return self.get_instance_recursive(interface, _empty, interface_consulted)

    def make_all_instances(self):
        for name in self.interfaces:
            item = self.interfaces[name]
            if item.is_lazy:
                continue

            interface_consulted: dict[str, bool] = {}
            self.get_instance_recursive(item.interface, _empty, interface_consulted)
