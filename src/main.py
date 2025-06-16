import gradio as gr
from dotenv import load_dotenv

from research_manager import ResearchManager

load_dotenv()

WELCOME_MESSAGE = (
    "Welcome to **Deep Research**!\n"
    "Send me a research topic and I will ask clarifying questions.\n"
    "Answer them here to receive a detailed report."
)


def _format_clarifications(questions: list[str]) -> str:
    return "\n".join(f"{idx + 1}. {q}" for idx, q in enumerate(questions))


def _build_clarification_block(questions: list[str], answers: str) -> str:
    lines = [line.strip() for line in answers.split("\n")]
    while len(lines) < len(questions):
        lines.append("")
    return "\n".join(
        f"Q{idx + 1}: {q}\nA{idx + 1}: {lines[idx]}" for idx, q in enumerate(questions)
    )


async def respond(
    message: str, history: list[tuple[str | None, str | None]], state: dict
):
    if not state:
        state = {"stage": "awaiting_query", "query": "", "questions": []}

    history.append((message, None))

    if state["stage"] == "awaiting_query":
        state["query"] = message
        manager = ResearchManager()
        questions = await manager.get_clarifying_questions(message)
        state["questions"] = questions
        if questions:
            state["stage"] = "awaiting_answers"
            q_text = _format_clarifications(questions)
            history.append(
                (
                    None,
                    f"Please answer the following questions, one per line:\n{q_text}",
                )
            )
            yield history, state
        else:
            state["stage"] = "running"
            history.append((None, ""))
            async for chunk in manager.run(message, ""):
                history[-1] = (None, (history[-1][1] or "") + chunk)
                yield history, state
            state["stage"] = "awaiting_query"
            yield history, state
    elif state["stage"] == "awaiting_answers":
        answers_block = _build_clarification_block(state["questions"], message)
        manager = ResearchManager()
        state["stage"] = "running"
        history.append((None, ""))
        async for chunk in manager.run(state["query"], answers_block):
            history[-1] = (None, (history[-1][1] or "") + chunk)
            yield history, state
        state["stage"] = "awaiting_query"
        yield history, state
    else:
        history.append((None, "Please wait for the current task to finish."))
        yield history, state


def reset():
    return [(None, WELCOME_MESSAGE)], {
        "stage": "awaiting_query",
        "query": "",
        "questions": [],
    }


with gr.Blocks(theme=gr.themes.Default(primary_hue="yellow")) as ui:
    chatbot = gr.Chatbot()
    state = gr.State({})
    msg = gr.Textbox(placeholder="Type your message and press Enter")

    ui.load(fn=reset, outputs=[chatbot, state])
    msg.submit(respond, inputs=[msg, chatbot, state], outputs=[chatbot, state])

if __name__ == "__main__":
    ui.launch()
