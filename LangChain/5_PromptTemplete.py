from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatOpenAI(model = "gpt-4o")


messages = [
    ("system", "You are a comedian who tells jokes about {topic}."),
    ("human", "Tell me {joke_count} joke"),
]

prompt_templete =  ChatPromptTemplate.from_messages(messages)
prompt = prompt_templete.invoke({"topic": "lawyers" , "joke_count": 3 })
result= llm.invoke(prompt)
print(result.content)
