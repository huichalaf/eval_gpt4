import streamlit as st
import pandas as pd
import sys

st.title('Human eval of LLMs')

uploaded_file = st.file_uploader("Upload your CSV", type="csv")
scores1 = []
scores2 = []
winners = []
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    # Inicializar sesión para rastrear la pregunta actual
    if 'index_pregunta' not in st.session_state:
        st.session_state.index_pregunta = 0

    # Mostrar pregunta actual
    try:
        pregunta = data.iloc[st.session_state.index_pregunta]['question']

        st.write(f"Pregunta: {pregunta}")

        # Mostrar opciones
        opcion1 = data.iloc[st.session_state.index_pregunta]['answer1']
        opcion2 = data.iloc[st.session_state.index_pregunta]['answer2']

        st.write(f"Option 1: {opcion1}")
        puntaje1 = st.slider("Score 1", 0, 100, 1)

        st.write(f"Option 2: {opcion2}")
        puntaje2 = st.slider("Score 2", 0, 100, 1)

        opcion_ganadora = st.radio("Choose the winner:", ["Option 1", "Option 2"])

        # Guardar puntajes y opción ganadora
        scores1.append(puntaje1)
        scores2.append(puntaje2)
        if opcion_ganadora == "Option 1":
            winners.append(1)
        else:
            winners.append(2)
        if st.button("Next"):
            # Aquí podrías guardar los puntajes y la opción ganadora en una base de datos o archivo.
            st.session_state.index_pregunta += 1
            # Si ya no hay más preguntas, reiniciar el índice.
            if st.session_state.index_pregunta >= len(data):
                st.session_state.index_pregunta = 0
                st.write("¡Eval completed, thank you!")
    except IndexError:
        st.write("¡Eval completed, thank you!")
        df = pd.DataFrame()
        df["scores1"] = scores1
        df["scores2"] = scores2
        df["winner"] = winners
        df.to_csv("human_eval_results.csv")
        #mostramos resultados
        st.write("Results:")
        st.write("Score 1:")
        st.write(scores1)
        st.write("Score 2:")
        st.write(scores2)
        #average
        st.write("Average score 1:")
        st.write(sum(scores1)/len(scores1))
        st.write("Average score 2:")
        st.write(sum(scores2)/len(scores2))
        #std
        st.write("Std score 1:")
        st.write(df["scores1"].std())
        st.write("Std score 2:")
        st.write(df["scores2"].std())
        #median
        st.write("Median score 1:")
        st.write(df["scores1"].median())
        st.write("Median score 2:")
        st.write(df["scores2"].median())
        st.write("Winner:")
        st.write(winners)
        #opcion ganadora mas veces
        st.write("Winner most times:")
        st.write(max(set(winners), key=winners.count))

    except Exception as e:
        st.write("An error ocurred: ", e)
else:
    st.write("Please upload a CSV file.")