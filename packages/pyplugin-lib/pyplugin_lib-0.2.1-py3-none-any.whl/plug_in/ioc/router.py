from functools import wraps
from typing import Any, Awaitable, Callable, cast, overload

from plug_in.exc import MissingMountError, MissingRouteError, RouterAlreadyMountedError
from plug_in.types.proto.core_host import CoreHostProtocol
from plug_in.types.proto.core_plugin import CorePluginProtocol
from plug_in.types.proto.core_registry import CoreRegistryProtocol
from plug_in.types.proto.resolver import ParameterResolverProtocol
from plug_in.types.proto.router import RouterProtocol
from plug_in.types.proto.joint import Joint
from plug_in.types.alias import Manageable
from plug_in.ioc.resolver import ParameterResolver


class Router(RouterProtocol):

    def __init__(self) -> None:
        self._reg: CoreRegistryProtocol | None = None
        self._routes = {}

    def mount(self, registry: CoreRegistryProtocol) -> None:
        """
        Raises:
            [plug_in.exc.RouterAlreadyMountedError][]: ...
        """
        if self._reg is not None:
            raise RouterAlreadyMountedError(
                f"This router {self} is already mounted ({self._reg})"
            )

        self._reg = registry

    def get_registry(self) -> CoreRegistryProtocol:
        """
        Raises:
            [plug_in.exc.MissingMountError][]: ...
        """
        if self._reg is None:
            raise MissingMountError(f"Mount is missing for this router ({self})")

        return self._reg

    def resolve[
        JointType: Joint
    ](self, host: CoreHostProtocol[JointType]) -> JointType | Awaitable[JointType]:
        """
        Resolve a host via mounted registry.

        Raises:
            [plug_in.exc.MissingMountError][]: ...
            [plug_in.exc.MissingPluginError][]: ...
        """
        reg = self.get_registry()
        return reg.resolve(host)

    def plugin_lookup(self, host: CoreHostProtocol) -> CorePluginProtocol:
        return self.get_registry().plugin(host)

    @overload
    def _callable_route_factory[
        R, **P
    ](self, callable: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]: ...

    @overload
    def _callable_route_factory[
        R, **P
    ](self, callable: Callable[P, R]) -> Callable[P, R]: ...

    def _callable_route_factory[
        R, **P
    ](self, callable: Callable[P, R] | Callable[P, Awaitable[R]]) -> (
        Callable[P, R] | Callable[P, Awaitable[R]]
    ):
        """
        Create new callable that will have default values substituted by a plugin
        resolver.

        Args:
            callable: Subject callable.

        Returns:
            New callable with substituted `CoreHost` defaults. Nothing but default
            values to parameters change in new callable signature.
        """
        # Keep parameter resolver
        param_resolver = ParameterResolver(
            callable=callable, plugin_lookup=self.plugin_lookup
        )

        self._routes[callable] = param_resolver

        if param_resolver.should_use_async_bind:
            # Create async wrapper for callable
            @wraps(callable)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                # Get arg bind
                bind = await param_resolver.get_one_time_bind_async(*args, **kwargs)

                # Proceed with call
                return await cast(Callable[P, Awaitable[R]], callable)(
                    *bind.args, **bind.kwargs
                )

            return async_wrapper
        else:
            # Create wrapper for callable
            @wraps(callable)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                # Get arg bind
                bind = param_resolver.get_one_time_bind_sync(*args, **kwargs)

                # Proceed with call
                return cast(Callable[P, R], callable)(*bind.args, **bind.kwargs)

            return wrapper

    def manage[T: Manageable](self) -> Callable[[T], T]:
        """
        Decorator maker for marking callables to be managed by plug_in IoC system.

        plug_in IoC system applies modification to the runtime of decorated
        callable, but does not changes its type hints. Default values of
        host type are just replaces with resolved default values. No further
        modification is applied to the marked callable.

        Args:
            eager_forward_resolve: Set this to `False` when You are using hosts
                with subjects being generic classes parametrized with forward
                references. Defaults to `True`. Default behavior slightly improves
                call-time performance.

        Returns:
            Decorator that makes your callable a manageable entity

        """
        return cast(Callable[[T], T], self._callable_route_factory)

    def get_route_resolver[
        **CallParams
    ](self, callable: Callable[CallParams, Any]) -> ParameterResolverProtocol[
        CallParams
    ]:
        """
        Return resolver for given callable.

        Raises:
            [.MissingRouteError][]: If callable is not managed by this router
        """
        try:
            return self._routes[callable]
        except KeyError as e:
            raise MissingRouteError(
                f"Route for {callable=} is not managed by this router"
            ) from e
