## Pydantic AI Unofficial Models

A package containing support for unofficial wrapper of LLM Models in the Pydantic AI framework/style/ecosystem.

### Meta AI API (Unofficial)

#### Basic Usage
```python
from pydantic_ai import Agent
from pydantic_ai_unofficial_models import MetaAIChatModel

model = MetaAIChatModel()
agent = Agent(model)

response = agent.run_sync("Hi, I am John, give some famous personality names based of my name.")

print(response)
```

#### Usage with Tools

```python
from pydantic_ai import Agent
from pydantic_ai_unofficial_models import MetaAIChatModel

model = MetaAIChatModel()
agent = Agent(model)

@agent.tool_plain
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@agent.tool_plain
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@agent.tool_plain
def subtract(a: int, b: int) -> int:
    """Subtract two numbers."""
    return a - b

@agent.tool_plain
def divide(a: int, b: int) -> float:
    """Divide two numbers."""
    return a / b

result = agent.run_sync("I have borrowed $2,000 at 6% interest for 1 year. What’s the EMI?")
print(result)
```
