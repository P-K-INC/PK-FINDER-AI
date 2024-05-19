import streamlit as st
import pandas as pd
import json
import time
from agent import query_agent, create_agent
caminho_imagem = "image/logo.png"
st.set_page_config(page_title='PKFinder', page_icon='http://localhost:8501/image/favicon.png', layout="centered", initial_sidebar_state="auto", menu_items=None)
def decode_response(response: str) -> dict:
    """This function converts the string response from the model to a dictionary object.

    Args:
        response (str): response from the model

    Returns:
        dict: dictionary with response data
    """
    return json.loads(response)

def write_response(response_dict: dict):
    """
    Write a response from an agent to a Streamlit app.

    Args:
        response_dict: The response from the agent.

    Returns:
        None.
    """

    # Check if the response is an answer.
    if "answer" in response_dict:
        return response_dict["answer"]

    # Check if the response is a bar chart.
    #  if "bar" in response_dict:
    #     data = response_dict["bar"]
    #    df = pd.DataFrame(data)
    #    df.set_index("columns", inplace=True)
    #   st.bar_chart(df)

    # Check if the response is a line chart.
    # if "line" in response_dict:
    #   data = response_dict["line"]
    #  df = pd.DataFrame(data)
    # df.set_index("columns", inplace=True)
    # st.line_chart(df)

    # Check if the response is a table.
    # if "table" in response_dict:
    #   data = response_dict["table"]
    #  df = pd.DataFrame(data["data"], columns=data["columns"])
    # st.table(df)

estilo_imagem = """
    <style>
        .imagem {
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
"""
# st.markdown(estilo_imagem, unsafe_allow_html=True)
# st.markdown("<div class='imagem'>", unsafe_allow_html=True)
st.image(caminho_imagem, use_column_width=True)
st.sidebar.image(caminho_imagem, use_column_width=True)
# st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align: center;'>Converse com seu CSV:</h1>", 
    unsafe_allow_html=True
)

st.sidebar.write("Faça upload do seu arquivo CSV abaixo.")
st.sidebar.write()
data = st.sidebar.file_uploader("Carregar um arquivo CSV", type=["csv"])

if "processed_data" not in st.session_state:
    st.session_state.processed_data = None

if data is not None:
    st.sidebar.info("CSV enviado com sucesso")

    if '.xlsx' in data.name:
        df = pd.read_excel(data)
    if '.csv' in data.name:
        df = pd.read_csv(data)

    data.seek(0, 0)
    st.dataframe(df, use_container_width=True)

    estilo_div = """
        <style>
            .box_response {
                border-radius: 10px;
                background-color: #172d43; 
                padding: 20px; 
                text-align: center; 
                color: white; 
                margin-bottom: 10px;
            }
        </style>
    """

    # Adiciona a div com o texto
    
    variavel_global = 'Pesquise Abaixo'
    text_space = st.empty()
    st.markdown(estilo_div, unsafe_allow_html=True)
    text_space.markdown("<div class='box_response'>{}</div>".format(variavel_global), unsafe_allow_html=True)
    input_text = st.text_area("Faça uma pergunta")

    if st.button("Enviar pergunta", type="primary"):
        with st.spinner("Pesquisando..."):
            # Create an agent from the CSV file.
            agent = create_agent(data)
            # Query the agent.
    
            response = query_agent(agent=agent, query=input_text)

            # # Decode the response.
            decoded_response = decode_response(response)
            estilo_div = """
                <style>
                    .box_response {
                        border-radius: 10px;
                        background-color: #76993d;
                        padding: 20px; 
                        text-align: center; 
                        color: white; 
                        margin-bottom: 10px;
                    }
                </style>
            """
            
            # Write the response to the Streamlit app.
            
            variavel_global = 'Resposta: ' + write_response(decoded_response)
            # variavel_global = 'Resposta: ' + 'ola'
            st.markdown(estilo_div, unsafe_allow_html=True)
            text_space.markdown("<div class='box_response'>{}</div>".format(variavel_global), unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Criado por P.K Inc</h4>", unsafe_allow_html=True)
        