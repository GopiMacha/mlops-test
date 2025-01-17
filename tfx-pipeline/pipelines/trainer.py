import tensorflow as tf
from tfx.utils.dsl_utils import external_input

def run_fn(fn_args):
    # Load data
    train_dataset = tf.data.TFRecordDataset(fn_args.train_files)
    eval_dataset = tf.data.TFRecordDataset(fn_args.eval_files)
    
    # Define a simple model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation="relu"),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer="adam", loss="mse", metrics=["mae"])
    
    # Train the model
    model.fit(train_dataset, epochs=10, validation_data=eval_dataset)
    
    # Save the model
    model.save(fn_args.serving_model_dir)
