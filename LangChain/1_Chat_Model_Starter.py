from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm=ChatOpenAI(model="gpt-4o")
result= llm.invoke("What is the current time in india?")
print(result.content)