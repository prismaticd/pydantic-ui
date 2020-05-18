from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from models import MODEL_CONFIG

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_model_config(model: str):
    klass = MODEL_CONFIG[model]["class"]
    data = MODEL_CONFIG[model]["data"]
    return klass, data


@app.get("/")
async def available_models(request: Request):
    """List all the available model pages"""
    model_names = MODEL_CONFIG.keys()
    return templates.TemplateResponse("index.html", {"request": request, "models": model_names})


@app.get("/{model}")
async def model_datatable(request: Request, model: str):
    """Datatable page for a given model"""
    return templates.TemplateResponse("datatable_view.html", {"request": request, "model": model})


@app.get("/{model}/list")
async def model_list(model: str):
    """JSON list of all instances of model"""
    klass, data = get_model_config(model)
    return klass.to_datatables(data)


@app.get("/{model}/{obj_id}/")
async def model_detail(request: Request, model: str, obj_id: str):
    """JSON model instance"""
    klass, data = get_model_config(model)
    for current_obj in data:
        current_obj_id = getattr(current_obj, klass.id_field())
        if str(current_obj_id) == obj_id:
            return templates.TemplateResponse(
                "detail_view.html",
                {
                    "request": request,
                    "id": obj_id,
                    "class_name": klass.__name__,
                    "current": current_obj.json(indent=2),
                    "schema": current_obj.to_json_editor_representation(indent=2),
                    "autocomplete": klass.all_js_autocomplete_function_paths(),
                },
            )

    raise HTTPException(404, "No such id")


@app.post("/{model}/{obj_id}/")
async def edit_item(request: Request, model: str, obj_id: str, data: dict):
    klass, _ = get_model_config(model)
    obj = klass(**data)
    return obj


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
