from langchain_core.messages import HumanMessage,SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.load.dump import dumps
import json, pprint
def multiply(a:int, b:int) ->int:
    """
    Multiply a and b
    Args:
        a: first int
        b: second int
    """
    return a * b
def add(a:int, b:int) ->int:
    """
    Add a and b
    Args:
        a: first int
        b: second int
    """
    return a + b
def divide(a:int, b:int) ->float:
    """
    Divide a by b
    Args:
        a: first int
        b: second int
    """
    return float(a / b)

tools = [add, multiply, divide]

model = ChatOllama(model = "llama3.2:latest")
model_with_tools = model.bind_tools(tools)

sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on set of given inputs")

def assistant(state:MessagesState):
    return {"messages":[model_with_tools.invoke([sys_msg] + state["messages"])]}

builder = StateGraph(MessagesState)
builder.add_node("assistant",assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

react_graph = builder.compile()

with open("react_graph.png", "wb") as f:
    f.write(react_graph.get_graph().draw_mermaid_png())

messages = [HumanMessage(content=f"Add 3 and 4. Multiply the output by 2 . Divide the output by 5", name="Kumar")]

results = react_graph.invoke({"messages": messages})
pprint.pprint(dumps(results))
for message in results["messages"]:
    message.pretty_print()