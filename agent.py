from langchain import OpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd

# Setting up the api key
API_KEY = "1234"


def create_agent(filename: str):
    """
    Create an agent that can access and use a large language model (LLM).

    Args:
        filename: The path to the CSV file that contains the data.

    Returns:
        An agent that can access and use the LLM.
    """

    # Create an OpenAI object.
    llm = OpenAI(openai_api_key=API_KEY)

    # Read the CSV file into a Pandas DataFrame.
    df = pd.read_csv(filename)

    # Create a Pandas DataFrame agent.
    return create_pandas_dataframe_agent(llm, df, verbose=True)


def truncate_prompt(prompt: str, max_tokens: int) -> str:
    tokens = prompt.split()  # simple whitespace tokenization
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
    return ' '.join(tokens)


def query_agent(agent, query):
    """
    Query an agent and return the response as a string.

    Args:
        agent: The agent to query.
        query: The query to ask the agent.

    Returns:
        The response from the agent as a string and responds in Brazilian Portuguese.
    """

    prompt = (
            """
            {"language": "pt-BR"}  # Specify Brazilian Portuguese
            Para a seguinte consulta, responda da seguinte forma:
            {"answer": "answer"}
    
            Retorne todas as saídas como uma string.
    
            Abaixo está a consulta.
            Consulta: 
            """
            + query
    )

    new_prompt = truncate_prompt(prompt, 3800)

    # Run the prompt through the agent.
    response = agent.run(new_prompt)

    # Convert the response to a string.
    return response.__str__()
