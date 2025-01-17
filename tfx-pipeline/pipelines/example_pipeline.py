from tfx.components import CsvExampleGen, Trainer, Pusher
from tfx.orchestration.pipeline import Pipeline
from tfx.proto import pusher_pb2  # Required for defining push destinations

def create_pipeline(pipeline_root: str, data_path: str, model_push_path: str) -> Pipeline:
    # Step 1: Ingest CSV data
    example_gen = CsvExampleGen(input_base=data_path)
    
    # Step 2: Trainer Component
    trainer = Trainer(
        module_file="trainer.py",  # Path to your custom training code
        examples=example_gen.outputs["examples"],  # Pass the examples from CsvExampleGen
    )
    
    # Step 3: Pusher Component
    pusher = Pusher(
        model=trainer.outputs["model"],  # Model from Trainer
        push_destination=pusher_pb2.PushDestination(
            filesystem=pusher_pb2.PushDestination.Filesystem(base_directory=model_push_path)
        ),
    )
    
    # Return the pipeline
    return Pipeline(
        pipeline_name="example_pipeline",
        pipeline_root=pipeline_root,
        components=[example_gen, trainer, pusher],
    )


