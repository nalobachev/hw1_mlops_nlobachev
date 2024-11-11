from typing import Any, Dict, List
from pydantic import BaseModel

class TrainRequest(BaseModel):
    model_type: str
    hyperparameters: Dict[str, Any] = {}
    training_data: List[Dict[str, Any]]

class TrainResponse(BaseModel):
    model_id: str
    message: str

class PredictionRequest(BaseModel):
    model_id: str
    input_data: List[Dict[str, Any]]

class PredictionResponse(BaseModel):
    predictions: List[Any]

class AvailableModel(BaseModel):
    model_type: str
    description: str
    hyperparameters: List[str]

class HealthResponse(BaseModel):
    status: str
    message: str