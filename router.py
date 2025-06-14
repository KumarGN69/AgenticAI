from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage,SystemMessage, BaseMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

def multiply(a:int, b:int) ->int:
    """
    Multiply a and b
    Args:
        a: first int
        b: second int
    """
    return a * b

model = ChatOllama(model = "mistral:latest")
model_with_tools = model.bind_tools([multiply])

def tool_calling_llm(state:MessagesState):
    return {"messages":[model_with_tools.invoke(state["messages"])]}

builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm",tool_calling_llm)
builder.add_node("tools", ToolNode([multiply]))

builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges("tool_calling_llm", tools_condition)
builder.add_edge("tools", END)

graph = builder.compile()
# messages = [AIMessage(content="Hi")]
messages = [HumanMessage(content=f"Multiply 3 and 6", name="Kumar")]

results = graph.invoke({"messages":messages})
# print(results)
for message in results["messages"]:
    message.pretty_print()

