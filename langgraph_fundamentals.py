import os,sys
base_path = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(os.path.join(base_path, "src"))
from dotenv import load_dotenv
load_dotenv()

from typing import Annotated
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# If your langchain version supports it, either of these should work:
# llm = init_chat_model("openai:gpt-4o-mini", temperature=0.7)
llm = init_chat_model("openai:gpt-4o-mini", temperature=0.7, api_key=os.environ["OPENAI_API_KEY"])
os.environ["TAVILY_API_KEY"] = "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" 

tool = TavilySearch(max_results=2)
llm_with_tools = llm.bind_tools([tool])

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=[tool]))
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile()