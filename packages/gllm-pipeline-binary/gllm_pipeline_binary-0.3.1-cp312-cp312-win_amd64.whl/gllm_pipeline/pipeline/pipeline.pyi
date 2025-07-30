from _typeshed import Incomplete
from gllm_datastore.cache.cache import BaseCache as BaseCache
from gllm_pipeline.pipeline.states import RAGState as RAGState
from gllm_pipeline.steps.pipeline_step import BasePipelineStep as BasePipelineStep
from gllm_pipeline.steps.terminator_step import TerminatorStep as TerminatorStep
from gllm_pipeline.utils.mermaid import MERMAID_HEADER as MERMAID_HEADER, combine_mermaid_diagrams as combine_mermaid_diagrams, extract_step_diagrams as extract_step_diagrams
from langgraph.graph import StateGraph
from typing import Any

INDENTATION: str

class Pipeline:
    '''Represents a sequence of steps executed in order, forming a pipeline.

    Attributes:
        steps (list[BasePipelineStep]): List of steps to be executed in the pipeline.
        state_type (type): The type of state used in the pipeline. Defaults to RAGState.
        recursion_limit (int): The maximum number of steps allowed.
        name (str | None): A name for this pipeline. Used when this pipeline is included as a subgraph.
            Defaults to None, in which case the name will be "Subgraph" followed by a unique identifier.
    '''
    steps: Incomplete
    recursion_limit: Incomplete
    name: Incomplete
    def __init__(self, steps: list[BasePipelineStep], state_type: type = ..., recursion_limit: int = 30, name: str | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None) -> None:
        '''Initializes the Pipeline with the given steps and state type.

        Args:
            steps (list[BasePipelineStep]): The steps to be executed in the pipeline.
            state_type (type, optional): The type of state to be used. Defaults to RAGState.
            recursion_limit (int, optional): The maximum number of steps allowed. Defaults to 30.
            name (str | None, optional): A name for this pipeline. Used when this pipeline is included as a subgraph.
                Defaults to None, in which case the name will be "Subgraph" followed by a unique identifier.
            cache_store (BaseCache | None, optional): The cache store to use for caching pipeline results.
                Defaults to None. If None, no caching will be used.
            cache_config (dict[str, Any] | None, optional): Configuration for the cache store.
                1. key_func: A function to generate cache keys. If None, the cache instance will use its own key
                    function.
                2. name: The name of the cache. If None, the cache instance will use its own key function.
                3. ttl: The time-to-live for the cache. If None, the cache will not have a TTL.
                4. matching_strategy: The strategy for matching cache keys.
                    If None, the cache instance will use "exact".
                5. matching_config: Configuration for the matching strategy.
                    If None, the cache instance will use its own default matching strategy configuration.

        Raises:
            ValueError: If the pipeline has no steps.
        '''
    @property
    def state_type(self) -> type:
        """The current state type of the pipeline.

        Returns:
            type: The current state type.
        """
    @state_type.setter
    def state_type(self, new_state_type: type) -> None:
        """Sets a new state type for the pipeline.

        Args:
            new_state_type (type): The new state type to set.

        Note:
            This operation will rebuild the pipeline graph if it has already been initialized, which can be
            computationally expensive for complex pipelines.
            It is recommended to set the state type before building the pipeline graph.
        """
    @property
    def graph(self) -> StateGraph:
        """The graph representation of the pipeline.

        If the graph doesn't exist yet, it will be built automatically.

        Returns:
            StateGraph: The graph representation of the pipeline.
        """
    def get_mermaid_diagram(self) -> str:
        """Generate a Mermaid diagram representation of the pipeline.

        Returns:
            str: The complete Mermaid diagram representation.
        """
    def build_graph(self) -> None:
        """Builds the graph representation of the pipeline by connecting the steps."""
    async def invoke(self, initial_state: dict[str, Any], config: dict[str, Any] | None = None) -> dict[str, Any]:
        '''Runs the pipeline asynchronously with the given initial state and configuration.

        Args:
            initial_state (dict[str, Any]): The initial state to start the pipeline with.
            config (dict[str, Any], optional): Additional configuration for the pipeline. User-defined config should not
                have "langraph_" prefix as it should be reserved for internal use. Defaults to None.

        Returns:
            dict[str, Any]: The final state after the pipeline execution.
                If \'debug_state\' is set to True in the config, the state logs will be included
                in the final state with the key \'__state_logs__\'.

        Raises:
            RuntimeError: If an error occurs during pipeline execution.
        '''
    def __or__(self, other: Pipeline | BasePipelineStep) -> Pipeline:
        """Combines the current pipeline with another pipeline or step using the '|' operator.

        When combining two pipelines, the state types must match.

        Args:
            other (Pipeline | BasePipelineStep): The other pipeline or step to combine with.

        Returns:
            Pipeline: A new pipeline consisting of the combined steps.

        Raises:
            ValueError: If the state types of the pipelines do not match.
        """
    def __lshift__(self, other: Pipeline | BasePipelineStep) -> Pipeline:
        """Includes another pipeline or step using the '<<' operator.

        This allows for easy composition where:
        - If 'other' is a Pipeline: it becomes a subgraph within this pipeline
        - If 'other' is a BasePipelineStep: it's added directly to this pipeline's steps

        The syntax `pipeline1 << pipeline2` visually indicates pipeline2 being inserted into pipeline1.
        The syntax `pipeline << step` adds the step to the pipeline.

        Args:
            other (Pipeline | BasePipelineStep): The pipeline to include as a subgraph or step to add.

        Returns:
            Pipeline: A new pipeline with the other pipeline included as a subgraph step or with the step added.
        """
    def __rshift__(self, other: Pipeline | BasePipelineStep) -> Pipeline:
        """Includes this pipeline as a subgraph in another context using the '>>' operator.

        This allows for easy composition where:
        - If 'other' is a Pipeline: this pipeline becomes a subgraph within the other pipeline
        - If 'other' is a BasePipelineStep: a new pipeline is created with the step, and this pipeline
          is included as a subgraph within that pipeline

        The syntax `pipeline1 >> pipeline2` embeds pipeline1 as a subgraph within pipeline2
        (equivalent to pipeline2 << pipeline1).
        The syntax `pipeline >> step` creates a new pipeline with the step, and includes this pipeline
        as a subgraph within that pipeline.

        Args:
            other (Pipeline | BasePipelineStep): The pipeline to include this pipeline in as a subgraph,
                or a step to create a new pipeline with.

        Returns:
            Pipeline: A new pipeline with this pipeline included as a subgraph.
        """
