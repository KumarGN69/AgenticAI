from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage,SystemMessage, BaseMessage
from custom_llm import CustomLLMModel
from langchain_ollama import ChatOllama

model = ChatOllama(model = "mistral:latest")

messages = [AIMessage(content="Hi")]
messages.append(AIMessage(content=f"SO you want to learn about Integral Calculus?", name="Model"))
messages.append(HumanMessage(content=f"Yes that's right!", name="Kumar"))
messages.append(AIMessage(content=f"What part of Integral calculus do you want to learn", name="Model"))
messages.append(HumanMessage(content=f"I want to learn about basics!", name="Kumar"))

result = model.invoke(messages)
# print(type(result))
pprint(result)
