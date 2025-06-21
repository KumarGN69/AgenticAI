from typing import TypedDict, Literal
import random
from langgraph.graph import StateGraph , START, END
from dataclasses import dataclass
from pydantic import BaseModel

class State(TypedDict):
    graph_state:str

# @dataclass
# class DataClassState:
#     name: str
#     mood: Literal["happy", "sad"]

class PydanticState(BaseModel):
    name: str
    mood: Literal["happy", "sad"]
    # __pydantic_fields_set__: set = set()

def node_1(state):
    print("--Node1--")
    # return {"graph_state": state['graph_state']+"I am"}
    return {"name":state.name + "is ..."}


def node_2(state):
    print("--Node2--")
    # return {"graph_state": state['graph_state']+" happy! :)"}
    return {"name": state.name + "happy! :)"}
def node_3(state):
    print("--Node3--")
    # return {"graph_state": state['graph_state']+" sad :("}
    return {"name": state.name + "sad :("}

def decide_mood(state)->Literal["node_2", "node_3"]:
    user_input = state.name
    if random.random() < 0.5:
        return "node_2"
    else:
        return "node_3"

builder = StateGraph(PydanticState)
builder.add_node("node_1",node_1)
builder.add_node("node_2",node_2)
builder.add_node("node_3",node_3)

builder.add_edge(START,"node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

graph = builder.compile()

# with open("graph.png", "wb") as f:
#     f.write(graph.get_graph().draw_mermaid_png())

# result = graph.invoke({"graph_state":"Hi I am Kumar,"})
# print("Final graph_state:", result["graph_state"])

result = graph.invoke(PydanticState(name="Kumar", mood="mad"))
print("Final name:", result["name"])