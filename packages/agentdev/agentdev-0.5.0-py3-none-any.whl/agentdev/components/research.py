# -*- coding: utf-8 -*-
# flake8: noqa: E501

import asyncio
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from agentdev.base.component import Component
from agentdev.models.llm import BaseLLM
from agentdev.schemas.message_schemas import (
    SystemPromptMessage,
    UserPromptMessage,
)
from agentdev.utils.search_util import SearchAPI, select_and_execute_search

DEFAULT_REPORT_STRUCTURE = """Use this structure to create a report on the user-provided topic:

1. Introduction (no research needed)
   - Brief overview of the topic area

2. Main Body Sections:
   - Each section should focus on a sub-topic of the user-provided topic

3. Conclusion
   - Aim for 1 structural element (either a list of table) that distills the main body sections
   - Provide a concise summary of the report"""


class SearchQuery(BaseModel):
    search_query: str = Field(None, description="Query for web search.")


class Queries(BaseModel):
    queries: List[SearchQuery] = Field(
        description="List of search queries.",
    )


class Section(BaseModel):
    name: str = Field(
        description="Name for this section of the report.",
    )
    description: str = Field(
        description="Brief overview of the main topics and concepts to be covered in this section.",
    )
    research: bool = Field(
        description="Whether to perform web research for this section of the report.",
    )
    content: str = Field(description="The content of the section.")


class ResearchPlan(BaseModel):
    sections: List[Section] = Field(description="Sections of the report.")
    final_report: Optional[str] = Field(None, description="Final report.")


class ResearchPlanConfig(BaseModel):
    """
    Research Proposal Input.
    """

    topic: str = Field(..., description="Research topic")
    llm: BaseLLM = Field(..., description="LLM")
    feedback: str = Field(None, description="User feedback")
    report_structure: str = DEFAULT_REPORT_STRUCTURE
    number_of_queries: int = 3
    search_api: SearchAPI = SearchAPI.TAVILY
    search_api_config: Dict[str, Any] = {}


class ResearchTaskConfig(BaseModel):
    topic: str = Field(..., description="Research topic")
    llm: BaseLLM = Field(..., description="LLM")
    sections: List[Section] = Field(..., description="Sections of the report")
    max_iterations: int = 3  # Maximum number of reflection + search iterations
    max_searches_per_iteration: int = (
        3  # Maximum number of search queries per iteration
    )
    search_api: SearchAPI = SearchAPI.TAVILY
    search_api_config: Dict[str, Any] = {}


class Review(BaseModel):
    grade: Literal["pass", "fail"] = Field(
        description="Evaluation result indicating whether the response meets requirements ('pass') or needs revision ('fail').",
    )
    follow_up_queries: List[SearchQuery] = Field(
        description="List of follow-up search queries.",
    )


async def query_llm(
    llm: BaseLLM,
    sys_prompt: str,
    user_prompt: str,
    **kwargs: Any,
) -> BaseModel:
    extra_kwargs = {}
    if "response_model" in kwargs:
        extra_kwargs["response_model"] = kwargs["response_model"]
    result = await llm.arun(
        model=os.getenv("MODEL_NAME", "qwen-max"),
        messages=[
            SystemPromptMessage(content=sys_prompt),
            UserPromptMessage(content=user_prompt),
        ],
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        parameters={},
        **extra_kwargs,
    )
    return result


def format_sections(sections: list[Section]) -> str:
    """Format a list of sections into a string"""
    formatted_str = ""
    for idx, section in enumerate(sections, 1):
        formatted_str += f"""
{'='*60}
Section {idx}: {section.name}
{'='*60}
Description:
{section.description}
Requires Research:
{section.research}

Content:
{section.content if section.content else '[Not yet written]'}

"""
    return formatted_str


