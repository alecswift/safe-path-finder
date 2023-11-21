import gradio as gr
from src.random_forests import predictor


demo = gr.Interface(
    fn=predictor,
    inputs=["text", "text", "text", "number", "number", "number", "number", "number"],
    outputs="number"
)

if __name__ == "__main__":
    demo.launch(show_api=False)
