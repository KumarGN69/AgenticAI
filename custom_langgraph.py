from typing import TypedDict, Literal
import random
from langgraph.graph import StateGraph , START, END
from custom_llm import CustomLLMModel

class State(TypedDict):
    graph_state:str

model = CustomLLMModel()
client = model.getclientinterface()

def node_1(state):
    print("--Node1--")
    return {"graph_state": state['graph_state']+"I am "}

def node_2(state):
    print("--Node2--")
    user_input = input("Enter your mood: ")
    response = client.generate(
        model=model.MODEL_NAME,
        prompt=f"What is the facial expression when the person is {user_input}?",
    )
    return {"graph_state": state['graph_state'] + f"{response.response}"}

def node_3(state):
    print("--Node3--")
    return {"graph_state": state['graph_state']+" sad :("}

def decide_mood(state)->Literal["node_2", "node_3"]:
    user_input = state['graph_state']
    if random.random() > 0.1:
        return "node_2"
    else:
        return "node_3"

builder = StateGraph(State)
builder.add_node("node_1",node_1)
builder.add_node("node_2",node_2)
builder.add_node("node_3",node_3)

builder.add_edge(START,"node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

graph = builder.compile()

with open("graph.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())

result = graph.invoke({"graph_state":"Hi I am Kumar,"})
print("Final graph_state:", result["graph_state"])