__author__ = "Willian Antônio"

from abc import ABC

from subtle_wired.core.component import (
    ContainerComponent,
)
from subtle_wired.core.injector import Injector


class Container(ABC):
    components: list[ContainerComponent] = []

    def startup(self):
        for comp in self.__class__.components:
            if not hasattr(comp, "container_config"):
                raise AttributeError(
                    f"The class '{comp.__name__}' must be decorated with a singleton or factory to be used in the container!"
                )

            config = comp.container_config()
            Injector().upsert_implementation(
                comp,
                injected_type=config.get("injected_type", "singleton"),
                is_lazy=config.get("is_lazy", False),
            )

        Injector().make_all_instances()
