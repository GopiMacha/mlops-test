import sys
import os
from kfp.compiler import Compiler
from pipelines.example_pipeline import create_pipeline

def compile_pipeline():
    pipeline_root = "gs://sinuous-myth-447220-m2_cloudbuild"
    data_path = "data/sample_data.csv"

    # Compile the pipeline directly
    Compiler().compile(
        pipeline_func=lambda: create_pipeline(pipeline_root=pipeline_root, data_path=data_path),
        package_path="example_pipeline.yaml"
    )

def run_pipeline():
    # Placeholder for triggering the pipeline execution
    print("Running pipeline is not implemented in this script.")

if __name__ == "__main__":
    mode = sys.argv[2]  # Get mode from command-line arguments
    if mode == "compile-pipeline":
        compile_pipeline()
    elif mode == "run-pipeline":
        run_pipeline()
