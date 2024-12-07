import pandas as pd
import os
import subprocess

from fastapi import FastAPI, HTTPException, UploadFile
from typing import List

from app.ml_models import train_model, AVAILABLE_MODELS, load_model
from app.schemas import TrainRequest, TrainResponse, AvailableModel, PredictionRequest, PredictionResponse, HealthResponse
from app.s3_utils import upload_file_to_s3, download_file_from_s3


app = FastAPI(title="HW1-2 Lobachev")

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


# Эндпоинт для загрузки файлов в S3
@app.post("/upload-to-s3/")
async def upload_to_s3(file: UploadFile):
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    bucket_name = os.getenv("MINIO_BUCKET_NAME")
    try:
        upload_file_to_s3(file_path, bucket_name, file.filename)
        return {"message": f"File {file.filename} uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {e}")
    finally:
        os.remove(file_path)

# Эндпоинт для скачивания файлов из S3
@app.get("/download-from-s3/{file_name}")
def download_from_s3(file_name: str):
    bucket_name = os.getenv("MINIO_BUCKET_NAME")
    output_path = f"/tmp/{file_name}"
    try:
        download_file_from_s3(bucket_name, file_name, output_path)
        return {"message": f"File {file_name} downloaded successfully to {output_path}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {e}")
    

@app.post("/dvc-push/")
def dvc_push():
    try:
        result = subprocess.run(["dvc", "push"], capture_output=True, text=True)
        if result.returncode == 0:
            return {"message": "Data successfully pushed to remote storage."}
        else:
            raise HTTPException(status_code=500, detail=result.stderr)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@app.post("/dvc-pull/")
def dvc_pull():
    try:
        result = subprocess.run(["dvc", "pull"], capture_output=True, text=True)
        if result.returncode == 0:
            return {"message": "Data successfully pulled from remote storage."}
        else:
            raise HTTPException(status_code=500, detail=result.stderr)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")