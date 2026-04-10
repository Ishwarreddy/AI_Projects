from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv

load_dotenv()

chat_history = ChatMessageHistory()


loader = PyPDFLoader(r"D:\Artificial_Inteligence_AI\Project\PDF_QA\Sample_PDF\Yeswant Yadav Nakka-Resume.pdf")
documents = loader.load()


text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=512)
vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever()

# LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)


prompt = ChatPromptTemplate.from_template("""
Answer the question based only on the following context:
{context}

Chat History:
{chat_history}

Question: {question}
""")

def format_history(history):
    lines = []
    for msg in history.messages:
        role = "User" if msg.type == "human" else "AI"
        lines.append(f"{role}: {msg.content}")
    return "\n".join(lines)

rag_chain = (
    {
        "context": lambda x: retriever.invoke(x["question"]),
        "question": lambda x: x["question"],
        "chat_history": lambda x: x["chat_history"]
    }
    | prompt
    | llm
    | StrOutputParser()
)


while True:
    query = input("Ask your question: ")

    if query.lower() == "exit":
        print("Bye")
        break                           

    chat_history.add_user_message(query)

    result = rag_chain.invoke({       
        "question": query,
        "chat_history": format_history(chat_history)
    })

    chat_history.add_ai_message(result)

    print("\nAnswer:")
    print(result)