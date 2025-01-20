from kfp.v2 import dsl
from kfp.v2.dsl import OutputPath
from kfp.components import create_component_from_func

# Component: Dummy step to write data to a file
def generate_data(output_data: OutputPath(str)):
    """Generates some dummy data and writes it to a file."""
    with open(output_data, "w") as f:
        f.write("Dummy data for testing.")

generate_data_op = create_component_from_func(
    func=generate_data,
    base_image="python:3.9"
)

# Component: Dummy step to process the generated data
def process_data(input_data: str, output_data: OutputPath(str)):
    """Processes the data and writes the result to a file."""
    with open(input_data, "r") as infile:
        data = infile.read()
    with open(output_data, "w") as outfile:
        outfile.write(f"Processed data: {data}")

process_data_op = create_component_from_func(
    func=process_data,
    base_image="python:3.9"
)

# Define the pipeline
@dsl.pipeline(
    name="simple-poc-pipeline",
    description="A simple POC pipeline to generate and process data."
)
def create_pipeline():
    # Step 1: Generate dummy data
    generated_data = generate_data_op()

    # Step 2: Process the generated data
    processed_data = process_data_op(input_data=generated_data.output)

