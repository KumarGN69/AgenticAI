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
react_graph = builder.compile(interrupt_before=["assistant"],checkpointer=MemorySaver())
with open("reactgraph_memory.png", "wb") as f:
    f.write(react_graph.get_graph().draw_mermaid_png())

#---------------------thread config for the graph-------------------
thread = RunnableConfig(configurable={"thread_id": "1"})

#---------------------Invoke the graph for Agent functionality-------------------
user_input = input("What do you want to do? (add/multiply/divide) ex:Add 3 and 4: ")

for event in react_graph.stream(input={"messages":HumanMessage(content=user_input, name="Kumar")},config=thread,stream_mode="values" ):
    event["messages"][-1].pretty_print()

# user_input = input("Do you want to call the tool? (yes/no): ")
react_graph.update_state(thread, {"messages": [HumanMessage(content="No actually divide 1000 by 120", name="Kumar")]})

if input("Do you want to call the tool? (yes/no): ").lower() == "yes":
    for event in react_graph.stream(input=None,config=thread,stream_mode="values" ):
        event["messages"][-1].pretty_print()
else:
    print("No tool called, exiting.")
