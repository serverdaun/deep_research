from agents import Agent, ModelSettings

from planner import planner_agent
from report_generator import ReportData, writer_agent
from web_search import search_agent

INSTRUCTIONS = (
    "You are a senior research orchestrator tasked with answering complex user questions by calling the "
    "appropriate tools.  You have access to the following tools:\n\n"
    "1. planner_agent(input: str) -> WebSearchPlan - Produce up to five web-search queries that, when executed, "
    "will help address the user's request.\n"
    "3. search_agent(input: str) -> str - Run a single web search and return a concise summary of the results.\n"
    "4. writer_agent(input: str) -> ReportData - Synthesise the final markdown report.  This **must** be the last "
    "tool you call; treat its output as your final hand-off to the user.\n\n"
    "Workflow guidelines:\n"
    "> Think step-by-step and decide which tool to invoke next. \n"
    "> After gathering clarifications (if any), call planner_agent once to devise your search strategy.\n"
    "> Next, iterate through search_agent calls to collect evidence.  You may call search_agent multiple times to "
    "cover each planned search term.\n"
    "> If, after reviewing the results, you believe the information is still insufficient, you may make additional "
    "calls to planner_agent or search_agent.  LIMIT yourself to a maximum of **two** extra tool calls beyond your "
    "initial plan/execution.\n"
    "> Once satisfied, call writer_agent **exactly once** and return its markdown_report to the user as your final "
    "answer.\n"
    "> Never reveal chain-of-thought or internal reasoning.  Keep your responses concise and focused on using the "
    "tools effectively.\n\n"
    "Remember: you have at most two extra tool invocations if you are unhappy with the intermediate results.  Choose "
    "them wisely."
)

planner_tool = planner_agent.as_tool(
    tool_name="planner_agent",
    tool_description="Produce up to five web-search queries that, when executed, will help address the user's request.",
)
web_search_tool = search_agent.as_tool(
    tool_name="search_agent",
    tool_description="Run a single web search and return a concise summary of the results.",
)
writer_tool = writer_agent.as_tool(
    tool_name="writer_agent", tool_description="Synthesise the markdown report."
)
tools = [planner_tool, web_search_tool, writer_tool]

research_agent = Agent(
    name="Research Agent",
    instructions=INSTRUCTIONS,
    tools=tools,
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="auto"),
    output_type=ReportData,
)
