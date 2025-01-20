from kfp.v2.compiler import Compiler
from example1_pipeline import create_pipeline

def compile_pipeline():
    """Compile the simple POC pipeline."""
    json_output_path = "simple_poc_pipeline.json"

    # Compile the pipeline
    Compiler().compile(
        pipeline_func=create_pipeline,
        package_path=json_output_path
    )
    print(f"Pipeline compiled successfully to '{json_output_path}'.")

if __name__ == "__main__":
    compile_pipeline()