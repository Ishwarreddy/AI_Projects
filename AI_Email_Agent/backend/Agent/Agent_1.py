from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from Tools.send_email import send_email


@tool
def email_tool(receiver: str, message: str) -> str:
    """
    Send an email to a specified recipient.
    Use this tool when the user wants to send an email or message to someone.
    Args:
        receiver: The recipient's full email address (e.g. john@example.com).
        message:  The plain-text body of the email to send.
    Returns:
        A confirmation string if the email was sent successfully.
    """
    return send_email(receiver, message)


llm = ChatOpenAI(model="gpt-4o", temperature=0)
Agent_1 = create_react_agent(model=llm, tools=[email_tool])