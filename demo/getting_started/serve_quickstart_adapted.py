from raycraft import RayServeDeployment
from starlette.requests import Request

from transformers import pipeline

translator_service = RayServeDeployment(
    num_replicas=2,
    ray_actor_options={"num_cpus": 0.2, "num_gpus": 0},
)


@translator_service.init
def model():
    return pipeline("translation_en_to_fr", model="t5-small")


@translator_service.remote
def translate(app, text: str) -> str:
    # Run inference
    model_output = app.model(text)

    # Post-process output to return only the translation text
    translation = model_output[0]["translation_text"]

    return translation


@translator_service.post  # ("/")
async def ingress(app, http_request: Request) -> str:
    english_text: str = await http_request.json()
    return app.translate(english_text)


app = translator_service()

if __name__ == "__main__":
    print(app)
