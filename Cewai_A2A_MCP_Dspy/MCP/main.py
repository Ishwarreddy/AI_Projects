"""
Project 1 — MCP (Model Context Protocol)
Topic: Weather Assistant
==========================================

WHAT IS MCP IN SIMPLE WORDS:
  MCP is a standard way to give tools to an AI agent.
  Instead of each agent having its own random tools,
  MCP says "let's have ONE standard way to define tools
  so ANY agent can use them."

  Think of it like a USB standard:
    Before USB  → every device had different plugs (chaos)
    After USB   → one standard plug, works everywhere
    MCP         → one standard way to define AI tools

THIS PROJECT:
  A Weather Assistant agent with 3 MCP-style tools:
    Tool 1: get_weather       → get weather for a city
    Tool 2: get_forecast      → get 3-day forecast
    Tool 3: get_weather_tip   → get clothing tip based on weather

  Agent receives: "What is the weather in London?"
  Agent uses MCP tools to answer it.

HOW TO RUN:
  pip install -r requirements.txt
  python main.py
"""

import os
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

load_dotenv()

# ============================================================
# MCP TOOLS — Standard way to define tools
# In real MCP, these would be on a separate server
# For learning, we define them here in the same file
# ============================================================

@tool
def get_weather(city: str) -> str:
    """
    MCP Tool 1: Get current weather for a city.
    Args:
        city: Name of the city e.g. London, Mumbai, New York
    Returns:
        Current weather conditions
    """
    # Simulated weather data (in real project → call weather API)
    weather_data = {
        "london":   {"temp": "12°C", "condition": "Cloudy",  "humidity": "80%", "wind": "15 km/h"},
        "mumbai":   {"temp": "32°C", "condition": "Humid",   "humidity": "90%", "wind": "10 km/h"},
        "new york": {"temp": "18°C", "condition": "Sunny",   "humidity": "55%", "wind": "20 km/h"},
        "dubai":    {"temp": "38°C", "condition": "Hot",     "humidity": "40%", "wind": "8 km/h"},
        "paris":    {"temp": "15°C", "condition": "Rainy",   "humidity": "75%", "wind": "12 km/h"},
        "tokyo":    {"temp": "22°C", "condition": "Clear",   "humidity": "60%", "wind": "18 km/h"},
    }

    city_lower = city.lower()
    if city_lower in weather_data:
        w = weather_data[city_lower]
        return (
            f"Weather in {city}:\n"
            f"  Temperature : {w['temp']}\n"
            f"  Condition   : {w['condition']}\n"
            f"  Humidity    : {w['humidity']}\n"
            f"  Wind Speed  : {w['wind']}"
        )
    return f"Weather data not available for {city}. Try: London, Mumbai, New York, Dubai, Paris, Tokyo"


@tool
def get_forecast(city: str) -> str:
    """
    MCP Tool 2: Get 3-day weather forecast for a city.
    Args:
        city: Name of the city e.g. London, Mumbai, New York
    Returns:
        3-day weather forecast
    """
    forecasts = {
        "london":   ["Day 1: Cloudy 12°C", "Day 2: Rainy 10°C",  "Day 3: Sunny 14°C"],
        "mumbai":   ["Day 1: Humid 32°C",  "Day 2: Humid 33°C",  "Day 3: Rainy 29°C"],
        "new york": ["Day 1: Sunny 18°C",  "Day 2: Cloudy 16°C", "Day 3: Rainy 14°C"],
        "dubai":    ["Day 1: Hot 38°C",    "Day 2: Hot 39°C",    "Day 3: Hot 37°C"],
        "paris":    ["Day 1: Rainy 15°C",  "Day 2: Cloudy 13°C", "Day 3: Sunny 17°C"],
        "tokyo":    ["Day 1: Clear 22°C",  "Day 2: Cloudy 20°C", "Day 3: Rainy 18°C"],
    }

    city_lower = city.lower()
    if city_lower in forecasts:
        days = forecasts[city_lower]
        return (
            f"3-Day Forecast for {city}:\n"
            f"  {days[0]}\n"
            f"  {days[1]}\n"
            f"  {days[2]}"
        )
    return f"Forecast not available for {city}."


@tool
def get_weather_tip(condition: str) -> str:
    """
    MCP Tool 3: Get clothing and activity tip based on weather condition.
    Args:
        condition: Weather condition e.g. Sunny, Rainy, Cloudy, Hot, Humid
    Returns:
        Practical tip for the weather condition
    """
    tips = {
        "sunny":  "Wear sunscreen and light clothes. Great day for outdoor activities!",
        "rainy":  "Carry an umbrella. Wear waterproof shoes. Avoid outdoor plans.",
        "cloudy": "Light jacket recommended. Good day for a walk.",
        "hot":    "Stay hydrated. Wear loose light-colored clothes. Avoid noon sun.",
        "humid":  "Wear breathable cotton clothes. Stay hydrated. Use deodorant.",
        "clear":  "Perfect weather! Light clothes. Enjoy outdoor activities.",
        "windy":  "Wear a jacket. Secure loose items. Good day to fly a kite!",
    }

    condition_lower = condition.lower()
    for key in tips:
        if key in condition_lower:
            return f"Tip for {condition} weather: {tips[key]}"

    return f"General tip: Always check the weather before stepping out!"


# ============================================================
# BUILD THE MCP AGENT
# This agent has access to all 3 MCP tools above
# ============================================================

llm = ChatOpenAI(model="gpt-4o", temperature=0)

mcp_tools = [get_weather, get_forecast, get_weather_tip]

system_prompt = """You are a helpful Weather Assistant.
You have access to 3 tools:
  1. get_weather      - for current weather
  2. get_forecast     - for 3-day forecast
  3. get_weather_tip  - for clothing/activity tips

Always use the tools to get accurate information.
Be concise and friendly in your responses."""

weather_agent = create_react_agent(
    model=llm,
    tools=mcp_tools,
    prompt=system_prompt
)


# ============================================================
# MAIN — Run the Weather Assistant
# ============================================================

def ask_agent(question: str):
    print(f"\n{'='*50}")
    print(f"You: {question}")
    print(f"{'='*50}")

    result = weather_agent.invoke({
        "messages": [("user", question)]
    })

    answer = result["messages"][-1].content
    print(f"Agent: {answer}")


if __name__ == "__main__":
    print("\n" + "="*50)
    print(" MCP Weather Assistant")
    print(" Topic: Weather | Tools: 3 MCP-style tools")
    print("="*50)
    print(" Cities available: London, Mumbai, New York,")
    print("                   Dubai, Paris, Tokyo")
    print("="*50)

    # Sample questions to show MCP tool usage
    sample_questions = [
        "What is the weather in London?",
        "Give me the 3-day forecast for Mumbai",
        "What should I wear in rainy weather?",
        "What is the weather in Tokyo and any tips?",
    ]

    print("\nSample questions:")
    for i, q in enumerate(sample_questions, 1):
        print(f"  {i}. {q}")
    print("  5. Ask your own question")

    choice = input("\nEnter choice (1-5): ").strip()

    if choice in ("1", "2", "3", "4"):
        ask_agent(sample_questions[int(choice) - 1])
    elif choice == "5":
        question = input("Your question: ").strip()
        ask_agent(question)
    else:
        ask_agent(sample_questions[0])

    # Interactive mode
    print("\n\nEnter 'exit' to quit or keep asking questions!")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        if user_input:
            ask_agent(user_input)