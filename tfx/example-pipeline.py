from kfp.v2 import dsl
from kfp.v2.dsl import component, Input, Output, Dataset, Model
from google_cloud_pipeline_components.v1.dataset import TextDatasetCreateOp
from google_cloud_pipeline_components.v1.automl import AutoMLTextTrainingJobRunOp
from google_cloud_pipeline_components.v1.endpoint import EndpointCreateOp, ModelDeployOp

@dsl.pipeline(
    name="simple-poc-pipeline",
    description="A simple pipeline for AutoML text classification."
)
def pipeline(
    project: str,
    region: str,
    import_file: str,
    display_name: str,
    pipeline_root: str,
):
    # Step 1: Create a Text Dataset
    dataset_task = TextDatasetCreateOp(
        display_name=display_name,
        gcs_source=import_file,
        import_schema_uri="gs://google-cloud-aiplatform/schema/dataset/schema-v0.0.1.yaml",
        project=project,
        location=region,
    )

    # Step 2: Train an AutoML Text Model
    training_task = AutoMLTextTrainingJobRunOp(
        display_name=display_name,
        dataset=dataset_task.outputs["dataset"],
        model_display_name=f"{display_name}-model",
        prediction_type="classification",
        multi_label=True,
        training_fraction_split=0.6,
        validation_fraction_split=0.2,
        test_fraction_split=0.2,
        project=project,
        location=region,
    )

    # Step 3: Create an Endpoint
    endpoint_task = EndpointCreateOp(
        project=project,
        location=region,
        display_name=f"{display_name}-endpoint",
    )

    # Step 4: Deploy the Model to the Endpoint
    ModelDeployOp(
        model=training_task.outputs["model"],
        endpoint=endpoint_task.outputs["endpoint"],
        deployed_model_display_name=f"{display_name}-deployed-model",
        automatic_resources_min_replica_count=1,
        automatic_resources_max_replica_count=1,
    )
