from kfp.v2.compiler import Compiler
from example_pipeline import pipeline
import google.cloud.aiplatform as aip
import sys
import os

def compile_pipeline(pipeline_file: str):
    """Compiles the pipeline to a YAML file."""
    Compiler().compile(
        pipeline_func=pipeline,
        package_path=pipeline_file,
    )
    print(f"Pipeline compiled successfully to '{pipeline_file}'.")

def run_pipeline(
    project_id: str,
    region: str,
    bucket_uri: str,
    pipeline_file: str,
    import_file: str,
    display_name: str,
):
    """Runs the compiled pipeline on Vertex AI."""
    pipeline_root = f"{bucket_uri}/pipeline_root"
    aip.init(project=project_id, staging_bucket=bucket_uri)

    job = aip.PipelineJob(
        display_name=display_name,
        template_path=pipeline_file,
        pipeline_root=pipeline_root,
        parameter_values={
            "project": project_id,
            "region": region,
            "import_file": import_file,
            "display_name": display_name,
            "pipeline_root": pipeline_root,
        },
    )

    print(f"Starting pipeline: {display_name}")
    job.run()

if __name__ == "__main__":
    # Define pipeline parameters
    PROJECT_ID = os.getenv("PROJECT_ID", "your-project-id")
    REGION = os.getenv("REGION", "us-central1")
    BUCKET_URI = os.getenv("BUCKET_URI", "gs://your-bucket-name")
    IMPORT_FILE = "gs://sinuous-creditcards-dev/happiness.csv"
    DISPLAY_NAME = "automl-text-classification"
    PIPELINE_FILE = "text_classification_pipeline.yaml"

    # Determine mode (compile or run)
    mode = sys.argv[1] if len(sys.argv) > 1 else "compile"

    if mode == "compile":
        compile_pipeline(PIPELINE_FILE)
    elif mode == "run":
        run_pipeline(
            project_id=PROJECT_ID,
            region=REGION,
            bucket_uri=BUCKET_URI,
            pipeline_file=PIPELINE_FILE,
            import_file=IMPORT_FILE,
            display_name=DISPLAY_NAME,
        )
    else:
        print(f"Unsupported mode: {mode}")
