from typing import cast
from raycraft import App, RayCraftAPI
from transformers import pipeline, Pipeline
from pydantic import BaseModel

translator_service = RayCraftAPI(
    num_replicas=2,
    ray_actor_options={"num_cpus": 0.2, "num_gpus": 0},
)


@translator_service.init
def model() -> Pipeline:
    return pipeline("translation_en_to_fr", model="t5-small")


@translator_service.remote
def translate(app: App, text: str) -> str:
    # Run inference
    model_output = app.model(text)

    # Post-process output to return only the translation text
    translation = model_output[0]["translation_text"]

    return cast(str, translation)


class EnglishText(BaseModel):
    english_text: str


@translator_service.post("/test/")
async def ingress(app: App, english_text: EnglishText) -> str:
    return app.translate(english_text.english_text) # type: ignore


app = translator_service()

if __name__ == "__main__":
    print(app)
