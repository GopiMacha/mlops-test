import sys
from kfp.v2 import Client

def run_pipeline(pipeline_gcs_path: str, region: str, project_id: str):
    """
    Trigger the pipeline run using the compiled pipeline stored in GCS.
    Args:
        pipeline_gcs_path (str): GCS path to the compiled pipeline YAML file (e.g., gs://...).
        region (str): Google Cloud region where Vertex AI Pipelines is deployed.
        project_id (str): Google Cloud project ID.
    """
    try:
        # Initialize the KFP client for Vertex AI Pipelines
        client = Client(host=f"https://{region}-kfp.googleapis.com",
                        project_id=project_id)
        print(f"KFP Client initialized for project: {project_id}, region: {region}")

        # Define pipeline parameters if applicable (modify as per your pipeline needs)
        pipeline_parameters = {
            # Example parameters if your pipeline accepts any
            # 'input_data': 'gs://your-bucket/data.csv',
        }

        # Submit the pipeline run using the GCS path
        run = client.create_run_from_job_spec(
            job_spec_path=pipeline_gcs_path,
            arguments=pipeline_parameters
        )

        # Print run details
        print(f"Pipeline submitted successfully. Run ID: {run.run_id}")
        print(f"Run details: {run.url}")

    except Exception as e:
        print(f"Error running pipeline: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python utils.py <mode> [args]")
        sys.exit(1)

    mode = sys.argv[1]  # Get mode from command-line arguments

    if mode == "run-pipeline":
        if len(sys.argv) != 5:
            print("Usage: python utils.py run-pipeline <pipeline-gcs-path> <region> <project-id>")
            sys.exit(1)
        pipeline_gcs_path = sys.argv[2]
        region = sys.argv[3]
        project_id = sys.argv[4]
        run_pipeline(pipeline_gcs_path, region, project_id)
    else:
        print("Unsupported mode. Use 'run-pipeline'.")
