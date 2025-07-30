from collections.abc import Collection
from typing import TYPE_CHECKING, Optional

from sym_metanet.blocks.base import ElementWithVars
from sym_metanet.engines.core import EngineBase, get_current_engine
from sym_metanet.util.funcs import first
from sym_metanet.util.types import VarType

if TYPE_CHECKING:
    from sym_metanet.blocks.links import Link
    from sym_metanet.blocks.nodes import Node
    from sym_metanet.network import Network


class Destination(ElementWithVars[VarType]):
    """Ideal congestion-free destination, representing a sink where cars can leave the
    highway with no congestion (i.e., no slowing down due to downstream density)."""

    def init_vars(self, *_, **__) -> None:
        """Initializes no variable in the ideal destination."""

    def step_dynamics(self, *_, **__) -> dict[str, VarType]:
        """No dynamics to steps in the ideal destination."""
        return {}

    def get_density(
        self, net: "Network", engine: Optional[EngineBase] = None, **_
    ) -> VarType:
        """Computes the (downstream) density induced by the ideal destination.

        Parameters
        ----------
        net : Network
            The network this destination belongs to.

        Returns
        -------
        symbolic variable
            The destination's downstream density.
        """
        if engine is None:
            engine = get_current_engine()
        link_up = self._get_entering_link(net)
        return engine.destinations.get_congestion_free_downstream_density(
            link_up.states["rho"][-1], link_up.rho_crit
        )

    def _get_entering_link(self, net: "Network") -> "Link[VarType]":
        """Internal utility to fetch the link entering this destination (can only be
        one)."""
        links_up: Collection[tuple["Node", "Node", "Link[VarType]"]] = net.in_links(
            net.destinations[self]  # type: ignore[index]
        )
        assert (
            len(links_up) == 1
        ), "Internal error. Only one link can enter a destination."
        return first(links_up)[-1]


class CongestedDestination(Destination[VarType]):
    """Destination with a downstream density scenario to emulate congestions, that is,
    cars cannot exit freely the highway but must slow down and, possibly, create a
    congestion."""

    _disturbances = {"d"}

    def init_vars(
        self,
        init_conditions: Optional[dict[str, VarType]] = None,
        engine: Optional[EngineBase] = None,
        **_,
    ) -> None:
        """Initializes
        - `d`: downstream density scenario (disturbance).

        Parameters
        ----------
        net : Network
            The network this destination belongs to.
        init_conditions : dict[str, variable], optional
            Provides name-variable tuples to initialize states, actions and disturbances
            with specific values. These values must be compatible with the symbolic
            engine in type and shape. If not provided, variables are initialized
            automatically.
        engine : EngineBase, optional
            The engine to be used. If `None`, the current engine is used.
        """
        if engine is None:
            engine = get_current_engine()
        self.disturbances: dict[str, VarType] = {
            "d": engine.var(f"d_{self.name}")
            if init_conditions is None or "d" not in init_conditions
            else init_conditions["d"]
        }

    def get_density(
        self, net: "Network", engine: Optional[EngineBase] = None, **_
    ) -> VarType:
        """Computes the (downstream) density induced by the congested destination.

        Parameters
        ----------
        net : Network
            The network this destination belongs to.
        engine : EngineBase, optional
            The engine to be used. If `None`, the current engine is used.

        Returns
        -------
        variable
            The destination's downstream density.
        """
        if engine is None:
            engine = get_current_engine()
        link_up = self._get_entering_link(net)
        return engine.destinations.get_congested_downstream_density(
            link_up.states["rho"][-1], self.disturbances["d"], link_up.rho_crit
        )
