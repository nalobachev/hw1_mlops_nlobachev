import uuid
import os
import pickle
from typing import Any, Dict, List
import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# Директория для сохранения моделей
MODEL_DIR = os.path.join(os.getcwd(), 'models')

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# Словарь доступных моделей
AVAILABLE_MODELS = {
    'decision_tree': {
        'model': DecisionTreeClassifier,
        'description': 'Decision Tree Classifier',
        'hyperparameters': ['criterion', 'splitter', 'max_depth', 'min_samples_split', 'min_samples_leaf']
    },
    'random_forest': {
        'model': RandomForestClassifier,
        'description': 'Random Forest Classifier',
        'hyperparameters': ['n_estimators', 'criterion', 'max_depth', 'min_samples_split', 'min_samples_leaf']
    },
    'logistic_regression': {
        'model': LogisticRegression,
        'description': 'Logistic Regression Classifier',
        'hyperparameters': ['penalty', 'C', 'solver', 'max_iter']
    }
}


def train_model(model_type: str, hyperparameters: Dict[str, Any], training_data: List[Dict[str, Any]]) -> str:
    if model_type not in AVAILABLE_MODELS:
        raise ValueError(f"Модель {model_type} не поддерживается.")

    model_class = AVAILABLE_MODELS[model_type]['model']
    valid_hyperparams = {k: v for k, v in hyperparameters.items() if k in AVAILABLE_MODELS[model_type]['hyperparameters']}
    model = model_class(**valid_hyperparams)

    df = pd.DataFrame(training_data)
    if 'target' not in df.columns:
        raise ValueError("Данные для обучения должны содержать колонку 'target'.")

    X = df.drop(columns=['target'])
    y = df['target']

    model.fit(X, y)

    model_id = str(uuid.uuid4())
    model_path = os.path.join(MODEL_DIR, f"{model_id}.pkl")
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    return model_id


def load_model(model_id: str):
    model_path = os.path.join(MODEL_DIR, f"{model_id}.pkl")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Модель с ID {model_id} не найдена.")
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model