from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage,SystemMessage, BaseMessage
from custom_llm import CustomLLMModel
from langchain_ollama import ChatOllama

def multiply(a:int, b:int) ->int:
    """
    Multiply a and b
    Args:
        a: first int
        b: second int
    """
    return a * b
model = ChatOllama(model = "mistral:latest")

messages = [AIMessage(content="Hi")]
messages.append(AIMessage(content=f"SO you want to learn about Integral Calculus?", name="Model"))
messages.append(HumanMessage(content=f"Yes that's right!", name="Kumar"))
messages.append(AIMessage(content=f"What part of Integral calculus do you want to learn", name="Model"))
messages.append(HumanMessage(content=f"I want to learn about basics!", name="Kumar"))

model_with_tools = model.bind_tools([multiply])
result = model_with_tools.invoke([HumanMessage(content=f"What is 3 multipled by 10", name="Kumar")])
# print(type(result))
pprint(result.tool_calls)
