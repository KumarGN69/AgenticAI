import dspy

lm = dspy.LM(model='ollama_chat/mistral:latest',api_base='http://localhost:11434',api_key='')
dspy.configure(lm=lm)

qa = dspy.ChainOfThought('question -> answer')
response = qa(question='Who is the president of USA')
print(type(response.answer))
print("Reasoning:",response.reasoning)
print("Answer:",response.answer)

