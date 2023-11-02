import gradio as gr
import pandas as pd
import json

data = None
index_pregunta = 0
scores1 = []
scores2 = []
winners = []

def evaluate(file, score1, score2, winner):
    global data, index_pregunta, scores1, scores2, winners

    # Cargamos el archivo CSV solo una vez
    if data is None:
        data = pd.read_csv(file.name)

    # Guardamos las calificaciones y el ganador
    scores1.append(score1)
    scores2.append(score2)
    if winner == "Option 1":
        winners.append(1)
    else:
        winners.append(2)
    #creamos un boton para que el usuario pueda pasar a la siguiente pregunta
    # Si aún hay más preguntas por responder
    if index_pregunta < len(data) - 1:
        index_pregunta += 1
        pregunta = data.iloc[index_pregunta]['question']
        option1 = data.iloc[index_pregunta]['answer1']
        option2 = data.iloc[index_pregunta]['answer2']

        return pregunta, option1, option2, 50, 50, ""  # Valores por defecto

    else:
        # Si ya respondió todas las preguntas
        df = pd.DataFrame()
        df["scores1"] = scores1
        df["scores2"] = scores2
        df["winner"] = winners

        # Puedes agregar aquí más lógica si quieres mostrar algo al final
        return "Gracias por completar la evaluación", "", "", 50, 50, ""

iface = gr.Interface(
    evaluate, 
    [
        "file", 
        gr.inputs.Slider(0, 100, default=50, label="Score 1"),
        gr.inputs.Slider(0, 100, default=50, label="Score 2"),
        gr.inputs.Radio(["Option 1", "Option 2"], label="Choose the winner")
    ], 
    [
        gr.outputs.Textbox(label="Question"),
        gr.outputs.Textbox(label="Option 1"),
        gr.outputs.Textbox(label="Option 2"),
        gr.outputs.Textbox(label="Default Score 1"),
        gr.outputs.Textbox(label="Default Score 2"),
        gr.outputs.Textbox(label="Message"),
    ],
    live=True
)

iface.launch()