class ResearchPlanner(Component[ResearchPlanConfig, ResearchPlan]):
    """
    Research Proposal.
    """

    name = "research_proposal"
    description = "Research Proposal"

    async def _arun(
        self,
        args: ResearchPlanConfig,
        **kwargs: Any,
    ) -> ResearchPlan:
        topic = args.topic
        feedback = args.feedback
        structure = args.report_structure
        llm = args.llm

        # search the web for context
        queries_to_search = await query_llm(
            llm=llm,
            sys_prompt=self._search_context_sys_prompt(
                topic,
                structure,
                args.number_of_queries,
            ),
            user_prompt="Generate search queries in json format that will help with planning the sections of the report.",
            response_model=Queries,
        )

        query_list = [
            query.search_query for query in queries_to_search.queries
        ]
        context = await select_and_execute_search(
            args.search_api,
            query_list,
            args.search_api_config,
        )

        # generate the report proposal with context and optional feedback
        proposal = await query_llm(
            llm=llm,
            sys_prompt=self._generate_proposal_sys_prompt(
                topic,
                structure,
                context,
                feedback,
            ),
            user_prompt="Generate the sections of the report. Your response must include a 'sections' field containing a list of sections. Each section must have: name, description, plan, research, and content fields.",  # noqa E501
            response_model=ResearchPlan,
        )

        return proposal

    @staticmethod
    def _search_context_sys_prompt(
        topic: str,
        structure: str,
        number_of_queries: int,
    ) -> str:
        return f"""You are performing research for a report.

<Report topic>
{topic}
</Report topic>

<Report organization>
{structure}
</Report organization>

<Task>
Your goal is to generate {number_of_queries} web search queries that will help gather information for planning the report sections.

The queries should:

1. Be related to the Report topic
2. Help satisfy the requirements specified in the report organization

Make the queries specific enough to find high-quality, relevant sources while covering the breadth needed for the report structure.
</Task>

<Format>
Call the Queries tool
</Format>
"""

    @staticmethod
    def _generate_proposal_sys_prompt(
        topic: str,
        structure: str,
        context: str,
        feedback: str,
    ) -> str:
        return f"""I want a plan for a report that is concise and focused.

<Report topic>
The topic of the report is:
{topic}
</Report topic>

<Report organization>
The report should follow this organization:
{structure}
</Report organization>

<Context>
Here is context to use to plan the sections of the report:
{context}
</Context>

<Task>
Generate a list of sections for the report. Your plan should be tight and focused with NO overlapping sections or unnecessary filler.

For example, a good report structure might look like:
1/ intro
2/ overview of topic A
3/ overview of topic B
4/ comparison between A and B
5/ conclusion

Each section should have the fields:

- Name - Name for this section of the report.
- Description - Brief overview of the main topics covered in this section.
- Research - Whether to perform web research for this section of the report.
- Content - The content of the section, which you will leave blank for now.

Integration guidelines:
- Include examples and implementation details within main topic sections, not as separate sections
- Ensure each section has a distinct purpose with no content overlap
- Combine related concepts rather than separating them

Before submitting, review your structure to ensure it has no redundant sections and follows a logical flow.
</Task>

<Feedback>
Here is feedback on the report structure from review (if any):
{feedback}
</Feedback>

<Format>
Call the Sections tool
</Format>
"""


class ResearchIteration(BaseModel):
    """State for a single research iteration."""

    iteration_id: int
    queries: List[str] = Field(default_factory=list)
    search_results: str = ""
    content: str = ""
    review_grade: Optional[Literal["pass", "fail"]] = None
    follow_up_queries: Optional[List[SearchQuery]] = None

    class Config:
        json_encoders = {SearchQuery: lambda v: v.dict() if v else None}


class SectionState(BaseModel):
    """State for tracking research progress of a section."""

    iterations: List[ResearchIteration] = Field(default_factory=list)
    is_completed: bool = False
    current_iteration: int = 0

    def add_iteration(self) -> ResearchIteration:
        """Add a new iteration and return it."""
        _id = len(self.iterations)
        iteration = ResearchIteration(iteration_id=_id)
        self.iterations.append(iteration)
        self.current_iteration = _id
        return iteration

    def get_current_iteration(self) -> ResearchIteration:
        """Get the current iteration."""
        return self.iterations[self.current_iteration]

    def get_previous_iteration(self) -> ResearchIteration:
        """Get the previous iteration."""
        return self.iterations[self.current_iteration - 1]

    def save_to_file(self, filepath: str) -> None:
        """Save section state to a JSON file."""
        with open(filepath, "w") as f:
            json.dump(self.dict(), f, indent=2)

    @classmethod
    def load_from_file(cls, filepath: str) -> "SectionState":
        """Load section state from a JSON file."""
        with open(filepath, "r") as f:
            data = json.load(f)
        return cls(**data)


