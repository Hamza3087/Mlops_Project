import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
import pandas as pd
import pickle

def train_model():
    # Load data
    df = pd.read_csv("processed_data.csv")
    X = df[["Humidity", "Wind Speed"]]
    y = df["Temperature"]
    
    # Model training
    model = LinearRegression()
    model.fit(X, y)
    
    # Log model and metrics to MLFlow
    mlflow.set_tracking_uri("http://127.0.0.1:5000")  # Ensure this is correct
    mlflow.set_experiment("Weather Prediction Experiment")
    
    with mlflow.start_run():
        mlflow.log_param("model_type", "LinearRegression")
        mlflow.log_metric("r2_score", model.score(X, y))
        mlflow.sklearn.log_model(model, "model")

        # Register model in MLFlow
        model_name = "Weather Prediction Model"
        mlflow.register_model(f"runs:/{mlflow.active_run().info.run_id}/model", model_name)

        # Save model locally
        with open("model.pkl", "wb") as f:
            pickle.dump(model, f)

if __name__ == "__main__":
    train_model()