from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Import your existing components
from langsmith import Client
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_tableau.tools.simple_datasource_qa import initialize_simple_datasource_qa
from utilities.prompt import AGENT_SYSTEM_PROMPT

# Load environment variables
load_dotenv()

# Add LangSmith tracing
langsmith_client = Client()

config = {
    "run_name": "Tableau Langchain Web_App.py"
}

# Create FastAPI app
app = FastAPI(title="Tableau AI Chat", description="Simple AI chat interface for Tableau data")

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Request/Response models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Initialize your agent (same as your original code)
def setup_agent():
    """Initialize the Tableau LangChain agent"""
    
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

    return create_react_agent(
        model=llm, 
        tools=tools,
        prompt=AGENT_SYSTEM_PROMPT
    )

# Initialize agent once when app starts
agent = setup_agent()

@app.get("/")
def home():
    """Serve the main HTML page"""
    return FileResponse('static/index.html')

@app.get("/index.html")
def static_index():
    return FileResponse('static/index.html')

@app.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:
    """Handle chat messages - this is where the AI magic happens"""
    try:
        # Use your existing agent logic
        messages = {"messages": [("user", request.message)]}
        
        # Get response from agent
        response_text = ""
        for chunk in agent.stream(messages, config=config, stream_mode="values"):
            if 'messages' in chunk and chunk['messages']:
                latest_message = chunk['messages'][-1]
                if hasattr(latest_message, 'content'):
                    response_text = latest_message.content
        
        return ChatResponse(response=response_text)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
