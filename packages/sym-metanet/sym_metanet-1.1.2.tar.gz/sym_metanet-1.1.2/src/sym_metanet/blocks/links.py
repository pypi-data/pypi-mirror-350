from collections.abc import Collection
from typing import TYPE_CHECKING, Any, Literal, Optional, Union

from sym_metanet.blocks.base import ElementWithVars
from sym_metanet.blocks.origins import MeteredOnRamp
from sym_metanet.engines.core import EngineBase, get_current_engine
from sym_metanet.util.funcs import first
from sym_metanet.util.types import VarType

if TYPE_CHECKING:
    from sym_metanet.blocks.nodes import Node
    from sym_metanet.network import Network


class Link(ElementWithVars[VarType]):
    """Highway link between two nodes [1, Section 3.2.1]. Links represent stretch of
    highway with similar traffic characteristics and no road changes (e.g., same number
    of lanes and maximum speed).

    References
    ----------
    [1] Hegyi, A., 2004, "Model predictive control for integrating traffic control
        measures", Netherlands TRAIL Research School.
    """

    __slots__ = ("N", "lam", "L", "rho_max", "rho_crit", "v_free", "a", "turnrate")
    _states = {"rho", "v"}

    def __init__(
        self,
        nb_segments: int,
        lanes: Union[VarType, int],
        length: Union[VarType, float],
        maximum_density: Union[VarType, float],
        critical_density: Union[VarType, float],
        free_flow_velocity: Union[VarType, float],
        a: Union[VarType, float],
        turnrate: Union[VarType, float] = 1.0,
        name: Optional[str] = None,
    ) -> None:
        """Creates an instance of a METANET link.

        Parameters
        ----------
        nb_segments : int
            Number of segments in this highway link, i.e., `N`.
        lanes : int or variable
            Number of lanes in each segment, i.e., `lam`.
        lengths : float or variable
            Length of each segment in the link, i.e., `L`.
        maximum density : float or variable
            Maximum density that the link can withstand, i.e., `rho_max`.
        critical_densities : float or variable
            Critical density at which the traffic flow is maximal, i.e., `rho_crit`.
        free_flow_velocities : float or variable
            Average speed of cars when traffic is freely flowing, i.e., `v_free`.
        a : float or variable
            Model parameter in the computations of the equivalent speed [1, Equation
            3.4].
        turnrate : float or variable, optional
            Fraction of the total flow that enters this link via the upstream node. Only
            relevant if multiple exiting links are attached to the same node, in order
            to split the flow according to these rates. Needs not be normalized. By
            default, all links have equal rates.
        name : str, optional
            Name of this link, by default `None`.

        References
        ----------
        [1] Hegyi, A., 2004, "Model predictive control for integrating traffic control
            measures", Netherlands TRAIL Research School.
        """
        super().__init__(name)
        self.N = nb_segments
        self.lam = lanes
        self.L = length
        self.rho_max = maximum_density
        self.rho_crit = critical_density
        self.v_free = free_flow_velocity
        self.a = a
        self.turnrate = turnrate

    def init_vars(
        self,
        init_conditions: Optional[dict[str, VarType]] = None,
        engine: Optional[EngineBase] = None,
        positive_init_speed: bool = False,
        positive_init_density: bool = False,
        **_,
    ) -> None:
        """For each segment in the link, initializes
         - `rho`: densities (state)
         - `v`: speeds (state).

        Parameters
        ----------
        init_conditions : dict[str, variable], optional
            Provides name-variable tuples to initialize states, actions and disturbances
            with specific values. These values must be compatible with the symbolic
            engine in type and shape. If not provided, variables are initialized
            automatically.
        engine : EngineBase, optional
            The engine to be used. If `None`, the current engine is used.
        positive_init_speed, positive_init_density : bool, optional
            If `True`, forces the initial speed/density to be positive, e.g., as
            `v = max(0, v)`. METANET is in fact known to sometime yield negative
            quantities, which are infeasible in reality.
        """
        if init_conditions is None:
            init_conditions = {}
        if engine is None:
            engine = get_current_engine()

        self.states: dict[str, VarType] = {
            name: (
                init_conditions[name]
                if name in init_conditions
                else engine.var(f"{name}_{self.name}", self.N)
            )
            for name in ("rho", "v")
        }

        if positive_init_density:
            self.states["rho"] = engine.max(0, self.states["rho"])
        if positive_init_speed:
            self.states["v"] = engine.max(0, self.states["v"])

    def get_flow(self, engine: Optional[EngineBase] = None, **kwargs) -> VarType:
        """Gets the flow in this link's segments.

        Parameters
        ----------
        engine : EngineBase, optional
            The engine to be used. If `None`, the current engine is used.

        Returns
        -------
        variable
            The flow in this link.
        """
        if engine is None:
            engine = get_current_engine()
        return engine.links.get_flow(self.states["rho"], self.states["v"], self.lam)

    def step_dynamics(
        self,
        net: "Network",
        tau: Union[VarType, float],
        eta: Union[VarType, float],
        kappa: Union[VarType, float],
        T: Union[VarType, float],
        delta: Union[None, VarType, float] = None,
        phi: Union[None, VarType, float] = None,
        engine: Optional[EngineBase] = None,
        positive_next_speed: bool = True,
        positive_next_density: bool = False,
        **_,
    ) -> dict[str, VarType]:
        """Steps the dynamics of this link.

        Parameters
        ----------
        net : Network
            The network the link belongs to.
        tau : float or variable
            Model parameter for the speed relaxation term.
        eta : float or variable
            Model parameter for the speed anticipation term.
        kappa : float or variable
            Model parameter for the speed anticipation term.
        T : float or variable
            Sampling time.
        delta : float or variable, optional
            Model parameter for merging phenomenum. By default, not considered.
        phi : float or variable, optional
            Model parameter for lane drop phenomenum. By defaul, not considered.
        engine : EngineBase, optional
            The engine to be used. If `None`, the current engine is used.
        positive_next_speed, positive_next_density : bool, optional
            If `True`, forces the speed/density at the next time step to be positive,
            e.g., as `v+ = max(0, v+)`. METANET is in fact known to sometime yield
            negative quantities, which are infeasible in reality.

        Returns
        -------
        Dict[str, variable]
            A dict with the states of the link (speeds and densities) at the next time
            step.
        """
        if engine is None:
            engine = get_current_engine()

        node_up, node_down = net.nodes_by_link[self]  # type: ignore[index]
        rho = self.states["rho"]
        v = self.states["v"]
        q = self.get_flow(engine)

        # get upstream flow and speed, and downstream density
        v0, q0 = node_up.get_upstream_speed_and_flow(net, self, engine, T=T)
        rhoN_1 = node_down.get_downstream_density(net, engine)
        if self.N > 1:
            q_up = engine.vcat(q0, q[:-1])
            v_up = engine.vcat(v0, v[:-1])
            rho_down = engine.vcat(rho[1:], rhoN_1)
        else:
            q_up = q0
            v_up = v0
            rho_down = rhoN_1

        # check for ramp merging in this link's upstream node with other
        # entering links.
        q_ramp = None
        if (
            delta is not None
            and node_up in net.origins_by_node
            and any(net.in_links(node_up))
        ):
            origin = net.origins_by_node[node_up]  # type: ignore[index]
            if isinstance(origin, MeteredOnRamp):
                q_ramp = origin.get_flow(net, T, engine)

        # check for lane drops in the next link (only if one link downstream)
        lanes_drop = None
        if phi is not None:
            links_down: Collection[
                tuple["Node", "Node", "Link[VarType]"]
            ] = net.out_links(node_down)
            if len(links_down) == 1:
                link_down = first(links_down)[-1]
                lanes_drop = self.lam - link_down.lam  # type: ignore[operator]
            if lanes_drop == 0:
                lanes_drop = None

        # step densities
        rho_next = engine.links.step_density(rho, q, q_up, self.lam, self.L, T)

        # step speeds
        Veq = self._get_equilibrium_speed(engine, rho)
        v_next = engine.links.step_speed(
            v,
            v_up,
            rho,
            rho_down,
            Veq,
            self.lam,
            self.L,
            tau,
            eta,
            kappa,
            T,
            q_ramp,
            delta,
            lanes_drop,
            phi,
            self.rho_crit,
        )
        if positive_next_density:
            rho_next = engine.max(0, rho_next)
        if positive_next_speed:
            v_next = engine.max(0, v_next)
        return {"rho": rho_next, "v": v_next}

    def _get_equilibrium_speed(self, engine: EngineBase, rho: VarType) -> VarType:
        """Internal utility to compute the equilibrium speed for the link's segments."""
        return engine.links.Veq(rho, self.v_free, self.rho_crit, self.a)


