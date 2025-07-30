from typing import Any, Optional, Type, Union

from duckdi.errors import (InterfaceAlreadyRegisteredError,
                           InvalidAdapterImplementationError)
from duckdi.errors.adapter_already_registered_error import \
    AdapterAlreadyRegisteredError
from duckdi.injections.injections_payload import InjectionsPayload
from duckdi.utils import to_snake


class InjectionsContainer:
    """
    # Internal structure that holds the mappings between registered interfaces and adapters.

    # Attributes:
        - adapters (dict): Maps the serialized interface name to its registered adapter class.
        - interfaces (dict): Maps the serialized interface name to its interface class.
    """

    adapters: dict[str, Any] = {}
    interfaces: dict[str, Type] = {}


def Interface[T](interface: Type[T], label: Optional[str] = None) -> Type[T]:
    """
    # Registers an interface for dependency injection.
    # This function is used to declare an interface that can later be mapped to an adapter implementation.
    # It ensures that the interface is uniquely registered under a resolved name or an optional label.

    # Args:
        - interface (Type[T]): The interface class to be registered.
        - label (Optional[str]): An optional custom label for the interface. If not provided, a snake_case version of the interface class name will be used.

    # Returns:
        - Type[T]: Returns the same interface class, enabling usage as a decorator.

    # Raises:
        - InterfaceAlreadyRegisteredError: If the interface or label has already been registered previously.

    # Example:
    .   @Interface
    .   class IUserRepository:
    .       ...

    # Example with a custom label:
    .   @Interface(label="user_repo")
    .   class IUserRepository:
    .       ...
    """
    interface_name = label if label is not None else to_snake(interface)
    if InjectionsContainer.interfaces.get(interface_name) is not None:
        raise InterfaceAlreadyRegisteredError(interface_name)

    InjectionsContainer.interfaces[interface_name] = interface
    return interface


def register[T](
    adapter: Type[T], label: Optional[str] = None, is_singleton: bool = False
) -> None:
    """
    # Registers an adapter (concrete implementation) for a previously registered interface.

    # This function maps an implementation class (adapter) to a label, making it available
    # for runtime resolution via the Get function. It also supports singleton behavior by
    # storing an already-instantiated adapter instance if `is_singleton` is set to True.

    # Args:
        - adapter (Type[T]): The concrete implementation class to register.
        - label (Optional[str]): An optional custom label for the adapter. If not provided, a snake_case version of the adapter class name will be used.
        - is_singleton (bool): If True, the adapter is instantiated immediately and reused on every resolution. If False, a new instance will be created each time.

    # Raises:
        - AdapterAlreadyRegisteredError: If an adapter has already been registered under the same label.

    # Example:
    .   register(PostgresUserRepository)

    # Example with a custom label:
    .   register(PostgresUserRepository, label="postgres_repo")

    # Example as a singleton:
    .   register(PostgresUserRepository, is_singleton=True)
    """
    adapter_name = label if label is not None else to_snake(adapter)

    if InjectionsContainer.adapters.get(adapter_name) is not None:
        raise AdapterAlreadyRegisteredError(adapter_name)

    InjectionsContainer.adapters[adapter_name] = adapter() if is_singleton else adapter


def Get[T](interface: Type[T], label: Optional[str] = None) -> Union[T, Type[T]]:
    """
    # Resolves and returns an instance of the adapter associated with the given interface.
    # This function is the main entry point for resolving dependencies no runtime.

    # Args:
        - interface (Type[T]): The interface class decorated with @Interface.
        - label (Optional[str]): Optional custom label used during interface registration. If omitted, the snake_case name of the interface class is used.

    # Returns:
        - T: An instance of the adapter class bound to the interface.

    # Raises
        - KeyError: If the interface is not found in the injection payload.
        - InvalidAdapterImplementationError: If the resolved adapter does not implement the expected interface.

    # Example:
    .   @Interface
    .   class IUserRepository:
    .       ...
    .
    .   register(PostgresUserRepository)
    .   user_repo = Get(IUserRepository)
    """
    injections_payload = InjectionsPayload().load()
    interface_name = label if label is not None else to_snake(interface)
    adapter = InjectionsContainer.adapters[injections_payload[interface_name]]

    if not isinstance(adapter, type):
        if not isinstance(adapter, interface):
            raise InvalidAdapterImplementationError(
                interface.__name__, type(adapter).__name__
            )
        return adapter

    if not issubclass(adapter, interface):
        raise InvalidAdapterImplementationError(interface.__name__, adapter.__name__)

    return adapter()
