import os
import sys
from kfp.compiler import Compiler

# Add the root directory (`tfx-pipeline`) to Python's module path
from example_pipeline import create_pipeline

def compile_pipeline():
    pipeline_root = "gs://sinuous-myth-447220-m2_cloudbuild"
    data_path = "data/sample_data.csv"

    # Compile the KFP pipeline
    Compiler().compile(
        pipeline_func=lambda: create_pipeline(pipeline_root=pipeline_root, data_path=data_path),
        package_path="example_pipeline.yaml"
    )

if __name__ == "__main__":
    mode = sys.argv[1]  # Get mode from command-line arguments
    if mode == "compile-pipeline":
        compile_pipeline()
    else:
        print("Unsupported mode. Use 'compile-pipeline'.")

