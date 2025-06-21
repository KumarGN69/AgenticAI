from langchain_core.messages import AIMessage, HumanMessage,SystemMessage, BaseMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig

#---------------------Tool definitions-------------------
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
def divide(a:int, b:int) ->int:
    """
    Divide a by b
    Args:
        a: first int
        b: second int
    """
    return a / b

#---------------------tool configs for llm-------------------
tools = [add, multiply, divide]

#---------------------instantiate an LLM and bind with tools-------------------
model = ChatOllama(model = "llama3.2:latest")
model_with_tools = model.bind_tools(tools)

#---------------------Define an assistant function/ tool/node-------------------
sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on set of given inputs")
def assistant(state:MessagesState):
    return {"messages":[model_with_tools.invoke([sys_msg] + state["messages"])]}

#---------------------Create nodes in the graph-----------------
builder = StateGraph(MessagesState)
builder.add_node("assistant",assistant)
builder.add_node("tools", ToolNode(tools))

#---------------------Define the flow in the Graph-------------------
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

#---------------------Define memory persistance-------------------
react_graph = builder.compile(checkpointer=MemorySaver())
with open("reactgraph_memory.png", "wb") as f:
    f.write(react_graph.get_graph().draw_mermaid_png())
config = RunnableConfig(configurable={"thread_id": "1"})

#---------------------Invoke the graph for Agent functionality-------------------
messages = [HumanMessage(content=f"Add 3 and 4", name="Kumar")]
results = react_graph.invoke({"messages":messages},config=config)
# print(results)
for message in results["messages"]:
    message.pretty_print()

messages = [HumanMessage(content=f"Multiply that by 2", name="Kumar")]
results = react_graph.invoke({"messages":messages},config=config)
# print(results)
for message in results["messages"]:
    message.pretty_print()

messages = [HumanMessage(content=f"Divide that by 4", name="Kumar")]
results = react_graph.invoke({"messages":messages},config=config)
# print(results)
for message in results["messages"]:
    message.pretty_print()