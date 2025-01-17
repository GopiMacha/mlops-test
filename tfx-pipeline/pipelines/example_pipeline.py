from tfx.components import CsvExampleGen, Trainer, Pusher
from tfx.orchestration.pipeline import Pipeline

def create_pipeline(pipeline_root: str, data_path: str) -> Pipeline:
    # Step 1: Ingest CSV data
    example_gen = CsvExampleGen(input_base=data_path)  # Path to the data folder
    
    # Step 2: Trainer Component
    trainer = Trainer(
        module_file="trainer.py",  # Path to your custom training code
        examples=example_gen.outputs["examples"],  # Pass the examples from CsvExampleGen
    )
    
    # Step 3: Pusher Component
    pusher = Pusher(
        model=trainer.outputs["model"],  # Model from Trainer
        model_blessing=None  # Optional: Add validation/blessing logic if needed
    )
    
    # Return the pipeline
    return Pipeline(
        pipeline_name="example_pipeline",
        pipeline_root=pipeline_root,
        components=[example_gen, trainer, pusher],
    )


