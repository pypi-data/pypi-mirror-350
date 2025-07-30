from collections.abc import Collection
from typing import TYPE_CHECKING, Any, Literal, Optional, Union

from sym_metanet.blocks.base import ElementWithVars
from sym_metanet.engines.core import EngineBase, get_current_engine
from sym_metanet.util.funcs import first
from sym_metanet.util.types import VarType

if TYPE_CHECKING:
    from sym_metanet.blocks.links import Link
    from sym_metanet.blocks.nodes import Node
    from sym_metanet.network import Network


class Origin(ElementWithVars[VarType]):
    """Ideal, state-less highway origin that conveys to the attached link as much flow
    as the flow in such link."""

    def init_vars(self, *_, **__) -> None:
        """Initializes no variable in the ideal origin."""

    def step_dynamics(self, *_, **__) -> dict[str, VarType]:
        """No dynamics to steps in the ideal origin."""
        return {}

    def get_speed(self, net: "Network", **__) -> VarType:
        """Computes the (upstream) speed induced by the ideal origin.

        Parameters
        ----------
        net : Network
            The network this destination belongs to.

        Returns
        -------
        variable
            The origin's upstream speed.
        """
        return self._get_exiting_link(net).states["v"][0]

    def get_flow(
        self, net: "Network", engine: Optional[EngineBase] = None, **kwargs
    ) -> VarType:
        """Computes the (upstream) flow induced by the ideal origin.

        Parameters
        ----------
        net : Network
            The network this destination belongs to.
        engine : EngineBase, optional
            The engine to be used. If `None`, the current engine is used.

        Returns
        -------
        symbolic variable
            The origin's upstream flow.
        """
        return self._get_exiting_link(net).get_flow(engine)[0]

    def _get_exiting_link(self, net: "Network") -> "Link[VarType]":
        """Internal utility to fetch the link leaving this destination (can only be
        one)."""
        links_down: Collection[tuple["Node", "Node", "Link[VarType]"]] = net.out_links(
            net.origins[self]  # type: ignore[index]
        )
        assert (
            len(links_down) == 1
        ), "Internal error. Only one link can leave an origin."
        return first(links_down)[-1]


class MainstreamOrigin(Origin[VarType]):
    """Mainstream origin, i.e., and origin whose queue is an abstraction of the sections
    upstream of boundaries of the freeway network that we are modeling. This origin is
    also equipped with a speed limit sign that allows to control the speed of the
    vehicles entering via it. For reference, see [1, Section 3.3.3].

    References
    [1] Hegyi, A., 2004, "Model predictive control for integrating traffic control
        measures", Netherlands TRAIL Research School.
    """

    _states = {"w"}
    _actions = {"r"}
    _disturbances = {"d"}

    def init_vars(
        self,
        init_conditions: Optional[dict[str, VarType]] = None,
        engine: Optional[EngineBase] = None,
        positive_init_queue: bool = False,
        **_,
    ) -> None:
        """Initializes
         - `w`: queue length (state)
         - `v_ctrl`: speed limit (control action)
         - `d`: demand (disturbance).

        Parameters
        ----------
        init_conditions : dict[str, variable], optional
            Provides name-variable tuples to initialize states, actions and disturbances
            with specific values. These values must be compatible with the symbolic
            engine in type and shape. If not provided, variables are initialized
            automatically.
        engine : EngineBase, optional
            The engine to be used. If `None`, the current engine is used.
        positive_init_queue : bool, optional
            If `True`, forces the initial queue to be positive, e.g., as
            `w = max(0, w)`. METANET is in fact known to sometime yield negative
            quantities, which are infeasible in reality.
        """
        if init_conditions is None:
            init_conditions = {}
        if engine is None:
            engine = get_current_engine()

        self.states: dict[str, VarType] = {
            "w": init_conditions["w"]
            if "w" in init_conditions
            else engine.var(f"w_{self.name}")
        }
        self.actions: dict[str, VarType] = {
            "v_ctrl": init_conditions["v_ctrl"]
            if "v_ctrl" in init_conditions
            else engine.var(f"v_ctrl_{self.name}")
        }
        self.disturbances: dict[str, VarType] = {
            "d": init_conditions["d"]
            if "d" in init_conditions
            else engine.var(f"d_{self.name}")
        }

        if positive_init_queue:
            self.states["w"] = engine.max(0, self.states["w"])

    def step_dynamics(
        self,
        net: "Network",
        T: Union[VarType, float],
        engine: Optional[EngineBase] = None,
        positive_next_queue: bool = False,
        **kwargs,
    ) -> dict[str, VarType]:
        """Steps the dynamics of this origin.

        Parameters
        ----------
        net : Network
            The network the origin belongs to.
        T : variable or float
            Sampling time.
        engine : EngineBase, optional
            The engine to be used. If `None`, the current engine is used.
        positive_next_queue : bool, optional
            If `True`, forces the queue at the next time step to be positive, e.g., as
            `w+ = max(0, w+)`. METANET is in fact known to sometime yield negative
            quantities, which are infeasible in reality.

        Returns
        -------
        Dict[str, variable]
            A dict with the states of the origin (queue) at the next time step.
        """
        if engine is None:
            engine = get_current_engine()

        q = self.get_flow(net, T, engine, **kwargs)
        w_next = engine.origins.step_queue(
            self.states["w"], self.disturbances["d"], q, T
        )

        if positive_next_queue:
            w_next = engine.max(0, w_next)
        return {"w": w_next}

    def get_flow(  # type: ignore[override]
        self,
        net: "Network",
        T: Union[VarType, float],
        engine: Optional[EngineBase] = None,
        **_,
    ) -> VarType:
        """Computes the (upstream) flow induced by the mainstream oriogin.

        Parameters
        ----------
        net : Network
            The network this destination belongs to.
        T : variable or float
            Sampling time of the simulation.
        engine : EngineBase, optional
            The engine to be used. If `None`, the current engine is used.

        Returns
        -------
        variable
            The origin's upstream flow.
        """
        if engine is None:
            engine = get_current_engine()
        link_down = self._get_exiting_link(net)
        return engine.origins.get_mainstream_flow(
            self.disturbances["d"],
            self.states["w"],
            self.actions["v_ctrl"],
            link_down.states["v"][0],
            link_down.rho_crit,
            link_down.a,
            link_down.v_free,
            link_down.lam,
            T,
        )


