import json
import logging
import os
import shutil
import zipfile
from typing import Any, Dict, List, Optional

import requests


def find_performance_artifact(
    artifacts_data: Dict[str, Any], run_id: str, artifact_prefix: str
) -> Optional[Dict[str, Any]]:
    """
    Finds the performance artifact within the artifacts data.
    (Name kept as is as it's specifically for performance artifacts)
    """
    for artifact in artifacts_data.get("artifacts", []):
        if artifact["name"] == f"{artifact_prefix}_{run_id}":
            return artifact
    return None


def extract_json_from_zip(zip_path: str, extract_dir: str) -> List[str]:
    """
    Extracts all JSON files from a zip archive to the specified directory and
    returns a list of paths to the extracted JSON files.
    """
    extracted_json_files: List[str] = []
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)
        extracted_files: List[str] = zip_ref.namelist()
        extracted_json_files = [
            os.path.join(extract_dir, file)
            for file in extracted_files
            if file.endswith(".json")
        ]  # Return full path
    return extracted_json_files


def load_json_file(json_path: str) -> Dict[str, Any]:
    """
    Loads data from a JSON file.
    (Renamed for clarity - was load_metrics_from_json, now more general)
    """
    try:
        with open(json_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"JSON file not found: {json_path}")
        raise
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from: {json_path}")
        raise


def save_json_file(data: Dict[str, Any], output_dir: str, filename: str) -> str:
    """
    Saves data to a JSON file in the specified output directory.
    """
    result_path: str = os.path.join(output_dir, filename)
    try:
        os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists
        with open(result_path, "w") as result_file:
            json.dump(data, result_file, indent=4)
        logging.info(f"Data saved to JSON: {result_path}")
        return result_path  # Return path to saved file
    except OSError as e:
        logging.error(f"Error saving JSON to {result_path}: {e}")
        raise


def download_zip_file(
    api_client: Any, artifact_id: int, output_dir: str, zip_filename: str
) -> str:
    """
    Downloads a zip file artifact from GitHub API by its ID and saves it to the output directory.
    """
    artifact_zip_path: str = os.path.join(
        output_dir, f"{zip_filename}.zip"
    )  # Use zip_filename param
    try:
        os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists
        download_response: requests.Response = api_client.download_artifact(
            artifact_id
        )  # Assuming api_client.download_artifact is still used
        with open(artifact_zip_path, "wb") as f:
            f.write(download_response.content)
        logging.info(f"Downloaded zip file to: {artifact_zip_path}")
        return artifact_zip_path  # Return path to downloaded zip
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading zip file: {e}")
        raise


def cleanup_zip_file(zip_path: str) -> None:
    """
    Deletes a zip file.
    (More general name - was cleanup_artifact_zip, now cleanup_zip_file)
    """
    try:
        os.remove(zip_path)
        logging.info(f"Deleted zip file: {zip_path}")
    except OSError as e:
        logging.error(f"Error deleting zip file {zip_path}: {e}")
        raise


def cleanup_output_dir(output_dir: str) -> None:
    """Removes the specified output directory if it exists."""
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
