import gradio as gr
from ai_core import ask_ai

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
        # 🛡️ TinyAI - Cybersecurity Assistant
        Built for SIEM | Wazuh | VAPT | Logs | Payloads
    """)
    with gr.Row():
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(label="💬 Chat", height=420, type="messages")
            msg = gr.Textbox(placeholder="Type your question...", show_label=False)
            clear = gr.Button("🧹 Clear")
        with gr.Column(scale=1):
            gr.Markdown("## Features\n- Chat Memory\n- User Intent\n- SIEM Log Understanding\n- Typing Animation\n- Internet Mode")

    def user_response(message, history):
        history = history or []
        for _, updated_history in ask_ai(message, history):
            yield "", updated_history

    msg.submit(fn=user_response, inputs=[msg, chatbot], outputs=[msg, chatbot], queue=True)
    clear.click(lambda: ("", []), outputs=[msg, chatbot])

demo.launch()