class MeteredOnRamp(Origin[VarType]):
    """On-ramp where cars can queue up before being given access to the attached link.
    For reference, look at [1], in particular, Section 3.2.1 and Equations 3.5 and 3.6.

    References
    ----------
    [1] Hegyi, A., 2004, "Model predictive control for integrating traffic control
        measures", Netherlands TRAIL Research School.
    """

    __slots__ = ("C", "flow_eq_type")
    _states = {"w"}
    _actions = {"r"}
    _disturbances = {"d"}

    def __init__(
        self,
        capacity: Union[VarType, float],
        flow_eq_type: Literal["in", "out"] = "out",
        name: Optional[str] = None,
    ) -> None:
        """Instantiates an on-ramp with the given capacity.

        Parameters
        ----------
        capacity : float or variable
            Capacity of the on-ramp, i.e., `C`.
        flow_eq_type : 'in' or 'out', optional
            Type of flow equation for the ramp. See
            `engine.origins.get_ramp_flow` for more details.
        name : str, optional
            Name of the on-ramp, by default None.
        """
        super().__init__(name)
        self.C = capacity
        self.flow_eq_type = flow_eq_type

    def init_vars(
        self,
        init_conditions: Optional[dict[str, VarType]] = None,
        engine: Optional[EngineBase] = None,
        positive_init_queue: bool = False,
        **_,
    ) -> None:
        """Initializes
         - `w`: queue length (state)
         - `r`: ramp metering rate (control action)
         - `d`: demand (disturbance).

        Parameters
        ----------
        init_conditions : dict[str, variable], optional
            Provides name-variable tuples to initialize states, actions and disturbances
            with specific values. These values must be compatible with the symbolic
            engine in type and shape. If not provided, variables are initialized
            automatically.
        engine : EngineBase, optional
            The engine to be used. If `None`, the current engine is used.
        positive_init_queue : bool, optional
            If `True`, forces the initial queue to be positive, e.g., as
            `w = max(0, w)`. METANET is in fact known to sometime yield negative
            quantities, which are infeasible in reality.
        """
        if init_conditions is None:
            init_conditions = {}
        if engine is None:
            engine = get_current_engine()

        self.states: dict[str, VarType] = {
            "w": init_conditions["w"]
            if "w" in init_conditions
            else engine.var(f"w_{self.name}")
        }
        self.actions: dict[str, VarType] = {
            "r": init_conditions["r"]
            if "r" in init_conditions
            else engine.var(f"r_{self.name}")
        }
        self.disturbances: dict[str, VarType] = {
            "d": init_conditions["d"]
            if "d" in init_conditions
            else engine.var(f"d_{self.name}")
        }

        if positive_init_queue:
            self.states["w"] = engine.max(0, self.states["w"])

    def step_dynamics(
        self,
        net: "Network",
        T: Union[VarType, float],
        engine: Optional[EngineBase] = None,
        positive_next_queue: bool = False,
        **kwargs,
    ) -> dict[str, VarType]:
        """Steps the dynamics of this origin.

        Parameters
        ----------
        net : Network
            The network the origin belongs to.
        T : variable or float
            Sampling time.
        engine : EngineBase, optional
            The engine to be used. If `None`, the current engine is used.
        positive_next_queue : bool, optional
            If `True`, forces the queue at the next time step to be positive, e.g., as
            `w+ = max(0, w+)`. METANET is in fact known to sometime yield negative
            quantities, which are infeasible in reality.

        Returns
        -------
        Dict[str, variable]
            A dict with the states of the origin (queue) at the next time step.
        """
        if engine is None:
            engine = get_current_engine()

        q = self.get_flow(net, T, engine, **kwargs)
        w_next = engine.origins.step_queue(
            self.states["w"], self.disturbances["d"], q, T
        )

        if positive_next_queue:
            w_next = engine.max(0, w_next)
        return {"w": w_next}

    def get_flow(  # type: ignore[override]
        self,
        net: "Network",
        T: Union[VarType, float],
        engine: Optional[EngineBase] = None,
        **_,
    ) -> VarType:
        """Computes the (upstream) flow induced by the metered ramp.

        Parameters
        ----------
        net : Network
            The network this destination belongs to.
        T : variable or float
            Sampling time of the simulation.
        engine : EngineBase, optional
            The engine to be used. If `None`, the current engine is used.

        Returns
        -------
        variable
            The origin's upstream flow.
        """
        if engine is None:
            engine = get_current_engine()
        link_down = self._get_exiting_link(net)
        return engine.origins.get_ramp_flow(
            self.disturbances["d"],
            self.states["w"],
            self.C,
            self.actions["r"],
            link_down.rho_max,
            link_down.states["rho"][0],
            link_down.rho_crit,
            T,
            self.flow_eq_type,
        )


