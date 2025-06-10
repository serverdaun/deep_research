import gradio as gr
from dotenv import load_dotenv

from research_manager import ResearchManager

load_dotenv()


async def ask_clarifications(query: str) -> tuple[str, list[str]]:
    """Generate clarifying questions for *query* and return both a nicely formatted string and the raw list."""
    manager = ResearchManager()
    questions = await manager.get_clarifying_questions(query)

    if not questions:
        return (
            "No clarifying questions were generated. You can proceed to run the research.",
            [],
        )

    formatted = "\n".join(f"{idx+1}. {q}" for idx, q in enumerate(questions))
    return formatted, questions


async def run_research(query: str, answers: str, questions: list[str]):
    """Run the complete research pipeline and stream the markdown report."""
    clarifications_block = ""

    answer_lines = [line.strip() for line in answers.split("\n")]
    while len(answer_lines) < len(questions):
        answer_lines.append("")

    q_and_a = []
    for idx, question in enumerate(questions):
        answer = answer_lines[idx]
        q_and_a.append(f"Q{idx+1}: {question}\nA{idx+1}: {answer}")

    clarifications_block = "\n".join(q_and_a)

    async for chunk in ResearchManager().run(query, clarifications_block):
        yield chunk


with gr.Blocks(theme=gr.themes.Default(primary_hue="yellow")) as ui:
    gr.Markdown("# Deep Research")

    with gr.Row():
        query_textbox = gr.Textbox(
            label="What topic would you like to research?",
            placeholder="e.g. How to create a Deep Research Agent?",
        )
        ask_button = gr.Button("Ask clarifying questions")

    clarifying_questions_state = gr.State([])
    clarifications_markdown = gr.Markdown(label="Clarifying questions will appear here")

    clarification_answers_box = gr.Textbox(
        label="Your answers to the clarifying questions (one per line)",
        placeholder="Answer 1\nAnswer 2\n...",
        lines=3,
    )

    run_button = gr.Button("Run research", variant="primary")
    report = gr.Markdown(label="Report")

    ask_button.click(
        fn=ask_clarifications,
        inputs=query_textbox,
        outputs=[clarifications_markdown, clarifying_questions_state],
    )

    run_button.click(
        fn=run_research,
        inputs=[query_textbox, clarification_answers_box, clarifying_questions_state],
        outputs=report,
    )

if __name__ == "__main__":
    ui.launch()