class LinkWithVsl(Link[VarType]):
    """Highway link between two nodes and whose segments are equipped with Variable
    Speed Limit signs [1, Section 3.3.1].

    References
    ----------
    [1] Hegyi, A., 2004, "Model predictive control for integrating traffic control
        measures", Netherlands TRAIL Research School.
    """

    __slots__ = ("vsl", "alpha")
    _actions = {"v_ctrl"}

    def __init__(
        self, *args: Any, segments_with_vsl: set[int], alpha: float, **kwargs: Any
    ) -> None:
        """Creates an instance of a METANET link with VSL signs.

        Parameters
        ----------
        args, kwargs
            See base class `Link` for the other parameters.
            Average speed of cars when traffic is freely flowing, i.e., `v_free`.
        segments_with_vsl : set of ints
            The set of segment indices that are equipped with a VSL sign (0-based).
        alpha : float
            Non-compliance factor to the indicated speed limit.

        References
        ----------
        [1] Hegyi, A., 2004, "Model predictive control for integrating traffic control
            measures", Netherlands TRAIL Research School.
        """
        super().__init__(*args, **kwargs)
        self.vsl = sorted(segments_with_vsl)  # has to be a list for indexing vectors
        self.alpha = alpha
        for index in self.vsl:
            if index >= self.N or index < 0:
                raise ValueError(f"Invalid segment index {index} for VSL sign.")

    def init_vars(
        self,
        init_conditions: Optional[dict[str, VarType]] = None,
        engine: Optional[EngineBase] = None,
        **kwargs: Any,
    ) -> None:
        """For each segment in the link, initializes
         - `rho`: densities (state)
         - `v`: speeds (state)
        and, if the segment is equipped with a VSL sign, initializes also the control
        speed
         - `v_ctrl` (action).

        Parameters
        ----------
        init_conditions : dict[str, variable], optional
            Provides name-variable tuples to initialize states, actions and disturbances
            with specific values. These values must be compatible with the symbolic
            engine in type and shape. If not provided, variables are initialized
            automatically.
        engine : EngineBase, optional
            The engine to be used. If `None`, the current engine is used.
        kwargs
            See method of base class `Link`.
        """
        if init_conditions is None:
            init_conditions = {}
        if engine is None:
            engine = get_current_engine()
        super().init_vars(init_conditions, engine, **kwargs)
        self.actions: dict[str, VarType] = {
            "v_ctrl": init_conditions["v_ctrl"]
            if "v_ctrl" in init_conditions
            else engine.var(f"v_ctrl_{self.name}", len(self.vsl))
        }

    def _get_equilibrium_speed(self, engine: EngineBase, rho: VarType) -> VarType:
        return engine.links.controlled_Veq(
            rho,
            self.actions["v_ctrl"],
            self.vsl,
            self.alpha,
            self.v_free,
            self.rho_crit,
            self.a,
        )


