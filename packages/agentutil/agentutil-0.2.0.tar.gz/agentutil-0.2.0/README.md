# AgentUtil

Basic classes and utilities for developing agent-based applications.

## Installation

```sh
pip install agentutil
```

Or, if you are developing locally:

```sh
pip install -e .
```

Or, if you are use `uv`:
```sh
uv add agentutil
```

## Usage

### Importing

```python
from agentutil.utils.agentAssistant import TestAgentAssistant, AgentAssistant
from agentutil.agent import Agent  # or your custom agent class
from agentutil.utils.models import News
```

### Example: Custom Assistant and Agent

```python
import asyncio
from agentutil.utils.agentAssistant import AgentAssistant
from agentutil.agent import Agent
from agentutil.utils.models import News

class SJAssistant(AgentAssistant):
    def __init__(self):
        super().__init__()

    def publish_article(self, news_id: str, news: News):
        print("MY CUSTOM PUBLISH...")
        await asyncio.sleep(1)

    def update_news_status(
        self,
        news_id: str,
        new_status: str,
        title: str = None,
        cms_news_id: int = None,
        cost: int = None,
        duration=None
    ):
        print("MY CUSTOM UPDATE...")

assistant = SJAssistant()

# Example agent class inheriting from Agent
class MasterAgent(Agent):
    async def run(self, data):
        print("Running MasterAgent...")

agent = MasterAgent(assitant=assistant)
agent.assitant.update_news_status("master_agent", "running")

asyncio.run(agent.assitant.publish_article(News(title="Sample"), "test"))
```

## Custom Agent package structure

```
ai_engine/graphs/agent1
├── __init__.py
├── agent.py
├── config.py
│
├── form
│   ├── __init__.py
│   └── agent_form.py
│
├── agents
│   ├── __init__.py
│   ├── node1.py
│   ├── node2.py
│   .
│   :
│   └── nodeN.py
│
├── models
│   ├── __init__.py
│   └──  models.py
│
├── outputformats
│   ├── __init__.py
│   └── formats.py
│
├── prompts
│   ├── __init__.py
│   └──  prompts.py
│
└── tools
    ├── __init__.py
    ├── tools1.py
    ├── tools2.py
    .
    :
    └── toolsN.py
```

your `agent.py` file should be like this:

```
from agentutil.agent import Agent
from .form.agent_form import NewsForm
from .config import AGENT_CONFIG

class MasterAgent(Agent):
    def __init__(self, assistant=None, form=None):
        super().__init__(assitant=assistant)
        self.form = NewsForm
        self.config = AGENT_CONFIG

    async def run(self, data):
        # your custom agent graph
        pass
```
your `config.py` should contains these fields:
```
AGENT_CONFIG = {
    "name": "نام خط تولید",
    "description": "توضیحات مربوط به خط تولید",
    "parameters": {
    }
}
```
your `form.agent_form.py` should be like this:

```
from django import forms

class NewsForm(forms.Form):
    pass
```
## License

MIT