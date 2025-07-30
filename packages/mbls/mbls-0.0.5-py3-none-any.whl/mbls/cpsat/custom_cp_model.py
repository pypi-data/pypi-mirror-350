from typing import Optional

from google.protobuf.internal.containers import RepeatedCompositeFieldContainer
from ortools.sat.cp_model_pb2 import ConstraintProto, CpSolverStatus
from ortools.sat.python.cp_model import CpModel, CpSolver, IntVar

from .. import ElapsedTimer
from .solution_progress_logger import SolutionProgressLogger
from .status import CpSatStatus


class CustomCpModel(CpModel):
    """A custom CpModel class that extends the ortools CpModel class."""

    solver: CpSolver
    """CpSolver object for solving the model."""
    sol_prog_logger: SolutionProgressLogger
    """(Optional) Logger for solution progress."""

    num_base_constraints: int
    """Number of base constraints in the model."""

    def __init__(self):
        super().__init__()
        self.num_base_constraints = 0

    def solve_and_get_status(
        self, computational_time: float, n_threads: int
    ) -> tuple[CpSolverStatus, float, float, float]:
        """Solve the CP model with the specified computational time and number of threads.

        Args:
            computational_time (float): The maximum computational time in seconds.
            n_threads (int): The number of threads to use for solving.

        Returns:
            tuple[CpSolverStatus, float, float, float]: A tuple containing
            - the solver status,
            - elapsed time,
            - the upper bound of the objective function, and
            - the lower bound of the objective function.
        """  # noqa: E501
        self.init_solver(computational_time, n_threads)

        solver_status = self.solver.solve(self)
        elapsed_time = self.solver.wall_time

        if CpSatStatus.found_feasible_solution(solver_status):
            ub = self.solver.objective_value
            lb = self.solver.best_objective_bound
        else:
            ub, lb = CpSatStatus.get_obj_value_and_bound_for_infeasible(
                self.is_maximize()
            )

        return solver_status, elapsed_time, ub, lb

    def init_solver(self, computational_time: float, n_threads: int) -> None:
        """Initializes the solver with the given computational time and number of threads.

        Args:
            computational_time (float): The maximum computational time in seconds.
            n_threads (int): The number of threads to use for solving.
        """  # noqa: E501
        self.solver = CpSolver()
        self.solver.parameters.max_time_in_seconds = computational_time
        self.solver.parameters.num_workers = n_threads

    def solve_with_prog_logger(
        self,
        computational_time: float,
        n_threads: int,
        timer: Optional[ElapsedTimer] = None,
    ) -> tuple[str, float, float, float]:
        """Solve the CP model with a solution progress logger.

        Args:
            computational_time (float): The maximum computational time in seconds.
            n_threads (int): The number of threads to use for solving.
            timer (Optional[ElapsedTimer], optional): Timer to be passed to solver callback. Defaults to None.

        Returns:
            tuple[str, float, float, float]: A tuple containing
            - the solver status as a string defined in SolverStatus,
            - elapsed time in seconds,
            - the upper bound of the objective function, and
            - the lower bound of the objective function.
        """  # noqa: E501
        self.init_solver(computational_time, n_threads)
        self.sol_prog_logger = SolutionProgressLogger(
            timer, print_on_solution_callback=True
        )

        solver_status = self.solver.solve(self, solution_callback=self.sol_prog_logger)
        elapsed_time = self.solver.wall_time

        if CpSatStatus.found_feasible_solution(solver_status):
            obj_value = self.solver.objective_value
            obj_bound = self.solver.best_objective_bound
        else:
            obj_value, obj_bound = CpSatStatus.get_obj_value_and_bound_for_infeasible(
                self.is_maximize()
            )

        return (
            CpSatStatus.get_status_string(solver_status),
            elapsed_time,
            obj_value,
            obj_bound,
        )

    # variable functions

    def change_domain(self, var: IntVar, domain: list[int]) -> None:
        """Changes the domain of a variable.

        Args:
            var (IntVar)
            domain (list[int]): A list of two integers representing the new domain.
        """
        assert len(domain) == 2, (
            f"Domain must be a list of two integers; {domain} given."
        )

        var.Proto().domain[:] = domain

    # objective functions

    def is_maximize(self) -> bool:
        """
        Returns:
            bool: True if the objective is maximize, False if minimize.
        """
        # TODO: find a way better than "self._CpModel__model.objective"
        if not hasattr(self._CpModel__model.objective, "maximize"):
            raise RuntimeError("Objective function has not been set.")
        return self._CpModel__model.objective.maximize

    # constraint functions

    def _get_constraints(self) -> RepeatedCompositeFieldContainer[ConstraintProto]:
        # TODO: find a way better than "self._CpModel__model.constraints"
        return self._CpModel__model.constraints

    def get_next_constr_idx(self) -> int:
        """Returns the index of the next constraint.

        Returns:
            int: The index of the next constraint.
        """
        return len(self._get_constraints())

    def freeze_base_constraints(self) -> None:
        """Sets the base number of constraints to the current number of constraints."""
        self.num_base_constraints = self.get_next_constr_idx()

    # methods to delete constraints

    def delete_constraints(self, idx_start: int, idx_end: int) -> None:
        del self._get_constraints()[idx_start:idx_end]

    def delete_added_constraints(self):
        """Deletes all constraints added after base model was built.

        Raises:
            ValueError: If no constraints were added after the base model was built.
        """

        if self.num_base_constraints == 0:
            raise ValueError("No base model constraints defined.")
        current_num_constraints = self.get_next_constr_idx()
        if current_num_constraints > self.num_base_constraints:
            self.delete_constraints(self.num_base_constraints, current_num_constraints)
