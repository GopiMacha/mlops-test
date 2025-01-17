import os
import sys

# Add the tfx-pipeline directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from tfx.orchestration.experimental.kubeflow.v2.kubeflow_v2_dag_runner import KubeflowV2DagRunner
from tfx.orchestration.experimental.kubeflow.v2.kubeflow_v2_dag_runner import KubeflowV2DagRunnerConfig
from pipelines.example_pipeline import create_pipeline

def compile_pipeline():
    # Define pipeline parameters
    pipeline_root = "gs://sinuous-myth-447220-m2_cloudbuild"
    data_path = "data/sample_data.csv"  # Path to the input data
    
    # Create the pipeline using the TFX pipeline creation function
    pipeline = create_pipeline(
        pipeline_root=pipeline_root,
        data_path=data_path
    )
    
    # Set up the Kubeflow V2 Dag Runner configuration
    runner_config = KubeflowV2DagRunnerConfig(
        default_image="tensorflow/tfx:latest"  # Replace with your TFX image if needed
    )
    
    # Compile the TFX pipeline into a Kubeflow Pipeline JSON file
    KubeflowV2DagRunner(
        config=runner_config,
        output_filename="example_pipeline.json"
    ).run(pipeline)

def run_pipeline():
    # Example of running the pipeline interactively
    pipeline_root = "gs://sinuous-myth-447220-m2_cloudbuild"
    data_path = "data/sample_data.csv"
    
    pipeline = create_pipeline(
        pipeline_root=pipeline_root,
        data_path=data_path
    )
    
    from tfx.orchestration.experimental.interactive.interactive_runner import InteractiveRunner
    InteractiveRunner().run(pipeline)

if __name__ == "__main__":
    mode = sys.argv[2]  # Get mode from command-line arguments
    if mode == "compile-pipeline":
        compile_pipeline()
    elif mode == "run-pipeline":
        run_pipeline()
