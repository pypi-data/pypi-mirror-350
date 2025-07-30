# AgenticWrapper

English | [简体中文](README_zh-CN.md)

AgenticWrapper is an extremely lightweight Python Agent framework that wraps your custom LLM function, enabling it with Agent capabilities, including **tool calling, memory management, and structured output**.

AgenticWrapper has no runtime dependencies.

## Quick Start

### Installation

```bash
pip install AgenticWrapper
```

### Basic Usage

```python
from AgenticWrapper import Agent

async def llm_func(messages: list[dict[str, str]]) -> str:
    # Assume this is your custom LLM function
    return "Hello, I'm AgenticWrapper."

agent = Agent(llm_func)
response = await agent.query("Hello")
print(response)
agent.clear_memory()
```

### Structured Output

Use Python `dataclass` to define the output structure:

```python
@dataclass
class SearchResult:
    query: str
    results: List[str]
    total_count: int

response = await agent.query("Search for relevant content", structured_output_type=SearchResult)
assert isinstance(response, SearchResult)
```

### Tool Calling

Define a tool function, preferably with function documentation:

```python
async def get_weather(location: str) -> str:
    """Get weather information"""
    # Simulate an API call
    await asyncio.sleep(0.1)
    if location.lower() == "london":
        return "The weather is clear, with a temperature of 15°C."
    elif location.lower() == "paris":
        return "The weather is clear, with a temperature of 18°C."
    else:
        return f"I don't know the weather for {location}."
```

Use the tool in the Agent:

```python
agent = Agent(llm_interaction_func=mock_llm_func, tools=[get_weather])
response = await agent.query("Check the weather in london")
print(response)
```

Tool function parameters types must be valid json types, return types must be `str`.

### More Examples

More examples can be found in [example.py](example.py).
