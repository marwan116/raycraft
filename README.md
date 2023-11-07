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

You can now run it distributed with Ray using raycraft with simple changes:

```diff
+ from raycraft import RayCraftAPI

+ simple_service = RayCraftAPI()

@simple_service.post("/")
async def read_root() -> dict[str, str]:
    return {"Hello": "World"}
```

## How to use

### Basic example
Ok so an endpoint returning {"Hello": "World"} isn't going to be enough to serve as a basic example so let's try something more interesting and relevant to why you might want to use raycraft!

Let's say you build a translation service using the following fastAPI code:

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

We can now run this app with Ray Serve using raycraft `demo.py`

```python
from raycraft import RayCraftAPI
from transformers import pipeline

app = RayCraftAPI()

def load_model():
    return pipeline("translation_en_to_fr", model="t5-small")

def translate(text: str):
    model = load_model()
    translated = model(text)[0]["translation_text"]
    return translated

@app.post("/")
async def translate(text: str):
    return translate(text)    
```

We then call the following command to run the app:
```bash
raycraft run demo:app
```

Ok now for the distributed part, let's say we want to run this app on 2 replicas, each replica taking half a GPU, we can do this by running the following command:

```python
from raycraft import RayCraftAPI
from transformers import pipeline

app = RayCraftAPI(ray_actor_options={"num_gpus": 0.5}, num_replicas=2)

def load_model():
    return pipeline("translation_en_to_fr", model="t5-small")

def translate(text: str):
    model = load_model()
    translated = model(text)[0]["translation_text"]
    return translated

@app.post("/")
async def translate(text: str):
    return translate(text)    
```

To avoid loading the model on every request, we can load the model in the constructor of the app:

```python
from raycraft import RayCraftAPI, App
from transformers import pipeline

app = RayCraftAPI(ray_actor_options={"num_gpus": 0.5}, num_replicas=2)

@app.init
def model():
    return pipeline("translation_en_to_fr", model="t5-small")

def translate(text: str):
    model = load_model()
    translated = model(text)[0]["translation_text"]
    return translated

@app.post("/")
async def translate(app: App, text: str):
    return translate(text) 
```

RayCraft is built on top of [Ray Serve](https://docs.ray.io/en/latest/serve/index.html)

With Ray Serve, you can now:
- Scale your app deployment to multiple replicas running on different machines
- Define the resources allocated to each replica including fractional GPUs
- Batch requests together to improve throughput
- Get fault tolerance and automatic retries
- Stream responses using websockets
- Compose different services together using RPC calls that are strictly typed and faster than http requests

<!-- 
### Advanced example

Ok now let's say we want to improve the throughput of our translation service by batching requests together, we can do this by using the `batch` decorator:

```python
from raycraft import RayCraftAPI, App
from transformers import pipeline

app = RayCraftAPI(ray_actor_options={"num_gpus": 0.5}, num_replicas=2)

@app.init
def model():
    return pipeline("translation_en_to_fr", model="t5-small")

def translate(text: str):
    model = load_model()
    translated = model(text)[0]["translation_text"]
    return translated

@app.batch(max_batch_size=32, batch_timeout=0.1)
@app.post("/")
async def translate(app: App, text: str):
    return translate(text) 
``` -->


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


## Roadmap
- Streaming support using websockets
- Deployment guide