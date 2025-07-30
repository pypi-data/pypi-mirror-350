from _typeshed import Incomplete
from dataclasses import dataclass
from gllm_core.event.event_emitter import EventEmitter as EventEmitter
from gllm_core.schema import Component
from gllm_pipeline.steps.pipeline_step import BasePipelineStep as BasePipelineStep
from gllm_pipeline.steps.terminator_step import TerminatorStep as TerminatorStep
from gllm_pipeline.utils.has_inputs_mixin import HasInputsMixin as HasInputsMixin
from gllm_pipeline.utils.mermaid import MERMAID_HEADER as MERMAID_HEADER, combine_mermaid_diagrams as combine_mermaid_diagrams, extract_step_diagrams as extract_step_diagrams
from langchain_core.runnables import RunnableConfig as RunnableConfig
from langgraph.graph import StateGraph as StateGraph
from typing import Any, Callable

ConditionType = Component | Callable[[dict[str, Any]], str]
DEFAULT_BRANCH: str

@dataclass
class ConditionInputs:
    """Container for different types of inputs used in condition evaluation.

    Attributes:
        merged (dict[str, Any]): Complete merged dictionary containing all state, config, and fixed args.
            Used for Callable conditions.
        mapped (dict[str, Any]): Dictionary containing only explicitly mapped inputs.
            Used for Component conditions.
        event_emitter (EventEmitter | None): Event emitter instance for logging.
    """
    merged: dict[str, Any]
    mapped: dict[str, Any]
    event_emitter: EventEmitter | None

class ConditionalStep(BasePipelineStep, HasInputsMixin):
    '''A pipeline step that conditionally executes different branches based on specified conditions.

    This step evaluates one or more conditions and selects a branch to execute based on the result.
    It provides flexibility in defining complex conditional logic within a pipeline.

    A minimal usage requires defining the branches to execute based on a `condition`, which is a callable
    that takes input from the state and returns a string identifying the branch to execute.

    Example:
    ```python
    ConditionalStep(
        name="UseCaseSelection",
        branches={"A": step_a, DEFAULT_BRANCH: step_b},
        condition=lambda x: "A" if "<A>" in x["query"] else "__default__"
    )
    ```
    This will execute `step_a` if the query contains "<A>", and `step_b` otherwise.

    The special key `__default__` (importable as DEFAULT_BRANCH) defines the default branch to execute
    if no other condition matches. If the DEFAULT_BRANCH is not defined and no condition matches,
    the step will raise an error.

    Attributes:
        name (str): A unique identifier for this pipeline step.
        branches (dict[str, BasePipelineStep | list[BasePipelineStep]]): Mapping of condition results to steps.
        condition (list[ConditionType] | None): The condition(s) to evaluate for branch selection.
        input_state_map (dict[str, str]): Mapping of condition input arguments to pipeline state keys.
        output_state (str | None): Key to store the condition result in the state, if desired.
        condition_aggregator (Callable[[list[Any]], str]): Function to aggregate multiple condition results.
        runtime_config_map (dict[str, str]): Mapping of condition input arguments to runtime configuration keys.
        fixed_args (dict[str, Any]): Fixed arguments to be passed to the condition evaluation.
    '''
    branches: Incomplete
    condition: Incomplete
    output_state: Incomplete
    condition_aggregator: Incomplete
    def __init__(self, name: str, branches: dict[str, BasePipelineStep | list[BasePipelineStep]], condition: ConditionType | list[ConditionType] | None = None, input_state_map: dict[str, str] | None = None, output_state: str | None = None, condition_aggregator: Callable[[list[Any]], str] = ..., runtime_config_map: dict[str, str] | None = None, fixed_args: dict[str, Any] | None = None) -> None:
        '''Initializes a new ConditionalStep.

        Args:
            name (str): A unique identifier for this pipeline step.
            branches (dict[str, BasePipelineStep | list[BasePipelineStep]]): Mapping of condition results to
                steps to execute.
            condition (ConditionType | list[ConditionType], optional): The condition(s) to evaluate for branch
                selection. If None, condition is evaluated from the state. Defaults to None.
            input_state_map (dict[str, str] | None, optional): Mapping of condition input arguments to pipeline
                state keys. If None, no input is taken from the state. Defaults to None.
            output_state (str | None, optional): Key to store the condition result in the state.
                If None, the output is not saved in the state. Defaults to None.
            condition_aggregator (Callable[[list[Any]], str], optional): Function to aggregate multiple condition
                results. Defaults to joining results with a semicolon (";").
            runtime_config_map (dict[str, str] | None, optional): Mapping of condition input arguments to runtime
                configuration keys. Defaults to None.
            fixed_args (dict[str, Any] | None, optional): Fixed arguments to be passed to the condition.
                Defaults to None.
        '''
    def add_to_graph(self, graph: StateGraph, previous_endpoints: list[str]) -> list[str]:
        """Integrates this step into the pipeline's internal structure.

        This method is used by `Pipeline` to manage the pipeline's execution flow.
        It should not be called directly by users.

        This method always creates a condition node that:
        1. Executes the condition and stores its result if output_state is defined
        2. Acts as a pass-through router if no output_state is defined
        3. Connects to the appropriate branch based on condition evaluation

        Args:
            graph (StateGraph): The internal representation of the pipeline structure.
            previous_endpoints (list[str]): The endpoints from previous steps to connect to.

        Returns:
            list[str]: The exit points (endpoints) of all non-terminating branches.
        """
    async def select_path(self, state: dict[str, Any], config: RunnableConfig) -> str:
        '''Determines which branch to execute based on the evaluated condition(s).

        This method prepares input data, evaluates conditions, aggregates results, and determines the branch to follow.

        Args:
            state (dict[str, Any]): The current state of the pipeline, containing all data.
            config (RunnableConfig): Runtime configuration for this step\'s execution.

        Returns:
            str: The identifier of the selected branch. Returns "__default__" if an error occurs
                or if the condition result doesn\'t match any branch.
        '''
    def get_all_steps(self) -> list[BasePipelineStep]:
        """Gets all steps from all branches.

        Returns:
            list[BasePipelineStep]: A list of all steps in all branches.
        """
    async def execute(self, state: dict[str, Any], config: RunnableConfig) -> dict[str, Any] | None:
        """Executes the conditional step and optionally saves the routing result.

        This method evaluates the condition and saves it to the output_state if specified.
        The route selection is done fresh for each execution to avoid caching issues.

        Args:
            state (dict[str, Any]): The current state of the pipeline, containing all data.
            config (RunnableConfig): Runtime configuration for this step's execution.

        Returns:
            dict[str, Any] | None: The update to the pipeline state after this step's operation.
                If output_state is defined, includes the selected route.
                Otherwise, returns None.
        """
    def get_mermaid_diagram(self) -> str:
        """Create a Mermaid diagram representation of the conditional step.

        Returns:
            str: The complete Mermaid diagram representation of the conditional branches.
        """
