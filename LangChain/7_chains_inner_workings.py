from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableSequence
from langchain_openai import ChatOpenAI

# Load environment variables from .env
load_dotenv()

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4")

# Define prompt templates
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You love facts and you tell facts about {animal}"),
        ("human", "Tell me {count} facts."),
    ]
)

# Create individual runnables (steps in the chain)
format_prompt = RunnableLambda(lambda x: prompt_template.invoke(x))
invoke_model = RunnableLambda(lambda x: model.invoke(x))
parse_output = RunnableLambda(lambda x: x.content)

# Create the RunnableSequence using the | operator
chain = format_prompt | invoke_model | parse_output

# Run the chain
response = chain.invoke({"animal": "cat", "count": 2})

# Output
print(response)