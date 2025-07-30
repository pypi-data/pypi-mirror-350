""" Client for interacting with MLflow. """

import logging
import os
from contextlib import contextmanager
from typing import Any, Dict, Generator, Optional

import mlflow

from modelhub.core import BaseClient, ModelhubCredential

logger = logging.getLogger(__name__)


class MLflowClient(BaseClient):
    """Client for interacting with MLflow."""

    def __init__(
        self,
        credential: ModelhubCredential,
        client_id: Optional[str] = None,
        copilot_id: Optional[str] = None,
        timeout: int = 10,
        verify_ssl: bool = True,
    ):
        """Initialize the MLflowClient."""
        super().__init__(credential, client_id, copilot_id, timeout, verify_ssl)
        self.configure_mlflow()

    def configure_mlflow(self) -> None:
        """Configure MLflow settings."""
        try:
            response = self.get("mlflow/tracking_uri")
            logger.info(f"MLflow tracking uri: {response}")
            tracking_uri = response.get("tracking_uri")
            if not tracking_uri:
                logger.error("Tracking URI not found in response")
                raise ValueError("Tracking URI not found in response")

            mlflow.set_tracking_uri(tracking_uri)
            logger.debug("Set MLflow tracking URI to: %s", tracking_uri)

            response = self.get("mlflow/credentials")
            username = response.get("username")
            password = response.get("password")

            if username and password:
                mlflow.set_registry_uri(tracking_uri)
                os.environ["MLFLOW_TRACKING_USERNAME"] = username
                os.environ["MLFLOW_TRACKING_PASSWORD"] = password
                logger.debug("Set MLflow credentials")
        except Exception as e:
            logger.error("Failed to configure MLflow: %s", str(e))
            raise

    @contextmanager
    def start_run(
        self,
        run_name: Optional[str] = None,
        nested: bool = False,
        tags: Optional[Dict[str, str]] = None,
        output_path: str = "/tmp",
    ) -> Generator[mlflow.ActiveRun, None, None]:
        """Context manager for starting an MLflow run."""
        logger.info("Starting MLflow run with name: %s", run_name)

        try:
            os.makedirs(output_path, exist_ok=True)
            logger.debug("Created output directory: %s", output_path)
        except OSError as e:
            logger.error(
                "Failed to create output directory '%s': %s", output_path, str(e)
            )
            raise

        try:
            with mlflow.start_run(run_name=run_name, nested=nested, tags=tags) as run:
                run_id = run.info.run_id
                run_id_path = os.path.join(output_path, "run_id")

                try:
                    with open(run_id_path, "w", encoding="utf-8") as f:
                        f.write(run_id)
                    logger.debug("Wrote run_id to: %s", run_id_path)
                except OSError as e:
                    logger.error(
                        "Failed to write run_id to '%s': %s", run_id_path, str(e)
                    )
                    raise

                yield run

        except Exception as e:
            logger.error("Error during MLflow run: %s", str(e))
            raise

    def end_run(self, status: str = "FINISHED") -> None:
        """End the current MLflow run."""
        mlflow.end_run(status=status)
        logger.debug("Ended MLflow run with status: %s", status)

    def get_previous_stage_run_id(self, output_path: str = "/tmp") -> str:
        """Get the run ID of the previous stage."""
        run_id_path = os.path.join(output_path, "run_id")
        try:
            with open(run_id_path, "r", encoding="utf-8") as f:
                run_id = f.read().strip()
            logger.debug("Retrieved previous stage run_id: %s", run_id)
            return run_id
        except FileNotFoundError:
            logger.error("Run ID file not found at: %s", run_id_path)
            raise

    def set_experiment(
        self, experiment_name: Optional[str] = None, experiment_id: Optional[str] = None
    ) -> None:
        """Set the active experiment."""
        mlflow.set_experiment(experiment_name, experiment_id)
        logger.debug("Set experiment: name=%s, id=%s", experiment_name, experiment_id)

    def log_param(self, key: str, value: Any) -> None:
        """Log a parameter."""
        mlflow.log_param(key, value)
        logger.debug("Logged parameter: %s=%s", key, value)

    def log_metric(self, key: str, value: float) -> None:
        """Log a metric."""
        mlflow.log_metric(key, value)
        logger.debug("Logged metric: %s=%f", key, value)

    def log_artifact(
        self,
        local_path: str,
        artifact_path: Optional[str] = None,
        run_id: Optional[str] = None,
    ) -> None:
        """Log an artifact."""
        mlflow.log_artifact(local_path, artifact_path, run_id)
        logger.debug("Logged artifact: %s", local_path)

    def get_run(self, run_id: str) -> Dict[str, Any]:
        """Get the run details."""
        run = mlflow.get_run(run_id)
        logger.debug("Retrieved run: %s", run_id)
        return run.to_dictionary()

    def load_model(self, model_uri: str) -> Any:
        """Load the model from the specified URI."""
        logger.debug("Loading model from: %s", model_uri)
        return mlflow.pyfunc.load_model(model_uri)

    def save_model(self, model: Any, model_path: str) -> None:
        """Save the model to the specified path."""
        logger.debug("Saving model to: %s", model_path)
        mlflow.pyfunc.save_model(model, model_path)

    @property
    def mlflow(self) -> mlflow:
        """
        Returns the mlflow module.

        Returns:
            mlflow: The MLflow module instance.
        """
        return mlflow

    def __enter__(self) -> "MLflowClient":
        """Support using client as a context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Cleanup when exiting context."""
        self.end_run()
