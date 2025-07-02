from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END, MessagesState
from typing import Any, Annotated
from typing_extensions import TypedDict
import operator
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig

def sorting_reducer(left, right):
    """ Combines and sorts the values in a list"""
    if not isinstance(left, list):
        left = [left]
    if not isinstance(right, list):
        right = [right]
    return sorted(left + right, reverse=False)

class State(TypedDict):
    state:Annotated[list, sorting_reducer]

class ReturnNodeValue:
    def __init__(self, node_secret: Any):
        self.value = node_secret
    def __call__(self, state: State) -> str:
        print(f"Adding {self.value} to {state["state"]}")
        return {"state": [self.value]}


def main():
    builder = StateGraph(State)
    builder.add_node("A", ReturnNodeValue(node_secret="I am A node"))
    builder.add_node("B1", ReturnNodeValue(node_secret="I am B1 node"))
    builder.add_node("B2", ReturnNodeValue(node_secret="I am B2 node"))
    builder.add_node("C", ReturnNodeValue(node_secret="I am C node"))
    builder.add_node("D", ReturnNodeValue(node_secret="I am D node"))

    builder.add_edge(START, "A")
    builder.add_edge("A", "B1")
    builder.add_edge("A", "C")
    builder.add_edge("B1", "B2")
    builder.add_edge(["B2","C"], "D")
    builder.add_edge("D", END)

    memory = MemorySaver()
    thread = RunnableConfig(configurable={"thread_id": "1"})
    graph = builder.compile(checkpointer=memory)
    with open("parallelization.png", "wb") as f:
        f.write((graph.get_graph()).draw_mermaid_png())


    graph.invoke(input={"state":[]},config=thread)
    print(graph.get_state(config=thread).values["state"])

if __name__ == "__main__":
    main()
    print("Graph executed successfully.")