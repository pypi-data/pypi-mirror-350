import os
import yaml
import tempfile
import zipfile
from pathlib import Path
from dotenv import load_dotenv
import requests
from typing import Optional
from datetime import datetime, timedelta
load_dotenv()  # This loads the .env file

S3_URL = "https://u3mvtbirxf.us-east-1.awsapprunner.com"
JOB_URL = "https://simplex--job-scheduler-app-handler.modal.run"

def read_config(directory: str) -> dict:
    """Read and validate the simplex.yaml configuration file"""
    config_path = Path(directory) / "simplex.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"No simplex.yaml found in {directory}")
    
    with open(config_path) as f:
        return yaml.safe_load(f)


def create_archive(directory: str, config: dict) -> str:
    """Create a temporary zip archive of the entire directory"""
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp:
        with zipfile.ZipFile(tmp.name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            base_path = Path(directory)
            
            # Walk through all files and directories
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = Path(root) / file
                    # Get path relative to the base directory
                    relative_path = file_path.relative_to(base_path)
                    # Add file to zip with its relative path
                    zip_file.write(file_path, arcname=str(relative_path))
                    
        return tmp.name

def push_directory(directory: str):
    """Main function to handle parsing yaml and creating zip archive"""
    config = read_config(directory)
    archive_path = create_archive(directory, config)
    
    project_name = config.get('name')
    if not project_name:
        raise ValueError("Project name not specified in simplex.yaml")
    
    cron_schedule = config.get("cron_schedule", None)
    if not cron_schedule:
        raise ValueError("Cron schedule not specified in simplex.yaml")
    
    try:
        s3_uri = upload_files_to_s3(archive_path, project_name)
    except Exception as e:
        print(f"Error uploading project: {e}")
        raise
    finally:
        os.unlink(archive_path)

    try:
        create_job_scheduled(project_name, cron_schedule, s3_uri)
    except Exception as e:
        print(f"Error creating job: {e}")
        raise
    finally:
        print("Successfully created job!")
    
    

def upload_files_to_s3(archive_path: str, project_name: str):
    # Read API key from environment
    api_key = os.getenv('SIMPLEX_API_KEY')
    if not api_key:
        raise ValueError("SIMPLEX_API_KEY environment variable not set")

    url = S3_URL + "/upload_files_to_s3"

    try:
        # Prepare the multipart form data
        files = {
            'zip_file': ('archive.zip', open(archive_path, 'rb'), 'application/zip')
        }
        data = {
            'project_name': project_name,
        }
        headers = {
            'x-api-key': api_key
        }

        # Make the POST request
        response = requests.post(
            url,
            files=files,
            data=data,
            headers=headers
        )
    
        # Check response
        response.raise_for_status()
        result = response.json()
        print(f"Successfully uploaded project: {result['project_name']}")
        return result['s3_uri']
    except Exception as e:
        print(f"Error uploading project: {e}")
        raise

def create_job_scheduled(project_name: str, cron_schedule: str, s3_uri: str):
    """Create a new job via the API"""
    # Read API key from environment
    api_key = os.getenv('SIMPLEX_API_KEY')
    if not api_key:
        raise ValueError("SIMPLEX_API_KEY environment variable not set")

    url = JOB_URL + "/api/v1/jobs/"

    try:
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': api_key
        }

        data = {
            'name': project_name,
            's3_uri': s3_uri,
            'cron_schedule': cron_schedule
        }

        response = requests.post(
            url,
            json=data,
            headers=headers
        )

        # Check response
        response.raise_for_status()
        result = response.json()
        print(f"Successfully created job: {result['name']}")
        return result

    except Exception as e:
        print(f"Error creating job: {e}")
        raise

    
def create_job_immediately(project_name: str, s3_uri: str):
    """Create a new job via the API"""
    # Read API key from environment
    api_key = os.getenv('SIMPLEX_API_KEY')
    if not api_key:
        raise ValueError("SIMPLEX_API_KEY environment variable not set")

    url = JOB_URL + "/api/v1/jobs/"
    

    try:
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': api_key
        }

        data = {
            'name': project_name,
            's3_uri': s3_uri,
            'schedule_time': (datetime.utcnow() + timedelta(minutes=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
        }

        response = requests.post(
            url,
            json=data,
            headers=headers
        )

        # Check response
        response.raise_for_status()
        result = response.json()
        print(f"Successfully created job: {result['name']}")
        return result

    except Exception as e:
        print(f"Error creating job: {e}")
        raise

def run_directory(directory: str):
    """Run a directory immediately"""
    config = read_config(directory)
    archive_path = create_archive(directory, config)
    
    project_name = config.get('name')
    if not project_name:
        raise ValueError("Project name not specified in simplex.yaml")
    
    try:
        s3_uri = upload_files_to_s3(archive_path, project_name)
    except Exception as e:
        print(f"Error uploading project: {e}")
        raise

    finally:
        os.unlink(archive_path)

    try:
        create_job_immediately(project_name, s3_uri)
    except Exception as e:
        print(f"Error creating job: {e}")
        raise