from tfx.components import CsvExampleGen, Trainer, Pusher
from tfx.dsl.pipeline import Pipeline

def create_pipeline(pipeline_root: str, data_path: str) -> Pipeline:
    example_gen = CsvExampleGen(input_base=data_path)
    trainer = Trainer(module_file="trainer.py")
    pusher = Pusher(model_push_destination={})
    return Pipeline(
        pipeline_name="example_pipeline",
        pipeline_root=pipeline_root,
        components=[example_gen, trainer, pusher],
    )

