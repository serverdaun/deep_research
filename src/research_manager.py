import asyncio

from agents import Runner, gen_trace_id, trace

from clarifier import ClarifyingQuestions, clarifier_agent
from planner import WebSearchItem, WebSearchPlan, planner_agent
from report_generator import ReportData, writer_agent
from web_search import search_agent


class ResearchManager:

    async def run(self, query: str, clarifications: str | None = None):
        """Run the deep research process, yielding status updates and the final report.

        If *clarifications* are provided (the user's answers to the clarifying questions), we will use them to
        augment the planning and reporting stages. Otherwise this behaves exactly like the previous implementation.
        """
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            print("Starting research...")

            # Combine the original query with any clarification the user has supplied.
            if clarifications:
                combined_query = (
                    f"Original query: {query}\n\nUser clarifications:\n{clarifications}"
                )
            else:
                combined_query = query

            search_plan = await self.plan_searches(combined_query)
            yield "Searches planned, starting to search..."
            search_results = await self.perform_searches(search_plan)
            yield "Searches complete, writing report..."
            report = await self.write_report(combined_query, search_results)
            yield report.markdown_report

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """Plan the searches to perform for the query"""
        print("Planning searches...")
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """Perform the searches to perform for the query"""
        print("Searching...")
        num_completed = 0
        tasks = [
            asyncio.create_task(self.search(item)) for item in search_plan.searches
        ]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Searching... {num_completed}/{len(tasks)} completed")
        print("Finished searching")
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        """Perform a search for the query"""
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                search_agent,
                input,
            )
            return str(result.final_output)
        except Exception:
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """Write the report for the query"""
        print("Thinking about report...")
        input = f"{query}\nSummarized search results: {search_results}"
        result = await Runner.run(
            writer_agent,
            input,
        )

        print("Finished writing report")
        return result.final_output_as(ReportData)

    async def get_clarifying_questions(self, query: str) -> list[str]:
        """Generate clarifying questions for a given query."""
        print("Generating clarifying questions...")
        result = await Runner.run(clarifier_agent, f"Query: {query}")
        questions_model: ClarifyingQuestions = result.final_output_as(
            ClarifyingQuestions
        )
        print(f"Generated {len(questions_model.questions)} clarifying questions")
        return questions_model.questions