class SimplifiedLinkWithVsl(LinkWithVsl[VarType]):
    """A simplified version of a link with VSL sign, where the equilibrium speed of the
    link is the direct control action (instead of controlling the displayed speed).

    See `LinkWithVsl` for the original version."""

    __slots__ = ("vsl", "alpha", "V_eq_type")
    _actions = {"V"}

    def __init__(
        self,
        *args: Any,
        segments_with_vsl: set[int],
        V_eq_type: Literal["limited", "unlimited"] = "limited",
        **kwargs: Any,
    ) -> None:
        """Creates an instance of a (simplified) METANET link with VSL signs.

        Parameters
        ----------
        args, kwargs
            See base class `Link` for the other parameters.
            Average speed of cars when traffic is freely flowing, i.e., `v_free`.
        segments_with_vsl : set of ints
            The set of segment indices that are equipped with a VSL sign (0-based).
        V_eq_type : "limited" or "unlimited"
            If "limited", the equilibrium speed action is capped by the standard
            equilibrium speed of the link, which is a function of the link density. If
            "unlimited", this cap is not forced, and it's up to the user to satisfy it.
            By default, "limited" is selected.

        References
        ----------
        [1] Hegyi, A., 2004, "Model predictive control for integrating traffic control
            measures", Netherlands TRAIL Research School.
        """
        super().__init__(
            *args, segments_with_vsl=segments_with_vsl, alpha=float("nan"), **kwargs
        )
        self.V_eq_type = V_eq_type

    def init_vars(
        self,
        init_conditions: Optional[dict[str, VarType]] = None,
        engine: Optional[EngineBase] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initializes as control action the equilibrium speed `V` of the link instead
        of the control speed `v_ctrl`."""
        if init_conditions is None:
            init_conditions = {}
        if engine is None:
            engine = get_current_engine()

        super().init_vars(init_conditions, engine, *args, **kwargs)

        del self.actions["v_ctrl"]
        self.actions["V"] = (
            init_conditions["V"]
            if "V" in init_conditions
            else engine.var(f"V_{self.name}", len(self.vsl))
        )

    def _get_equilibrium_speed(self, engine: EngineBase, rho: VarType) -> VarType:
        if engine is None:
            engine = get_current_engine()
        V_ctrl = self.actions["V"]
        Veq = engine.links.Veq(rho, self.v_free, self.rho_crit, self.a)
        if self.V_eq_type == "unlimited":
            Veq[self.vsl] = V_ctrl
        else:
            Veq[self.vsl] = engine.min(Veq[self.vsl], V_ctrl)
        return Veq
