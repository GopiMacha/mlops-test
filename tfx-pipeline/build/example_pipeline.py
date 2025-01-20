from kfp.v2 import dsl
from kfp.v2.dsl import OutputPath
from kfp.components import create_component_from_func

# Component: Load and process CSV data
def load_csv(input_base: str, output_data: OutputPath(str)):
    """Loads and copies CSV data."""
    import os
    import shutil
    os.makedirs(output_data, exist_ok=True)
    shutil.copytree(input_base, output_data)

csv_example_gen_op = create_component_from_func(
    func=load_csv,
    base_image="python:3.9",
)

# Component: Train a machine learning model
def train_model(training_data: str, model_output: OutputPath(str)):
    """Trains a simple model using the training data."""
    import os
    os.makedirs(model_output, exist_ok=True)
    with open(os.path.join(model_output, "model.txt"), "w") as f:
        f.write(f"Trained model using data at {training_data}")

trainer_op = create_component_from_func(
    func=train_model,
    base_image="python:3.9",
)

# Component: Push the trained model to a deployment location
def push_model(model: str, deployment: OutputPath(str)):
    """Pushes the trained model to a deployment directory."""
    import os
    import shutil
    os.makedirs(deployment, exist_ok=True)
    shutil.copytree(model, deployment)

pusher_op = create_component_from_func(
    func=push_model,
    base_image="python:3.9",
)

# Define the pipeline
@dsl.pipeline(
    name="example-pipeline",
    description="A pipeline for loading CSV data, training a model, and deploying it."
)
def create_pipeline(
    pipeline_root: str,
    data_path: str
):
    # Step 1: Load CSV data
    example_gen = csv_example_gen_op(
        input_base=data_path,
        output_data=f"{pipeline_root}/example_gen_output"
    )

    # Step 2: Train the model
    trainer = trainer_op(
        training_data=example_gen.output,  # Use default single output
        model_output=f"{pipeline_root}/trainer_output"
    )

    # Step 3: Deploy the trained model
    pusher = pusher_op(
        model=trainer.output,  # Use default single output
        deployment=f"{pipeline_root}/pusher_output"
    )