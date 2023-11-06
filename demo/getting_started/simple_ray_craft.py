from raycraft import RayCraftAPI, App

simple_service = RayCraftAPI()


@simple_service.post("/")
async def read_root() -> dict[str, str]:
    return {"Hello": "World"}

app = simple_service()