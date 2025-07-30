import mlflow
import os
import logging
from datetime import datetime
import pandas as pd
from ultralytics import YOLO, settings
 
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
settings.update({"mlflow": False})
 
class TrackModel:
    def __init__(self, experiment_name, run_name=None):
        self.experiment_name = experiment_name
        self.run_name = run_name or f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.run = None
 
    def __enter__(self):
        try:
            mlflow.set_tracking_uri("http://mlflow-service.mlflow.svc.cluster.local:5000")
            mlflow.set_experiment(self.experiment_name)
            self.run = mlflow.start_run(run_name=self.run_name)
            logging.info(f"Started MLflow run: {self.run.info.run_id}")
            return self
        except Exception as e:
            logging.exception(f"Failed to start MLflow run: {e}")
            raise
 
    def log_param(self, name, value):
        try:
            mlflow.log_param(name, value)
            logging.info(f"Logged param: {name} = {value}")
        except Exception as e:
            logging.exception(f"Error logging param {name}: {e}")
 
    def log_metric(self, name, value):
        try:
            mlflow.log_metric(name, value)
            logging.info(f"Logged metric: {name} = {value}")
        except Exception as e:
            logging.exception(f"Error logging metric {name}: {e}")
 
    def log_artifact(self, artifact_path):
        try:
            if os.path.exists(artifact_path):
                if os.path.isdir(artifact_path):
                    for root, _, files in os.walk(artifact_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            relative_path = os.path.relpath(file_path, artifact_path)
                            mlflow.log_artifact(file_path, artifact_path=os.path.dirname(relative_path))
                else:
                    mlflow.log_artifact(artifact_path)
                logging.info(f"Logged artifact: {artifact_path}")
            else:
                logging.warning(f"Artifact path '{artifact_path}' does not exist.")
        except Exception as e:
            logging.exception(f"Error logging artifact {artifact_path}: {e}")
 
    def read_results_as_dataframe(self, path):
        logging.info(f"Reading results from: {path}")
        try:
            return pd.read_csv(path)
        except Exception as e:
            logging.exception(f"Failed to read results CSV: {e}")
            raise
 
    def extract_metrics_from_dataframe(self, df):
        metrics = {}
        if df.empty:
            logging.warning("Empty DataFrame. No metrics extracted.")
            return metrics
        try:
            latest_row = df.iloc[-1]
            metrics = {
                'lr/pg0': latest_row.get('lr/pg0'),
                'lr/pg1': latest_row.get('lr/pg1'),
                'lr/pg2': latest_row.get('lr/pg2'),
                'train/box_loss': latest_row.get('train/box_loss'),
                'train/cls_loss': latest_row.get('train/cls_loss'),
                'train/dfl_loss': latest_row.get('train/dfl_loss'),
                'val/box_loss': latest_row.get('val/box_loss'),
                'val/cls_loss': latest_row.get('val/cls_loss'),
                'val/dfl_loss': latest_row.get('val/dfl_loss'),
                'metrics/mAP50-95B': latest_row.get('metrics/mAP50(B)'),
                'metrics/mAP50B': latest_row.get('metrics/mAP50-95(B)'),
                'metrics/precisionB': latest_row.get('metrics/precision(B)'),
                'metrics/recallB': latest_row.get('metrics/recall(B)')
            }
        except Exception as e:
            logging.exception(f"Error extracting metrics from DataFrame: {e}")
        return metrics
 
    def log_training_parameters(self, train_dataset_path, epochs, imgsz):
        try:
            num_train_images = len([
                f for f in os.listdir(train_dataset_path)
                if os.path.isfile(os.path.join(train_dataset_path, f))
            ])
            self.log_param("num_train_images", num_train_images)
            self.log_param("epochs", epochs)
            self.log_param("imgsz", imgsz)
        except Exception as e:
            logging.exception(f"Error logging training parameters: {e}")
            
    def log_validate_parameters(self, valid_dataset_path):
        try:
            num_valid_images = len([
                f for f in os.listdir(valid_dataset_path)
                if os.path.isfile(os.path.join(valid_dataset_path, f))
            ])
            self.log_param("num_valid_images", num_valid_images)
        except Exception as e:
            logging.exception(f"Error logging valid parameters: {e}")
 
    def log_training_metrics_and_artifacts(self, output_dir, model_path, results):
        try:
            results_csv = os.path.join(output_dir, model_path, "results.csv")
            df = self.read_results_as_dataframe(results_csv)
            metrics = self.extract_metrics_from_dataframe(df)
            for name, value in metrics.items():
                if value is not None:
                    self.log_metric(name, value)
            self.log_artifact(results.save_dir)
            logging.info(f"Training complete. Artifacts logged from: {results.save_dir}")
            return results.save_dir
        except Exception as e:
            logging.exception(f"Error during logging metrics and artifacts: {e}")
            raise
            
    def log_validate_metrics_and_artifacts(self, results):
        try:
            logging.info("Model validation started.")
            if hasattr(results, 'results_dict'):
                metrics = results.results_dict
                for metric, value in metrics.items():
                    safe_metric = metric.replace("(", "_").replace(")", "").replace("/", "_")
                    self.log_metric(safe_metric, value)
                logging.info("Validation metrics logged to MLflow.")

            self.log_artifact(results.save_dir)
            logging.info(f"Validation complete. Artifacts logged from: {results.save_dir}")
            return results.save_dir
        except Exception as e:
            logging.exception(f"Error during logging validation metrics and artifacts: {e}")
            raise
            
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            mlflow.end_run()
            logging.info("MLflow run ended.")
        except Exception as e:
            logging.exception("Error ending MLflow run: {e}")