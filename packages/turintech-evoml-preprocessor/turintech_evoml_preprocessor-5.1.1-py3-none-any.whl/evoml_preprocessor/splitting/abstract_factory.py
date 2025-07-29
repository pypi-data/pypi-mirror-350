"""Defines an abstract factory that can be used to easily create factories"""

# @TODO: this file is very generic and should be moved to a library
# (evoml_utils)?
from __future__ import annotations

import logging
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from evoml_preprocessor.utils.string_enum import StrEnum

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["AbstractFactory"]

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

InterfaceT = TypeVar("InterfaceT")
EnumT = TypeVar("EnumT", bound=Enum)


class AbstractFactory(Generic[EnumT, InterfaceT]):
    """Abstract class implementing the generic behaviour of a factory,
    i.e. mapping an enum/name to an implementation of a common interface.

    Allows you to create an instance that maps members of an enumeration
    (`EnumT`, first generic variable) to classes implementing an interface
    (`InterfaceT`, second generic variable).

    Usage
    =====
    You can use this class when you have multiple implementation of an interface
    `InterfaceT` but you'd like to allow the user to choose which one to use
    based on some sort of configuration enum `EnumT`.

    This class is meant to be instanciated with the `EnumT` and `InterfaceT`
    types in the module that defines both the enumeration and the interface.
    Then each implementation can import the factory instance, the enum and the
    interface, then register itself in the factory as an implementation of a
    given enum member.

    The main advantage of this approach is that it should limit all occurence of
    the implementation class to the module where it's defined and its tests.
    This allows you to easily add or delete implementation classes, only
    requiring you to edit the enumeration.

    Example:
    ========
    ```python
    from enum import Enum

    class NotificationType(StrEnum):
        EMAIL = "email"
        SMS = "sms"

    class NotificationProvider:
        ...

    class EmailProvider(NotificationProvider):
        ...

    class SmsProvider(NotificationProvider):
        ...

    notification_factory = AbstractFactory[NotificationType, NotificationProvider]()
    notification_factory.register(NotificationType.EMAIL, EmailProvider)
    notification_factory.register(NotificationType.SMS, SmsProvider)
    ```
    """

    logger = logging.getLogger("factory")

    def __init__(self) -> None:
        """Initializes the registry keeping track of the registered implementations"""
        self._registry: Dict[EnumT, Type[InterfaceT]] = {}

    def register(self, name: EnumT, impl: Type[InterfaceT]) -> Type[InterfaceT]:
        """Class method to register new abstract implementations to the internal registry.
        Args:
            name (str):
                The name of the entity to register.
            impl (Type[InterfaceT]):
                A class implementing the given interface
        Returns:
            The class (impl) that was registered
        """
        self._registry[name] = impl
        return impl

    def create(self, name: EnumT, *args: Any, **kwargs: Any) -> Optional[InterfaceT]:
        """Factory command to create an instance of an abstract implementation
        based on its name.

        Passes all arguments (*args, **kwargs) after the name to the class being
        instantiated.

        Args:
            name (EnumT):
                The name of the implementation to instanciate.
            args (*):
                Any number of positional arguments to provide to the chosen
                implementation.
            kwargs (**):
                Any number of keyword arguments to provide to the chosen
                implementation.
        Returns:
            An instance of the abstract interface.
        """
        implementation_class = self.get_impl(name)
        if implementation_class is None:
            return None
        instance = implementation_class(*args, **kwargs)
        return instance

    def get_impl(self, key: EnumT) -> Optional[Type[InterfaceT]]:
        """Gets the class implementation of the current interface for a given
        name/enum. Returns None if the requested implementation does not exist.
        """
        implementation = self._registry.get(key)
        if implementation is None:
            self.logger.warning(f"Implementation {key} does not exist in the registry")
        return implementation

    def get_registered(self) -> List[EnumT]:
        """Get the list of registered implementations names"""
        return list(self._registry.keys())


def new_factory(enum_t: EnumT, interface_t: InterfaceT) -> Type[AbstractFactory[EnumT, InterfaceT]]:
    """Generates a new factory for the given enum and interface pair"""

    class Factory(AbstractFactory[EnumT, InterfaceT]):
        # No need for any code here, the generic class does all of the work
        ...

    Factory.__doc__ = f"""\
    Factory mapping the values of the '{enum_t.__name__}' enum to classes
    implementing the '{interface_t.__name__}' abstract interface.
    """

    return Factory[enum_t, interface_t]
