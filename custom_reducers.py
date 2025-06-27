from typing import TypedDict, Literal, Annotated
from operator import add
import random
from langgraph.graph import StateGraph , START, END
from pydantic import BaseModel
from langgraph.errors import InvalidUpdateError

def reduce_list(left: list | None, right: list | None) -> list:
    """Custom reducer to concatenate two lists, handling cases where one or both are None.

    :param left: First list (or None)
    :param right: Second list (or None)
    :return: Concatenated list
    """
    if left is None:
        left = []
    if right is None:
        right = []
    return left + right


class PydanticState(BaseModel):
    foo: Annotated[list[int],reduce_list]

def node_1(state: PydanticState):
    print("--Node1--")
    return {"foo": [state.foo[0] + 1]}
def node_2(state: PydanticState):
    print("--Node2--")
    return {"foo": [state.foo[0] + 2]}
def node_3(state:PydanticState):
    print("--Node3--")
    return {"foo": [state.foo[0] + 2]}

builder = StateGraph(PydanticState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

builder.add_edge(START, "node_1")
builder.add_edge("node_1","node_2")
builder.add_edge("node_1","node_3")
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

graph = builder.compile()
with open("graph.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())
try:
    result = graph.invoke(PydanticState(foo=[1.5]))
    print("Final result:", result["foo"])
except InvalidUpdateError as e:
    print(f"Invalid update error occurred: {e}")
    # Should print the final value of foo after processing through the nodes
