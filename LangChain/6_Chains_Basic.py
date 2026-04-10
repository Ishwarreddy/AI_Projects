from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
llm = ChatOpenAI(model = "gpt-4o")


prompt_templete = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a facts expert who know about{animal}."),
        ("human", "tell me {fact_count}."),
    ]
)

chain = prompt_templete | llm | StrOutputParser()

result =chain.invoke({"animal": "elephant" , "fact_count": 1})
print(result)

