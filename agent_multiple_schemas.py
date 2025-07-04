from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig

class OverallState(TypedDict):
    question:str
    answer:str
    notes:str

class InputState(TypedDict):
    question:str

class OutputState(TypedDict):
    answer:str

def thinking_node(state: InputState):
    """A node that thinks about the question"""
    return {
        "answer": "Bye!",
        "notes": "I am a philosopher now!!",
    }
def get_response(state: OverallState) -> str:
    """A node that gets a response from the model"""
    llm = ChatOllama(model="llama3.2:latest", temperature=0.1)
    response = llm.invoke(f"question: {state["question"]}")
    return response



def answer_node(state: OverallState)-> OutputState:
    """A node that answers the question"""
    return {
        "answer": get_response(state).content,
    }

def main(question:str):
    builder = StateGraph(OverallState, input=InputState, output=OutputState)
    builder.add_node("thinking", thinking_node)
    builder.add_node("answering", answer_node)
    builder.add_edge(START, "thinking")
    builder.add_edge("thinking", "answering")
    builder.add_edge("answering", END)

    thread = RunnableConfig(configurable={"thread_id": "1"})
    graph = builder.compile(checkpointer=MemorySaver())
    with open("multiple_schemas.png", "wb") as f:
        f.write((graph.get_graph()).draw_mermaid_png())

    return graph.invoke(
        input={"question": {question}},
        config=thread
    )

if __name__ == "__main__":
    result = main(input("Enter your question: "))
    print(result['answer'])
