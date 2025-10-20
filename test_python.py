from custom_llm import CustomLLMModel

num1 = input('Enter first number: ')
num2 = input('Enter second number: ')
action = input('Enter the action to be performed: ')
PROMPT = (f" You are an expert and senior arithmetic teacher. Perform the {action} on {num1} , {num2}"
          f" Explain your reasons for choosing the operands the way you did"
          f" Double check what happens if the sequence of operands are reversed "
          f" Validate and update your response"
          f" Summarize the output for brevity")
model = CustomLLMModel(reasoning=True)
response= model.getchatinstance().invoke(input=PROMPT)

print(response.content)




