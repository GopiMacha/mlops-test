import kfp
from pipelines.example_pipeline import create_pipeline

def compile_pipeline():
    pipeline_func = create_pipeline(
        pipeline_root="gs://your-bucket-name/pipeline-root",
        data_path="data/sample_data.csv"
    )
    kfp.compiler.Compiler().compile(pipeline_func, "example_pipeline.json")

def run_pipeline():
    # Code to trigger the pipeline execution
    print("Running pipeline...")

if __name__ == "__main__":
    import sys
    mode = sys.argv[2]  # Get mode from command-line arguments
    if mode == "compile-pipeline":
        compile_pipeline()
    elif mode == "run-pipeline":
        run_pipeline()
