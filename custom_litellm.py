import os, requests, dotenv
from smolagents import CodeAgent, tool, LiteLLMModel

dotenv.load_dotenv()

@tool
def jobsearch(query: str) -> str:
    """
    This tool returns the open jobs
    Args:
        query (str): The search query containing job title, location, and type.
    """
    # construct the query for searching the job sites
    search_query = f"http://serpapi.com/search?q={query}&api_key={os.getenv("SERPAPI_API_KEY")}"
    # make the http api call to serpapi service
    response = requests.get(url=search_query, verify=False)
    # convert and extract the relevant search details
    open_jobs = response.json()['organic_results']
    return open_jobs

model = LiteLLMModel(model_id="ollama_chat/mistral:latest", api_key="ollama")
agent = CodeAgent(tools = [jobsearch], model=model)
response = agent.run(
        task="Search for jobs in Hyderabad for Vice president with Hybrid working options",
        max_steps=1
    )
print(type(response))
print(response)