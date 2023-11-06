# RayCraft

## Motivation
FastAPI + Ray = <3

Let's take a FastAPI app and supercharge it with Ray Serve

e.g. given you have a FastAPI app:

```python
from fastapi import FastAPI

simple_service = FastAPI()

@simple_service.post("/")
async def read_root() -> dict[str, str]:
    return {"Hello": "World"}
```

You can now run it distributed with Ray using raycraft with a single change:

```python
from raycraft import RayCraftAPI, App

simple_service = RayCraftAPI()

@simple_service.post("/")
async def read_root(app: App) -> dict[str, str]:
    return {"Hello": "World"}


app = simple_service()
```

With Ray Serve, you can now:
- Scale your app deployment to multiple replicas running on different machines
- Define the resources allocated to each replica including fractional GPUs
- Batch requests together to improve throughput
- Get fault tolerance and automatic retries

## How to use

### Basic example
Let's assume we have a translation service that takes in a string and returns the translation.

```python
from fastapi import FastAPI
from transformers import pipeline

app = FastAPI()

def load_model():
    return pipeline("translation_en_to_fr", model="t5-small")

@app.post("/")
async def translate(text: str):
    model = load_model()
    translated = model(text)[0]["translation_text"]
    return {"translation": translated}
```

We can now run this app with Ray Serve using raycraft:

```python
from raycraft import RayCraftAPI
from fastapi import FastAPI
from transformers import pipeline

app = RayCraftAPI()

@app.init
def load_model():
    return pipeline("translation_en_to_fr", model="t5-small")

@app.remote
def translate(text: str):
    model = load_model()
    translated = model(text)[0]["translation_text"]
    return translated

@app.post("/")
async def translate(app: RayCraftAPI, text: str):
    return app.translate.remote(text)
```

### Composing models


## How to setup

Using poetry:

```bash
poetry add raycraft
```

Using pip:

```bash
pip install raycraft
```

