import sys
import os

# Add the tfx-pipeline directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

import kfp
from pipelines.example_pipeline import create_pipeline

def compile_pipeline():
    pipeline_func = create_pipeline(
        pipeline_root="gs://sinuous-myth-447220-m2_cloudbuild",
        data_path="data/sample_data.csv"
        model_push_path="./model_deploy",  
    )
    kfp.compiler.Compiler().compile(pipeline_func, "example_pipeline.json")

def run_pipeline():
    # Code to trigger the pipeline execution
    print("Running pipeline...")

if __name__ == "__main__":
    mode = sys.argv[2]  # Get mode from command-line arguments
    if mode == "compile-pipeline":
        compile_pipeline()
    elif mode == "run-pipeline":
        run_pipeline()
