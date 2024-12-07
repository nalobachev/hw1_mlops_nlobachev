# HW-1
## Completed by Nikita Lobachev

This service can be used to train models, store them and predict.
To run you can use following command:
    ```bash
    poetry run uvicorn app.main:app --reload
    ```
Currently following endpoints are implemeted:
- **/train**: 
Fits the required model with given parameters and data, and stores the fitted model. Example request:
    ```json
    {
      "model_type": "decision_tree",
      "hyperparameters": {
        "criterion": "gini",
        "max_depth": 5
      },
      "training_data": [
        {"feature1": 0.1, "feature2": 1.0, "target": 0},
        {"feature1": 1.2, "feature2": 0.5, "target": 1},
        {"feature1": 0.3, "feature2": 0.8, "target": 0}
      ]
    }
    ```
- **/models/available**:
Returns the available classes of models.

- **/predict**:
Predicts an output for given model using given data. Example request:
    ```json
    {
      "model_id": "6d6f05c5-434a-4920-b01d-fecd9e4ca467",
      "input_data": [
        {"feature1": 0.1, "feature2": 0.5},
        {"feature1": 1.0, "feature2": 0.4}
      ]
    }
    ```

- **/health**:
Checks health status.


# Update:
Now its is possible to start service using docker-compose:
  ```
  docker-compose build
  doccker-compose up
  ```