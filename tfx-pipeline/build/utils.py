import os
import sys
from kfp.compiler import Compiler

# Add the root directory (`tfx-pipeline`) to Python's module path
from example_pipeline import create_pipeline

def compile_pipeline():
    pipeline_root = "gs://sinuous-myth-447220-m2_cloudbuild"
    data_path = "data/sample_data.csv"
    yaml_output_path = "example_pipeline.yaml"
    json_output_path = "example_pipeline.json"

    # Compile the KFP pipeline
    Compiler().compile(
        pipeline_func=lambda: create_pipeline(pipeline_root=pipeline_root, data_path=data_path),
        package_path=yaml_output_path 
    )
    print(f"Pipeline successfully compiled to '{yaml_output_path}'.")

    # Step 2: Convert the YAML file to JSON format
    with open(yaml_output_path, "r") as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)

    with open(json_output_path, "w") as json_file:
        json.dump(yaml_data, json_file, indent=2)

    print(f"Pipeline successfully converted to JSON: '{json_output_path}'.")

if __name__ == "__main__":
    mode = sys.argv[1]  # Get mode from command-line arguments
    if mode == "compile-pipeline":
        compile_pipeline()
    else:
        print("Unsupported mode. Use 'compile-pipeline'.")