class SimplifiedMeteredOnRamp(MeteredOnRamp[VarType]):
    """A simplified version of the vanilla on-ramp, where the flow of vehicles on the
    ramp is the direct control action (instead of controlling the metering rate that in
    turns dictates the car flow on the ramp).

    See `MeteredOnRamp` for the original version."""

    _actions = {"q"}

    def __init__(
        self,
        capacity: Union[VarType, float],
        flow_eq_type: Literal["limited", "unlimited"] = "limited",
        name: Optional[str] = None,
    ) -> None:
        """Instantiates a simplified on-ramp with the given capacity.

        Parameters
        ----------
        capacity : float or variable
            Capacity of the on-ramp, i.e., `C`.
        flow_eq_type : 'limited' or 'unlimited', optional
            Type of flow equation for the ramp. See
            `engine.origins.get_simplifiedramp_flow` for more details.
        name : str, optional
            Name of the on-ramp, by default None.
        """
        super().__init__(capacity, flow_eq_type, name)  # type: ignore[arg-type]

    def init_vars(
        self,
        init_conditions: Optional[dict[str, VarType]] = None,
        engine: Optional[EngineBase] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initializes as control action the flow `q` on the ramp instead of the
        metering rate `r`."""
        if init_conditions is None:
            init_conditions = {}
        if engine is None:
            engine = get_current_engine()

        super().init_vars(init_conditions, engine, *args, **kwargs)

        del self.actions["r"]
        self.actions["q"] = (
            init_conditions["q"]
            if "q" in init_conditions
            else engine.var(f"q_{self.name}")
        )

    def get_flow(  # type: ignore[override]
        self,
        net: "Network",
        T: Union[VarType, float],
        engine: Optional[EngineBase] = None,
        **_,
    ) -> VarType:
        """Computes the (upstream) flow induced by the simple-metered ramp.

        Returns
        -------
        variable
            The origin's upstream flow.
        """
        if engine is None:
            engine = get_current_engine()
        link_down = self._get_exiting_link(net)
        return engine.origins.get_simplifiedramp_flow(
            self.actions["q"],
            self.disturbances["d"],
            self.states["w"],
            self.C,
            link_down.rho_max,
            link_down.states["rho"][0],
            link_down.rho_crit,
            T,
            self.flow_eq_type,  # type: ignore[arg-type]
        )
