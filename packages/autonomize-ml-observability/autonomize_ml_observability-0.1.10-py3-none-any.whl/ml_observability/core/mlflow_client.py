"""MLflow client implementation for modelhub-observability SDK."""

import os
from contextlib import contextmanager
from typing import Any, Dict, Generator, Optional

import mlflow

from ml_observability.core.base_client import BaseClient
from ml_observability.core.credential import ModelhubCredential
from ml_observability.core.exceptions import ModelHubAPIException
from ml_observability.utils import setup_logger

logger = setup_logger(__name__)


class MLflowClient(BaseClient):
    """Client for interacting with MLflow via Modelhub API."""

    def __init__(
            self,
            credential: Optional[ModelhubCredential] = None,
            copilot_client_id: Optional[str] = None,
            copilot_id: Optional[str] = None,
            timeout: int = 10,
            verify_ssl: bool = True,
            base_url: Optional[str] = None,
            direct_tracking_uri: Optional[str] = None,
    ):
        """
        Initialize the MLflowClient.

        Args:
            credential: ModelhubCredential for authentication (or base URL if string)
            copilot_client_id: Optional client ID
            copilot_id: Optional copilot ID
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
            base_url: Base URL for Modelhub API (alternative to credential)
            direct_tracking_uri: Direct MLflow tracking URI (bypass Modelhub API)
        """
        self.direct_tracking_uri = direct_tracking_uri

        # If we have a direct tracking URI, we'll use that instead of Modelhub API
        if direct_tracking_uri:
            self._initialize_direct_mlflow(direct_tracking_uri)
            # We still need a dummy credential for the BaseClient
            if credential is None and base_url is None:
                dummy_url = "https://dummy.modelhub.url"
                credential = ModelhubCredential(modelhub_url=dummy_url, token="dummy")

        # Handle base_url as an alternative to credential
        if credential is None and base_url is not None:
            credential = ModelhubCredential(modelhub_url=base_url)

        # Handle string credential
        if isinstance(credential, str):
            credential = ModelhubCredential(modelhub_url=credential)

        # Initialize the base client
        super().__init__(credential, copilot_client_id, copilot_id, timeout, verify_ssl)

        # If using Modelhub API, configure MLflow through it
        if not direct_tracking_uri:
            self.configure_mlflow()

    def _initialize_direct_mlflow(self, tracking_uri: str) -> None:
        """
        Initialize MLflow directly with a tracking URI.

        Args:
            tracking_uri: MLflow tracking URI
        """
        try:
            mlflow.set_tracking_uri(tracking_uri)
            logger.debug("Set MLflow tracking URI directly to: %s", tracking_uri)
            # Check if credentials are provided via environment variables
            username = os.getenv("MLFLOW_TRACKING_USERNAME")
            password = os.getenv("MLFLOW_TRACKING_PASSWORD")
            if username and password:
                mlflow.set_registry_uri(tracking_uri)
                logger.debug("Using MLflow credentials from environment")
        except Exception as e:
            logger.error("Failed to initialize MLflow with direct tracking URI: %s", str(e))
            raise

    def configure_mlflow(self) -> None:
        """
        Configure MLflow settings through Modelhub API.
        """
        try:
            response = self.get("mlflow/tracking_uri")
            logger.debug("MLflow tracking URI from API: %s", response)
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
            logger.error("Failed to configure MLflow through API: %s", str(e))
            raise ModelHubAPIException(f"Failed to configure MLflow: {str(e)}")

    @contextmanager
    def start_run(
            self,
            run_name: Optional[str] = None,
            nested: bool = False,
            tags: Optional[Dict[str, str]] = None,
            output_path: str = "/tmp",
    ) -> Generator[mlflow.ActiveRun, None, None]:
        """
        Context manager for starting an MLflow run.

        Args:
            run_name: Name of the run
            nested: Whether the run is nested
            tags: Tags for the run
            output_path: Path to write run ID

        Yields:
            Active MLflow run
        """
        logger.debug("Starting MLflow run with name: %s", run_name)

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
        """
        End the current MLflow run.

        Args:
            status: Status of the run
        """
        mlflow.end_run(status=status)
        logger.debug("Ended MLflow run with status: %s", status)

    def get_previous_stage_run_id(self, output_path: str = "/tmp") -> str:
        """
        Get the run ID of the previous stage.

        Args:
            output_path: Path containing the run ID file

        Returns:
            Run ID
        """
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
        """
        Set the active experiment.

        Args:
            experiment_name: Name of the experiment
            experiment_id: ID of the experiment
        """
        mlflow.set_experiment(experiment_name, experiment_id)
        logger.debug("Set experiment: name=%s, id=%s", experiment_name, experiment_id)

    def log_param(self, key: str, value: Any) -> None:
        """
        Log a parameter.

        Args:
            key: Parameter name
            value: Parameter value
        """
        mlflow.log_param(key, value)
        logger.debug("Logged parameter: %s=%s", key, value)

    def log_metric(self, key: str, value: float, step: Optional[int] = None) -> None:
        """
        Log a metric.

        Args:
            key: Metric name
            value: Metric value
            step: Step for the metric
        """
        mlflow.log_metric(key, value, step=step)
        logger.debug("Logged metric: %s=%f", key, value)

    def log_artifact(
            self,
            local_path: str,
            artifact_path: Optional[str] = None,
            run_id: Optional[str] = None,
    ) -> None:
        """
        Log an artifact.

        Args:
            local_path: Path to the artifact
            artifact_path: Path within MLflow artifact storage
            run_id: Optional run ID
        """
        mlflow.log_artifact(local_path, artifact_path, run_id)
        logger.debug("Logged artifact: %s", local_path)

    def get_run(self, run_id: str) -> Dict[str, Any]:
        """
        Get the run details.

        Args:
            run_id: Run ID

        Returns:
            Run details
        """
        run = mlflow.get_run(run_id)
        logger.debug("Retrieved run: %s", run_id)
        return run.to_dictionary()

    def load_model(self, model_uri: str) -> Any:
        """
        Load the model from the specified URI.

        Args:
            model_uri: Model URI

        Returns:
            Loaded model
        """
        logger.debug("Loading model from: %s", model_uri)
        return mlflow.pyfunc.load_model(model_uri)

    def save_model(self, model: Any, model_path: str) -> None:
        """
        Save the model to the specified path.

        Args:
            model: Model to save
            model_path: Path to save the model
        """
        logger.debug("Saving model to: %s", model_path)
        mlflow.pyfunc.save_model(model, model_path)

    @property
    def mlflow(self) -> Any:
        """
        Returns the mlflow module.

        Returns:
            mlflow: The MLflow module instance
        """
        return mlflow

    def __enter__(self) -> "MLflowClient":
        """Support using client as a context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Cleanup when exiting context."""
        self.end_run()