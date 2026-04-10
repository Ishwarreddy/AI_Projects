from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model = "gpt-4o")

message = [
    SystemMessage("Yor are an expect in maths"),
    HumanMessage("tell me what is square root of 81??")
]

result = llm.invoke(message)
print(result.content)