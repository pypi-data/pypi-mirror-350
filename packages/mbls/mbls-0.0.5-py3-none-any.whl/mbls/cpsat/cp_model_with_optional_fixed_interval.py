from typing import Hashable

from ortools.sat.python.cp_model import IntVar

from .cp_model_with_fixed_interval import CpModelWithFixedInterval


class CpModelWithOptionalFixedInterval(CpModelWithFixedInterval):
    # Variables

    var_op_is_present: dict[Hashable, IntVar]
    """
    Dictionary to store presence indicator variables for each operation in a job.
    """

    var_op_intvl_opt_fixed_name_set: set[str]
    """
    Set to store names of optional fixed interval variables.
    """

    def __init__(self, horizon: int):
        """Initialize the CpModelWithOptionalFixedInterval class.

        Args:
            horizon (int): The horizon for the scheduling problem,
                           which is the maximum time that any operation can end.
        """
        super().__init__(horizon)

        # Parameter
        self.horizon = horizon

        # Initialize dictionaries to store variables
        self.var_op_is_present = {}

        # Initialize the set to store interval variable names
        self.var_op_intvl_opt_fixed_name_set = set()

    def define_optional_fixed_interval_var(
        self, job_idx: str, stage_idx: str, mc_idx: str, processing_time: int
    ):
        """Define an optional interval variable with fixed processing time
        for an operation.

        Args:
            job_idx (str): The index of the job.
            stage_idx (str): The index of the stage.
            mc_idx (str): The index of the machine.
            processing_time (int): The processing time of the operation.
        """
        # method var_optional_casts on line 184 in constraint_program_model.py
        suffix = f"{job_idx}_{stage_idx}_{mc_idx}"
        var_intvl_name = f"intvl_opt_fixed_{suffix}"
        # Check if the interval variable name already exists
        if var_intvl_name in self.var_op_intvl_opt_fixed_name_set:
            raise ValueError(
                f"Interval variable name '{var_intvl_name}' already exists."
            )

        # Create an optional interval variable with the specified processing time
        start_var = self.new_int_var(0, self.horizon, f"start_{suffix}")
        end_var = self.new_int_var(0, self.horizon, f"end_{suffix}")
        is_present_var = self.new_bool_var(f"is_present_{suffix}")
        intvl_var = self.new_optional_interval_var(
            start_var, processing_time, end_var, is_present_var, var_intvl_name
        )

        # Add each variable to the corresponding dictionaries
        self.var_op_start[job_idx, stage_idx, mc_idx] = start_var
        self.var_op_end[job_idx, stage_idx, mc_idx] = end_var
        self.var_op_is_present[job_idx, stage_idx, mc_idx] = is_present_var
        self.var_op_intvl[job_idx, stage_idx, mc_idx] = intvl_var

        # Add name of the new variable to the set
        self.var_op_intvl_opt_fixed_name_set.add(var_intvl_name)
