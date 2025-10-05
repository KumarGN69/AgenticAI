import dspy

class DSPY:
    def __init__(self):
        self.lm = dspy.LM(model='ollama_chat/mistral:latest',api_base='http://localhost:11434',api_key='')
        dspy.configure(lm=self.lm)

    def chainofthought(self, question, answer) -> None:
        qa = dspy.ChainOfThought('question -> answer')
        response = qa(question=question, answer=answer)
        print(type(response.answer))
        print("Reasoning:",response.reasoning)
        print("Answer:",response.answer)

# Example usage
handle = DSPY()
handle.chainofthought(question='Who is the president of USA', answer='')

