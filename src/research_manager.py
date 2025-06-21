from agents import Runner, gen_trace_id, trace
from datetime import datetime

from clarifier import ClarifyingQuestions, clarifier_agent
from report_generator import ReportData
from research_agent import research_agent


class ResearchManager:

    async def run(self, query: str, clarifications: str | None = None):
        """Run the deep-research pipeline using `research_agent`."""
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            print("Starting research with ResearchAgent…")

            today = datetime.utcnow().date().isoformat()
            prefix = f"Current date: {today}\n"
            combined_query = prefix + (
                f"Original query: {query}\n\nUser clarifications:\n{clarifications}"
                if clarifications
                else query
            )
            yield "Research in progress…"

            result = await Runner.run(research_agent, combined_query)
            report: ReportData = result.final_output_as(ReportData)

            yield "Report generated. Rendering markdown…"
            yield report.markdown_report

    async def get_clarifying_questions(self, query: str) -> list[str]:
        """Generate clarifying questions for a given query."""
        print("Generating clarifying questions...")
        result = await Runner.run(clarifier_agent, f"Query: {query}")
        questions_model: ClarifyingQuestions = result.final_output_as(
            ClarifyingQuestions
        )
        print(f"Generated {len(questions_model.questions)} clarifying questions")
        return questions_model.questions
