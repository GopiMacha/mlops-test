from kfp import dsl
from kfp.components import load_component_from_text

# Component: Load and process CSV data
csv_example_gen_op = load_component_from_text("""
name: CsvExampleGen
description: Load and process CSV data.
inputs:
- {name: input_base, type: String, description: "Path to input CSV files"}
outputs:
- {name: output_data, type: String, description: "Processed data output"}
implementation:
  container:
    image: python:3.9
    command:
    - python
    - -c
    - |
      import os
      import shutil
      import sys
      input_base = sys.argv[1]
      output_data = sys.argv[2]
      os.makedirs(output_data, exist_ok=True)
      shutil.copytree(input_base, output_data)
    args:
    - {inputValue: input_base}
    - {outputPath: output_data}
""")


# Component: Train a machine learning model
trainer_op = load_component_from_text("""
name: Trainer
description: Train a machine learning model.
inputs:
- {name: training_data, type: String, description: "Path to training data"}
outputs:
- {name: model, type: String, description: "Path to trained model"}
implementation:
  container:
    image: python:3.9
    command:
    - python
    - -c
    - |
      import os
      import sys
      training_data = sys.argv[1]
      model = sys.argv[2]
      os.makedirs(model, exist_ok=True)
      with open(os.path.join(model, "model.txt"), "w") as f:
          f.write("Trained model using: " + training_data)
    args:
    - {inputValue: training_data}
    - {outputPath: model}
""")


# Component: Push the trained model to a deployment location
pusher_op = load_component_from_text("""
name: Pusher
description: Push the trained model to a destination.
inputs:
- {name: model, type: String, description: "Path to trained model"}
outputs:
- {name: deployment, type: String, description: "Path to deployment directory"}
implementation:
  container:
    image: python:3.9
    command:
    - python
    - -c
    - |
      import os
      import shutil
      import sys
      model = sys.argv[1]
      deployment = sys.argv[2]
      os.makedirs(deployment, exist_ok=True)
      shutil.copytree(model, deployment)
    args:
    - {inputValue: model}
    - {outputPath: deployment}
""")


@dsl.pipeline(
    name="Example Pipeline",
    description="A KFP pipeline for loading CSV data, training a model, and deploying it."
)
def create_pipeline(pipeline_root: str, data_path: str):  # Type annotations added
    # Step 1: Load CSV data
    example_gen = csv_example_gen_op(input_base=data_path)
    
    # Step 2: Train the model
    trainer = trainer_op(training_data=example_gen.outputs["output_data"])
    
    # Step 3: Deploy the trained model
    pusher = pusher_op(model=trainer.outputs["model"])
