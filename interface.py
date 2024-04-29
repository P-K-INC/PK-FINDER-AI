import streamlit as st
import pandas as pd
import json
from agent import query_agent, create_agent


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
        st.write(response_dict["answer"])

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


st.set_page_config(layout='wide')

st.title("Converse com seu CSV")
st.write("💼🚬Criado por PK INC💼🚬")

st.write("Faça upload do seu arquivo CSV abaixo.")

data = st.file_uploader("Carregar um CSV")

if "processed_data" not in st.session_state:
    st.session_state.processed_data = None

if data is not None:
    st.info("CSV Uploaded Successfully")
    df = pd.read_csv(data)
    data.seek(0, 0)
    st.dataframe(df, use_container_width=True)

    st.info("Chat aqui")

    input_text = st.text_area("Faça uma pergunta")

    if st.button("Submit Query", type="primary"):
        # Create an agent from the CSV file.
        agent = create_agent(data)

        # Query the agent.
        response = query_agent(agent=agent, query=input_text)

        # Decode the response.
        decoded_response = decode_response(response)

        # Write the response to the Streamlit app.
        write_response(decoded_response)
