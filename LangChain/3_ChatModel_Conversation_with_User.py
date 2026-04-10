
"""-------------------------Chat History is stored in Local memory-----------------------------"""



from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage , AIMessage ,SystemMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o")
chat_history=[]

system_message = SystemMessage(content="You are a helpful chat assistant.")
chat_history.append(system_message)
 
while True:
    query = input("You: ")
    if query.lower() == "exit":
        break
    chat_history.append(HumanMessage(content=query))

    result = llm.invoke(chat_history)
    response = result.content
    chat_history.append(AIMessage(content=response))
    print(f"AI : {response}")

print("-----------Message Hostory-----------------")
print(chat_history)

