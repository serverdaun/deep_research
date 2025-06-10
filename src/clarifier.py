from agents import Agent
from pydantic import BaseModel, Field

INSTRUCTIONS = (
    "You are a domain expert who wants to fully understand the research intent behind a user's high-level query. "
    "Return a concise list (max 3) of the most important clarifying questions you would ask the user to narrow the scope "
    "and make the subsequent research more targeted and useful. Output only the questions - no additional commentary."
)


class ClarifyingQuestions(BaseModel):
    """A list of clarifying questions to present to the user before starting the research."""

    questions: list[str] = Field(
        description="The clarifying questions that should be asked of the user before planning the research."
    )


clarifier_agent = Agent(
    name="ClarifierAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ClarifyingQuestions,
)
