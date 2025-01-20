from kfp.v2.compiler import Compiler
from example_pipeline import create_pipeline

def compile_pipeline():
    """Compile the pipeline into a PipelineJob JSON for Vertex AI Pipelines."""
    pipeline_root = "gs://sinuous-myth-447220-m2_cloudbuild"
    data_path = "data/sample_data.csv"
    json_output_path = "example_pipeline.json"

    # Compile the pipeline into a PipelineJob JSON file
    Compiler().compile(
        pipeline_func=lambda: create_pipeline(
            pipeline_root=pipeline_root,
            data_path=data_path
        ),
        package_path=json_output_path
    )
    print(f"Pipeline successfully compiled to '{json_output_path}'.")

if __name__ == "__main__":
    compile_pipeline()
