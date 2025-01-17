import sys
import os

# Add the tfx-pipeline directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pipelines.example_pipeline import create_pipeline
from kfp.compiler import Compiler

def compile_pipeline():
    pipeline_root = "gs://sinuous-myth-447220-m2_cloudbuild"
    data_path = "data/sample_data.csv"

    # Compile the pipeline
    Compiler().compile(
        pipeline_func=lambda: create_pipeline(pipeline_root=pipeline_root, data_path=data_path),
        package_path="example_pipeline.yaml"
    )

if __name__ == "__main__":
    import sys
    mode = sys.argv[2]  # Get mode from command-line arguments
    if mode == "compile-pipeline":
        compile_pipeline()
    else:
        print("Unsupported mode. Use 'compile-pipeline'.")
