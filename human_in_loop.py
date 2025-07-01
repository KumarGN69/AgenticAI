from langchain_core.messages import AIMessage, HumanMessage,SystemMessage, BaseMessage, RemoveMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig

#---------------------Model instantiation-------------------
model = ChatOllama(model = "llama3.2:latest")

#---------------------Graph state message definition-------------------
class State(MessagesState):
    summary:str
#---------------------Define the start and end states-------------------
def call_model(state:State,config:RunnableConfig):
    """
    Call the model with the current state and return the response.
    """
    summary = state.get("summary", "")
    if summary:
        system_message = f"Summary of the earlier conversation: {summary}\n"
        messages = [SystemMessage(content=system_message)] + state["messages"]
    else:
        messages =state["messages"]
    response = model.invoke(messages, config=config)
    return {"messages": response }
#---------------------Define the conversation summarization-------------------
def summarize_conversation(state:State):
    """
    Summarize the conversation so far.
    """
    summary = state.get("summary", "")
    if summary:
        summary_message =(
            f"This is summary of the conversation to date :{summary}\n"
            f"Extend the summary with the latest messages.\n"
        )
    else:
        summary_message= "Create a summary of the conversation so far.\n"

    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"summary": response.content, "messages":delete_messages}

#---------------------Define the condition to continue the conversation-------------------
def should_continue(state:State):
    """Return to execute next node"""
    messages = state["messages"]
    if len(messages) >=6:
        return "summarize_conversation"
    else:
        return "conversation"

#---------------------Define the components of the Graph-------------------
workflow = StateGraph(State)
workflow.add_node("conversation", call_model)
workflow.add_node("summarize_conversation",summarize_conversation)
#---------------------Define the flow in the Graph-------------------
workflow.add_edge(START,"conversation")
workflow.add_conditional_edges("conversation", should_continue,
    {
        "conversation": "conversation",                    # Loop back
        "summarize_conversation": "summarize_conversation" # Go to summary
    }
)
workflow.add_edge("summarize_conversation", END)

#---------------------Define memory persistance-------------------
graph = workflow.compile(checkpointer=MemorySaver())

# Save the graph as an image
with open("human_in_loop.png", "wb") as f:
    f.write((graph.get_graph()).draw_mermaid_png())
#---------------------Define the thread for graph workflow-------------------
config = RunnableConfig(configurable={"thread_id": "1"})

for chunk in graph.stream({"messages":[HumanMessage(content="Hi ! I am Kumar")]},config=config,stream_mode="updates"):
    print(chunk)
    # chunk["conversation"]["messages"].pretty_print()


