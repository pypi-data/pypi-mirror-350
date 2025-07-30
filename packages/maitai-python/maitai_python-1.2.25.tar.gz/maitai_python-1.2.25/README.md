# Quickstart

Full docs can be found at https://docs.trymaitai.ai

## Installation

Install the Maitai SDK:

```bash
pip install maitai-python
```

## Implementation

Implementing Maitai into your application requires minimal code changes.

```python
import maitai

messages = [
    {"role": "system", "content": "You are a helpful ordering assistant..."},
    {"role": "user", "content": "Generate a response to the customer..."},
]

response = maitai.chat.completions.create(
    messages=messages,
    model="llama3-70b-8192",  ## Remove this line to set model in Portal
    session_id="YOUR_SESSION_ID",
    intent="CONVERSATION",
    application="YOUR_APPLICATION_NAME",
)
```

**Note**
Maitai requires `openai` version `1.30.1` or later. If you are using an older version, please upgrade.

## Run Your Application

Run your application, make sure it makes at least one Chat Completion Request, then head over
to https://portal.trymaitai.ai and watch Maitai learn your application in real time.