

from typing import Literal
from langchain_core.messages import HumanMessage
from langchain.chat_models import ChatOpenAI # Using OpenAI for simplicity, replace with Anthropic if needed.
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
import requests
from bs4 import BeautifulSoup

# Wikipedia search tool
@tool
def wikipedia_search(query: str):
    """Searches Wikipedia for a given query and returns a summary."""
    try:
        url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"

        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        content = soup.find('div', class_='mw-parser-output')
        if content:
            paragraphs = content.find_all('p')
            summary = " ".join(paragraph.text for paragraph in paragraphs[:3]).strip()
            return summary
        else:
            return "Error: Content not found on Wikipedia."
    except requests.exceptions.RequestException as e:
        return f"Error: Request failed - {e}"
    except Exception as e:
        return f"Error: An unexpected error occurred - {e}"


def should_continue(state: MessagesState) -> Literal["tools", END]:
    messages = state['messages']
    # Check for tool calls in the *last response*, not the user's message.
    # if len(messages) > 1 and messages[-1].tool_calls:  # Check the AI's response
    #     return "tools"  # Go to tools node if the model suggests a tool call
    if len(messages) > 1 and "Error" not in messages[-1].content and len(messages[-1].content) > 100:
        return END  # Stop if a long enough, error-free summary is obtained
    else:
        return "tools" 


def agentic_search(call_model):
    workflow = StateGraph(MessagesState)

    workflow.add_node("agent", call_model)

    tool_node = ToolNode([wikipedia_search])
    workflow.add_node("tools", tool_node)  # Update as necessary to ensure it aligns with the rest of your infrastructure
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue)
    workflow.add_edge("tools", "agent")

    checkpointer = MemorySaver()

    app = workflow.compile(checkpointer=checkpointer)

    # Run the agent with OpenAI
    final_state = app.invoke(
        {"messages": [HumanMessage(content="Summarize the history of Python")]},
        config={"configurable": {"thread_id": 42}}  # Ensure this configuration is supported
    )

    print(final_state["messages"][-1].content)
