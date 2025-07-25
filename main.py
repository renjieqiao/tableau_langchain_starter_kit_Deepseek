import os
from dotenv import load_dotenv

# Import LangSmith tracing (debugging in LangSmith.com)
from langsmith import Client

# Langgraph packages
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_tableau.tools.simple_datasource_qa import initialize_simple_datasource_qa

from utilities.chat import print_stream
from utilities.prompt import AGENT_SYSTEM_PROMPT

# Load environment
load_dotenv()

# Add LangSmith tracing
langsmith_client = Client()

config = {
    "run_name": "Tableau Langchain Main.py"
}

# Initialize the Tableau data source tool
analyze_datasource = initialize_simple_datasource_qa(
    domain=os.environ['TABLEAU_DOMAIN'],
    site=os.environ['TABLEAU_SITE'],
    jwt_client_id=os.environ['TABLEAU_JWT_CLIENT_ID'],
    jwt_secret_id=os.environ['TABLEAU_JWT_SECRET_ID'],
    jwt_secret=os.environ['TABLEAU_JWT_SECRET'],
    tableau_api_version=os.environ['TABLEAU_API_VERSION'],
    tableau_user=os.environ['TABLEAU_USER'],
    datasource_luid=os.environ['DATASOURCE_LUID'],
    tooling_llm_model="deepseek-reasoner",
    model_provider="deepseek"
)

# Create the agent
llm = ChatOpenAI(
        model="deepseek-reasoner", #deepseek-reasoner   deepseek-chat
        temperature=0,
        base_url=os.getenv("OPENAI_API_BASE"),   # DeepSeek API URL
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
tools = [analyze_datasource]

TableauLangChain = create_react_agent(
    model = llm, 
    tools = tools,
    prompt=AGENT_SYSTEM_PROMPT)
    
# Usage
your_prompt = 'Show Me the Top Customers by Sales'

# Run the agent
messages = {"messages": [("user", your_prompt)]}
print_stream(TableauLangChain.stream(messages, config=config, stream_mode="values"))

