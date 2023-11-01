import streamlit as st
import pandas as pd
import base64
import json

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{bin_file}">{file_label}</a>'
    return href

st.title('Human eval of LLMs')

uploaded_file = st.file_uploader("Upload your CSV", type="csv")
scores1 = []
scores2 = []
winners = []
latex_code = r"""
For \( \lambda_2 = 6 \): We need to solve the equation \( (A - I)\mathbf{x}_2 = \left(\begin{pmatrix} 4 & 1 \\ 2 & 3 \end{pmatrix} - 6\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}\right)\mathbf{x}_2 = \begin{pmatrix} -2 & 1 \\ 2 & -3 \end{pmatrix}\mathbf{x}_2 = 0 \) for vector \( \mathbf{x}_2 \).
"""

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    if 'index_pregunta' not in st.session_state:
        st.session_state.index_pregunta = 0
        st.experimental_rerun()


    if st.session_state.index_pregunta < len(data):
        try:
            pregunta = data.iloc[st.session_state.index_pregunta]['question']
            st.markdown("$$ A = \\begin{pmatrix} 4 & 1 \\\\ 2 & 3 \\end{pmatrix} $$")
            st.markdown(f"Pregunta: {pregunta}")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"Option 1: {data.iloc[st.session_state.index_pregunta]['answer1']}")
                puntaje1 = st.slider("Score 1", 0, 100, 1, key=f"p1_{st.session_state.index_pregunta}")
            with col2:
                st.markdown(f"Option 2: {data.iloc[st.session_state.index_pregunta]['answer2']}")
                puntaje2 = st.slider("Score 2", 0, 100, 1, key=f"p2_{st.session_state.index_pregunta}")

            opcion_ganadora = st.radio("Choose the winner:", ["Option 1", "Option 2"])
            scores1.append(puntaje1)
            scores2.append(puntaje2)
            if opcion_ganadora == "Option 1":
                winners.append(1)
            else:
                winners.append(2)

            if st.button("Next"):
                st.session_state.index_pregunta += 1

        except Exception as e:
            st.write("An error occurred:", e)

    else:
        st.write("¡Eval completed, thank you!")
        df = pd.DataFrame()
        df["scores1"] = scores1
        df["scores2"] = scores2
        df["winner"] = winners
        df.to_csv("human_eval_results.csv")

        st.write("Results:")
        st.write(df.describe())

        json_data = {}
        json_data["scores1_avg"] = sum(scores1)/len(scores1)
        json_data["scores2_avg"] = sum(scores2)/len(scores2)
        json_data["scores1_std"] = df["scores1"].std()
        json_data["scores2_std"] = df["scores2"].std()
        json_data["scores1_median"] = df["scores1"].median()
        json_data["scores2_median"] = df["scores2"].median()
        json_data["scores1_moda"] = df["scores1"].mode()[0]
        json_data["scores2_moda"] = df["scores2"].mode()[0]
        json_data["total_questions"] = len(scores1)
        json_data["winner"] = df["winner"].mode()[0]

        with open('results_human_eval.json', 'w') as f:
            json.dump(json_data, f)

        st.markdown(get_binary_file_downloader_html('results_human_eval.json', 'Download Results JSON'), unsafe_allow_html=True)
        st.markdown(get_binary_file_downloader_html('human_eval_results.csv', 'Download Results CSV'), unsafe_allow_html=True)

else:
    st.write("Please upload a CSV file.")
