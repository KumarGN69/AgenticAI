from custom_llm import CustomLLMModel
from pydantic import BaseModel, Field

class Result(BaseModel):
    action: str
    result: float

# Define the arithmetic functions
def multiply(a:int, b:int) ->int:
    """
    Multiply a and b
    Args:
        a: first int
        b: second int
    """
    return a * b
def add(a:int, b:int) ->int:
    """
    Add a and b
    Args:
        a: first int
        b: second int
    """
    return a + b
def divide(a:int, b:int) ->float:
    """
    Divide a by b
    Args:
        a: first int
        b: second int
    """
    return float(a / b)

model = CustomLLMModel().getmodelinstance()
# structured_llm = model.with_structured_output(Result)
query = input("Enter the arithmetic functions you want to perform: ")
prompt = (
            f"You are an experienced arithmetic teaching assistant"
            f"You have access to the following tools:"
            f"[{add},{multiply},{divide}]"
            f"Create python code using these tools per user instruction in {query}"
            # f"Save the generated code as generated_code.py in the same folder"
            f"Execute the generated code and output the final result "
        )

response = model.invoke(prompt)
print(f"The answer to your arithmetic task is:{response}")