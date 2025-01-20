from kfp.v2 import dsl
from kfp.components import create_component_from_func

# Component: Load and process CSV data
def load_csv(input_base: str, output_data: str):
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
def train_model(training_data: str, model: str):
    """Trains a simple model using the training data."""
    import os
    os.makedirs(model, exist_ok=True)
    with open(os.path.join(model, "model.txt"), "w") as f:
        f.write(f"Trained model using: {training_data}")

trainer_op = create_component_from_func(
    func=train_model,
    base_image="python:3.9",
)

# Component: Push the trained model to a deployment location
def push_model(model: str, deployment: str):
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
        training_data=example_gen.outputs["output_data"],
        model=f"{pipeline_root}/trainer_output"
    )

    # Step 3: Deploy the trained model
    pusher = pusher_op(
        model=trainer.outputs["model"],
        deployment=f"{pipeline_root}/pusher_output"
    )