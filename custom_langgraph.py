from typing import TypedDict, Literal, Annotated
from langgraph.graph import StateGraph , START, END, MessagesState
from langchain_core.messages import HumanMessage

from langchain_ollama import ChatOllama

def multiply(a:int, b:int) ->int:
    """
    Multiply a and b
    Args:
        a: first int
        b: second int
    """
    return a * b
def tool_calling_llm(state:MessagesState):
    return {"messages":[llm_with_tools.invoke(state["messages"])]}

llm = ChatOllama(
    model ="mistral:latest"
)
llm_with_tools = llm.bind_tools([multiply])

builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_edge(START, "tool_calling_llm")
builder.add_edge("tool_calling_llm", END)

graph = builder.compile()

result = graph.invoke({"messages":HumanMessage(content="Multiply 4 and 5")})
print("Result:",result["messages"])
