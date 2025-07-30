from abc import abstractmethod
import inspect
from typing import Any, Awaitable, Callable, Protocol, Self, Sequence

from plug_in.types.proto.core_host import CoreHostProtocol
from plug_in.types.proto.core_plugin import CorePluginProtocol
from plug_in.types.proto.hosted_mark import HostedMarkProtocol
from plug_in.types.proto.joint import Joint


class FinalParamStageProtocol[T: HostedMarkProtocol, JointType: Joint, MetaData](
    Protocol
):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def default(self) -> T: ...

    @property
    @abstractmethod
    def host(self) -> CoreHostProtocol[JointType]: ...

    @property
    @abstractmethod
    def plugin(self) -> CorePluginProtocol[JointType, MetaData]: ...


class ParamsStateMachineProtocol(Protocol):

    @property
    @abstractmethod
    def callable(self) -> Callable: ...

    # @property
    # @abstractmethod
    # def resolve_provider(self) -> Callable[[CoreHostProtocol], Callable[[], Joint]]: ...

    @abstractmethod
    def advance(self) -> "ParamsStateMachineProtocol": ...

    @abstractmethod
    def is_final(self) -> bool: ...

    @abstractmethod
    def assert_final(self) -> "FinalParamsProtocol":
        """
        Return self if it is a final state, or raise AssertionError.
        """
        ...

    @abstractmethod
    def finalize(self) -> "FinalParamsProtocol":
        """
        Advance to the final state or raise any of the advancing stage exceptions.
        """
        ...


class FinalParamsProtocol[T: HostedMarkProtocol, JointType: Joint](
    ParamsStateMachineProtocol, Protocol
):

    @property
    def params(self) -> Sequence[FinalParamStageProtocol[T, JointType, Any]]: ...

    @property
    def type_hints(self) -> dict[str, Any]: ...

    @property
    def sig(self) -> inspect.Signature: ...

    @property
    def callable(self) -> Callable: ...

    @property
    def plugin_lookup(self) -> Callable[[CoreHostProtocol], CorePluginProtocol]: ...

    def advance(self) -> Self: ...

    def sync_resolver_map(
        self,
    ) -> dict[str, Callable[[], JointType]]:
        """
        Returns prepared map of parameter names to their synchronous resolvers.
        """
        ...

    def async_resolver_map(self) -> dict[str, Callable[[], Awaitable[JointType]]]:
        """
        Returns prepared map of parameter names to their asynchronous resolvers.
        """
        ...
