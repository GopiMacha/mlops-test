import sys
import os

# Add the tfx-pipeline directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from pipelines.example_pipeline import create_pipeline
from kfp.compiler import Compiler

def compile_pipeline():
    # Define pipeline parameters
    pipeline_root = "gs://sinuous-myth-447220-m2_cloudbuild"
    data_path = "data/sample_data.csv"  # Path to the CSV data

    # Define a function to pass parameters to the pipeline
    def pipeline_func():
        return create_pipeline(pipeline_root=pipeline_root, data_path=data_path)

    # Compile the pipeline
    Compiler().compile(
        pipeline_func=pipeline_func,
        package_path="example_pipeline.yaml"
    )

def run_pipeline():
    # Placeholder for running the pipeline (if needed)
    print("Running pipeline is not implemented in this script.")

if __name__ == "__main__":
    mode = sys.argv[2]  # Get mode from command-line arguments
    if mode == "compile-pipeline":
        compile_pipeline()
    elif mode == "run-pipeline":
        run_pipeline()
