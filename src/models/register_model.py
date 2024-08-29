import sys
import mlflow
from mlflow.tracking import MlflowClient
import os
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.utils.logging_config import setup_logging

def main():
    # Load environment variables
    load_dotenv()
    logger.info("Environment variables loaded.")

    # Retrieve environment variables
    dagshub_username = os.getenv('DAGSHUB_USERNAME')
    dagshub_token = os.getenv('DAGSHUB_TOKEN')
    repo_owner = os.getenv('REPO_OWNER')
    repo_name = os.getenv('REPO_NAME')

    if not all([dagshub_username, dagshub_token, repo_owner, repo_name]):
        logger.error("Please set all required environment variables.")
        return

    # Configure MLflow
    os.environ['MLFLOW_TRACKING_USERNAME'] = dagshub_username
    os.environ['MLFLOW_TRACKING_PASSWORD'] = dagshub_token

    mlflow.set_tracking_uri(f"https://dagshub.com/{repo_owner}/{repo_name}.mlflow")
    logger.info("MLflow configured successfully.")

    # Define the model name
    model_name = "iris_classification_model"

    # Retrieve the latest run ID
    client = MlflowClient()
    experiment = client.get_experiment_by_name("iris_classification")
    if experiment is None:
        logger.error("Experiment 'iris_classification' not found.")
        return

    runs = client.search_runs(experiment_ids=[experiment.experiment_id], order_by=["start_time DESC"], max_results=1)
    if not runs:
        logger.error("No runs found for the experiment.")
        return

    latest_run = runs[0]
    run_id = latest_run.info.run_id
    logger.info(f"Latest run ID: {run_id}")

    # Register the model
    model_uri = f"runs:/{run_id}/model"
    model_details = mlflow.register_model(model_uri, model_name)

    # Transition the model to production stage
    client.transition_model_version_stage(
        name=model_name,
        version=model_details.version,
        stage="Production"
    )

    logger.info(f"Model {model_name} version {model_details.version} is now in Production")

if __name__ == "__main__":
    # Configure the logger
    logger = setup_logging()

    # Start the script
    logger.info("Starting the script...")
    main()
    logger.info("Script finished.")