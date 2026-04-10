"""
Steps to replicate this example:
1. Create a Firebase account
2. Create a new Firebase project and FireStore Database
3. Retrieve the Project ID
4. Install the Google Cloud CLI on your computer
    - https://cloud.google.com/sdk/docs/install
    - Authenticate the Google Cloud CLI with your Google account
        - https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev
    - Set your default project to the new Firebase project you created
5. pip install langchain-google-firestore
6. Enable the Firestore API in the Google Cloud Console:
    - https://console.cloud.google.com/apis/enableflow?apiid=firestore.googleapis.com&project=crewai-automation
"""


from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory
import os

load_dotenv()

# Setup Firebase Firestore
PROJECT_ID = "langchain-1bf24"
SESSION_ID = "user_session_new"
COLLECTION_NAME = "chat_history"

# ✅ Fix 2: Set Google credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\Artificial_Inteligence_AI\Project\LangChain\langchain-1bf24-firebase-adminsdk-fbsvc-0d911ed412.json"

# Initialize Firestore Client
print("Initializing Firestore Client...")
client = firestore.Client(project=PROJECT_ID)

# Initialize Firestore Chat Message History
print("Initializing Firestore Chat Message History...")
chat_history = FirestoreChatMessageHistory(
    session_id=SESSION_ID,
    collection=COLLECTION_NAME,
    client=client,
)
print("Chat History Initialized.")
print("Current Chat History:", chat_history.messages)

llm = ChatOpenAI(model="gpt-4o")
print("Start chatting with the AI. Type 'exit' to quit.")

while True:
    query = input("You: ")
    if query.lower() == "exit":
        break

    chat_history.add_user_message(query)
    ai_response = llm.invoke(chat_history.messages)
    
    # ✅ Fix 1: Use correct method to save AI response
    chat_history.add_ai_message(ai_response.content)
    
    print(f"AI: {ai_response.content}")