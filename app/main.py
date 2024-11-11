from fastapi import FastAPI, HTTPException
from typing import List
from app.ml_models import train_model, AVAILABLE_MODELS, load_model
from app.schemas import TrainRequest, TrainResponse, AvailableModel, PredictionRequest, PredictionResponse, HealthResponse
import pandas as pd

app = FastAPI(title="HW1 Lobachev")


@app.post("/train", response_model=TrainResponse)
def train_endpoint(request: TrainRequest):
    try:
        model_id = train_model(
            model_type=request.model_type,
            hyperparameters=request.hyperparameters,
            training_data=request.training_data
        )
        return TrainResponse(
            model_id=model_id,
            message="Модель успешно обучена."
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера.")


@app.get("/models/available", response_model=List[AvailableModel])
def get_available_models():
    models = []
    for model_type, info in AVAILABLE_MODELS.items():
        models.append(AvailableModel(
            model_type=model_type,
            description=info['description'],
            hyperparameters=info['hyperparameters']
        ))
    return models


@app.post("/predict", response_model=PredictionResponse)
def predict_endpoint(request: PredictionRequest):
    try:
        model = load_model(request.model_id)
        input_df = pd.DataFrame(request.input_data)
        predictions = model.predict(input_df).tolist()
        return PredictionResponse(predictions=predictions)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера.")
    

@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="ок",
        message="Сервис работает в норме."
    )