class ResearchActor(Component[ResearchTaskConfig, ResearchPlan]):
    """
    Research Actor.
    """

    name = "research_actor"
    description = "Research Actor"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.global_state: Dict[str, SectionState] = {}
        self.state_dir = "artifacts"  # Directory to store state files

    def _clean_state(self) -> None:
        """Clean the global state."""
        self.global_state = {}

    def _get_section_state(self, section_name: str) -> SectionState:
        """Get or create state for a section."""
        if section_name not in self.global_state:
            self.global_state[section_name] = SectionState()
        return self.global_state[section_name]

    def save_all_states(self) -> None:
        """Save all section states to disk in a single JSON file."""
        # Create state directory if it doesn't exist
        Path(self.state_dir).mkdir(parents=True, exist_ok=True)

        # Create a single file for all states
        filepath = os.path.join(self.state_dir, "research_states.json")

        try:
            # Convert global_state to serializable format
            serializable_state = {
                section_name: {
                    "iterations": [
                        {
                            "iteration_id": iter.iteration_id,
                            "queries": iter.queries,
                            "search_results": iter.search_results,
                            "content": iter.content,
                            "review_grade": iter.review_grade,
                            "follow_up_queries": iter.follow_up_queries,
                        }
                        for iter in state.iterations
                    ],
                    "is_completed": state.is_completed,
                    "current_iteration": state.current_iteration,
                }
                for section_name, state in self.global_state.items()
            }

            # Save to file with proper encoding for Chinese characters
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(serializable_state, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(
                f"Warning: Could not save global state to file {filepath}: {str(e)}",
            )

    async def _arun(
        self,
        args: ResearchTaskConfig,
        **kwargs: Any,
    ) -> ResearchPlan:
        """
        Process sections in parallel, performing research for sections where research=True.
        """
        print(f"\nStarting research process for topic: {args.topic}")
        self.llm = args.llm
        self.search_api = args.search_api
        self.search_params_to_pass = args.search_api_config

        # Start fresh
        self._clean_state()

        # Create tasks for sections that need research
        research_tasks = []
        for section in args.sections:
            if section.research:
                research_tasks.append(
                    self._research(
                        topic=args.topic,
                        section=section,
                        max_research_iterations=args.max_iterations,
                        max_searches_per_iteration=args.max_searches_per_iteration,
                        **kwargs,
                    ),
                )

        # Run research tasks in parallel
        completed_sections_as_context = ""
        if research_tasks:
            completed_sections = await asyncio.gather(*research_tasks)

            # Update the original sections with research results
            research_section_index = 0
            for i, section in enumerate(args.sections):
                if section.research:
                    args.sections[i] = completed_sections[
                        research_section_index
                    ]
                    research_section_index += 1

            completed_sections_as_context = format_sections(completed_sections)
            print("\nAll research tasks completed successfully!")

        non_research_tasks = []
        for section in args.sections:
            if not section.research:
                non_research_tasks.append(
                    self._non_research(
                        topic=args.topic,
                        section=section,
                        context=completed_sections_as_context,
                        **kwargs,
                    ),
                )
        # Run non research tasks in parallel
        if non_research_tasks:
            completed_sections = await asyncio.gather(*non_research_tasks)

            # Update the original sections with research results
            research_section_index = 0
            for i, section in enumerate(args.sections):
                if not section.research:
                    args.sections[i] = completed_sections[
                        research_section_index
                    ]
                    research_section_index += 1
            print("\nAll non-research tasks completed successfully!")

        # compile the report
        print("\nCompiling final report...")
        final_report = "\n\n".join(
            [section.content for section in args.sections],
        )

        # persist final report and states
        # todo: better artifact management
        os.makedirs(self.state_dir, exist_ok=True)
        safe_topic = "".join(c if c.isalnum() else "_" for c in args.topic)
        final_report_path = os.path.join(
            self.state_dir,
            f"final_report_for_{safe_topic}.md",
        )
        with open(final_report_path, "w") as f:
            f.write(final_report)
        self.save_all_states()
        print(
            f"\nResearch completed! Final report saved to: {final_report_path}",
        )

        return ResearchPlan(sections=args.sections, final_report=final_report)

    async def _research(
        self,
        topic: str,
        section: Section,
        max_research_iterations: int,
        max_searches_per_iteration: int,
    ) -> Section:
        """
        Perform research for a single section.

        Args:
            section: Section to research
            **kwargs: Additional arguments

        Returns:
            Section with updated content from research
        """
        print(f"\nStarting parallel research for section: {section.name}")
        section_state = self._get_section_state(section.name)
        fix_info = {
            "topic": topic,
            "section_name": section.name,
            "section_description": section.description,
        }

        for iter in range(max_research_iterations):
            print(
                f"\n -- Research iteration {iter + 1}/{max_research_iterations} for section: {section.name}",
            )
            # Start new iteration
            iteration = section_state.add_iteration()

            # Set search queries
            if iter == 0:
                search_queries = await self._generate_search_queries(
                    topic,
                    section.description,
                    max_searches_per_iteration,
                )
                query_list = [
                    query.search_query for query in search_queries.queries
                ]
            else:
                query_list = (
                    section_state.get_previous_iteration().follow_up_queries
                )

            # Execute searches and gather context
            search_results = await self._search(query_list)

            # Process the context
            writing_result = await self._write(
                additional_context=search_results,
                section_content=section.content,
                **fix_info,
            )

            # Review the section
            review = await self._review(
                section_content=writing_result,
                num_of_follow_up_queries=max_searches_per_iteration,
                **fix_info,
            )

            # Update section states
            iteration.queries = [
                q.search_query for q in search_queries.queries
            ]
            iteration.search_results = search_results
            iteration.content = writing_result
            section.content = writing_result
            iteration.review_grade = review.grade
            iteration.follow_up_queries = (
                [x.search_query for x in review.follow_up_queries]
                if hasattr(review, "follow_up_queries")
                else []
            )

            # early exit if the section is good enough
            if review.grade == "pass":
                print(
                    f"\n -- Section '{section.name}' passed review after iteration {iter + 1}",
                )
                break
            else:
                print(
                    f"\n -- Section '{section.name}' needs revision, generating follow-up queries...",
                )

        else:
            print(
                f"Section '{section.name}' completed research due to max iterations reached",
            )

        return section

    async def _non_research(
        self,
        topic: str,
        section: Section,
        context: str,
        **kwargs: Any,
    ) -> Section:
        """
        Write a non-research section.
        """
        print(f"Generating non-research section: {section.name}")
        sys_prompt = self._write_non_research_section_sys_prompt(
            topic,
            section.name,
            section.description,
            context,
        )
        usr_prompt = "Generate a report section based on the provided sources."

        section_content = await query_llm(
            llm=self.llm,
            sys_prompt=sys_prompt,
            user_prompt=usr_prompt,
        )

        section.content = section_content.choices[0].message.content

        return section

    async def _generate_search_queries(
        self,
        topic: str,
        section_description: str,
        number_of_queries: int,
    ) -> List[str]:
        """
        Generate search queries for a section.

        Args:
            section: Section to generate queries for

        Returns:
            List of search queries
        """

        sys_prompt = self._generate_section_search_queries_sys_prompt(
            topic,
            section_description,
            number_of_queries,
        )
        user_prompt = "Generate search queries on the provided topic."

        search_queries = await query_llm(
            llm=self.llm,
            sys_prompt=sys_prompt,
            user_prompt=user_prompt,
            response_model=Queries,
        )

        return search_queries

    async def _search(self, query_list: List[str]) -> str:
        """
        Execute search queries and gather context.

        Args:
            queries: List of search queries
            **kwargs: Additional arguments

        Returns:
            Combined context from searches
        """
        return await select_and_execute_search(
            self.search_api,
            query_list,
            self.search_params_to_pass,
        )

    async def _write(
        self,
        topic: str,
        section_name: str,
        section_description: str,
        section_content: str,
        additional_context: str,
    ) -> str:
        """
        Process search context and generate section content.

        Args:
            context: Search context
            section: Section to process

        Returns:
            Updated section content
        """

        additional_context_formatted = (
            self.write_section_additional_context_prompt(
                topic,
                section_name,
                section_description,
                section_content,
                additional_context,
            )
        )

        section_content = await query_llm(
            llm=self.llm,
            sys_prompt=self.write_section_sys_prompt(),
            user_prompt=additional_context_formatted,
        )
        return section_content.choices[0].message.content

    async def _review(
        self,
        topic: str,
        section_description: str,
        section_content: str,
        num_of_follow_up_queries: int,
        **kwargs: Any,
    ) -> str:
        review_sys_prompt = self._review_section_sys_prompt(
            topic,
            section_description,
            section_content,
            num_of_follow_up_queries,
        )
        review_user_prompt = (
            "Grade the report and consider follow-up questions for missing information. "
            "If the grade is 'pass', return empty strings for all follow-up queries. "
            "If the grade is 'fail', provide specific search queries to gather missing information."
        )

        review = await query_llm(
            llm=self.llm,
            sys_prompt=review_sys_prompt,
            user_prompt=review_user_prompt,
            response_model=Review,
        )
        return review

    @staticmethod
    def _generate_section_search_queries_sys_prompt(
        topic: str,
        section_description: str,
        number_of_queries: int,
    ) -> str:
        return f"""You are an expert technical writer crafting targeted web search queries that will gather comprehensive information for writing a technical report section.

<Report topic>
{topic}
</Report topic>

<Section topic>
{section_description}
</Section topic>

<Task>
Your goal is to generate at most {number_of_queries} search queries that will help gather comprehensive information above the section topic.

The queries should:

1. Be related to the topic
2. Examine different aspects of the topic

Make the queries specific enough to find high-quality, relevant sources.
</Task>

<Format>
Call the Queries tool
</Format>
"""

    @staticmethod
    def write_section_sys_prompt() -> str:
        return """Write one section of a research report.

<Task>
1. Review the report topic, section name, and section topic carefully.
2. If present, review any existing section content.
3. Then, look at the provided Source material.
4. Decide the sources that you will use it to write a report section.
5. Write the report section and list your sources.
</Task>

<Writing Guidelines>
- If existing section content is not populated, write from scratch
- If existing section content is populated, synthesize it with the source material
- Strict 150-200 word limit
- Use simple, clear language
- Use short paragraphs (2-3 sentences max)
- Use ## for section title (Markdown format)
</Writing Guidelines>

<Citation Rules>
- Assign each unique URL a single citation number in your text
- End with ### Sources that lists each source with corresponding numbers
- IMPORTANT: Number sources sequentially without gaps (1,2,3,4...) in the final list regardless of which sources you choose
- Example format:
  [1] Source Title: URL
  [2] Source Title: URL
</Citation Rules>

<Final Check>
1. Verify that EVERY claim is grounded in the provided Source material
2. Confirm each URL appears ONLY ONCE in the Source list
3. Verify that sources are numbered sequentially (1,2,3...) without any gaps
</Final Check>
"""

    @staticmethod
    def write_section_additional_context_prompt(
        topic: str,
        section_name: str,
        section_description: str,
        section_content: str,
        additional_context: str,
    ) -> str:
        return f"""
<Report topic>
{topic}
</Report topic>

<Section name>
{section_name}
</Section name>

<Section topic>
{section_description}
</Section topic>

<Existing section content (if populated)>
{section_content}
</Existing section content>

<Source material>
{additional_context}
</Source material>
"""

    @staticmethod
    def _review_section_sys_prompt(
        topic: str,
        section_description: str,
        section_content: str,
        num_of_follow_up_queries: int,
    ) -> str:
        return f"""Review a report section relative to the specified topic:

<Report topic>
{topic}
</Report topic>

<section topic>
{section_description}
</section topic>

<section content>
{section_content}
</section content>

<task>
Evaluate whether the section content adequately addresses the section topic.

If the section content does not adequately address the section topic, generate at most {num_of_follow_up_queries} follow-up search queries to gather missing information.
</task>

<format>
Call the Feedback tool and output with the following schema:

grade: Literal["pass","fail"] = Field(
    description="Evaluation result indicating whether the response meets requirements ('pass') or needs revision ('fail')."
)
follow_up_queries: List[SearchQuery] = Field(
    description="List of follow-up search queries.",
)
</format>
"""

    @staticmethod
    def _write_non_research_section_sys_prompt(
        topic: str,
        section_name: str,
        section_description: str,
        context: str,
    ) -> str:
        return f"""You are an expert technical writer crafting a section that synthesizes information from the rest of the report.

<Report topic>
{topic}
</Report topic>

<Section name>
{section_name}
</Section name>

<Section topic>
{section_description}
</Section topic>

<Available report content>
{context}
</Available report content>

<Task>
1. Section-Specific Approach:

For Introduction:
- Use # for report title (Markdown format)
- 50-100 word limit
- Write in simple and clear language
- Focus on the core motivation for the report in 1-2 paragraphs
- Use a clear narrative arc to introduce the report
- Include NO structural elements (no lists or tables)
- No sources section needed

For Conclusion/Summary:
- Use ## for section title (Markdown format)
- 100-150 word limit
- For comparative reports:
    * Must include a focused comparison table using Markdown table syntax
    * Table should distill insights from the report
    * Keep table entries clear and concise
- For non-comparative reports:
    * Only use ONE structural element IF it helps distill the points made in the report:
    * Either a focused table comparing items present in the report (using Markdown table syntax)
    * Or a short list using proper Markdown list syntax:
      - Use `*` or `-` for unordered lists
      - Use `1.` for ordered lists
      - Ensure proper indentation and spacing
- End with specific next steps or implications
- No sources section needed

3. Writing Approach:
- Use concrete details over general statements
- Make every word count
- Focus on your single most important point
</Task>

<Quality Checks>
- For introduction: 50-100 word limit, # for report title, no structural elements, no sources section
- For conclusion: 100-150 word limit, ## for section title, only ONE structural element at most, no sources section
- Markdown format
- Do not include word count or any preamble in your response
</Quality Checks>
"""
