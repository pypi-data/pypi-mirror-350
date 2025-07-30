import argparse

import keras_tuner as kt
import tensorflow as tf
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from seg_tgce.data.crowd_seg.generator import (
    REAL_SCORERS,
)
from seg_tgce.data.crowd_seg.tfds_builder import (
    get_processed_data,
)
from seg_tgce.experiments.plot_utils import plot_training_history, print_test_metrics
from seg_tgce.models.builders import build_scalar_model_from_hparams
from seg_tgce.models.ma_model import ScalarVisualizationCallback

TARGET_SHAPE = (64, 64)
BATCH_SIZE = 128
NUM_CLASSES = 6  # From CLASSES_DEFINITION in generator.py
TRAIN_EPOCHS = 20
TUNER_EPOCHS = 1
N_SCORERS = len(REAL_SCORERS)

# Default hyperparameters for direct training
DEFAULT_HPARAMS = {
    "initial_learning_rate": 1e-3,
    "q": 0.5,
    "noise_tolerance": 0.5,
    "a": 0.3,
    "b": 0.7,
}


def build_model(hp=None):
    """Build model using hyperparameters.

    Args:
        hp: Optional Keras Tuner hyperparameters object. If None, uses default values.

    Returns:
        Compiled Keras model
    """
    if hp is None:
        # Use default hyperparameters
        params = DEFAULT_HPARAMS
    else:
        # Use tuner hyperparameters
        params = {
            "initial_learning_rate": DEFAULT_HPARAMS[
                "initial_learning_rate"
            ],  # Fixed initial learning rate
            "q": hp.Float("q", min_value=0.1, max_value=0.9, step=0.1),
            "noise_tolerance": hp.Float(
                "noise_tolerance", min_value=0.1, max_value=0.9, step=0.1
            ),
            "b": hp.Float("b", min_value=0.1, max_value=1.0, step=0.1),
            "a": hp.Float("a", min_value=0.1, max_value=1.0, step=0.1),
        }

    return build_scalar_model_from_hparams(
        learning_rate=params["initial_learning_rate"],
        q=params["q"],
        noise_tolerance=params["noise_tolerance"],
        b=params["b"],
        a=params["a"],
        num_classes=NUM_CLASSES,
        target_shape=TARGET_SHAPE,
        n_scorers=N_SCORERS,
    )


def train_with_tuner(train_gen, val_gen):
    """Train model using Keras Tuner for hyperparameter optimization."""
    tuner = kt.BayesianOptimization(
        build_model,
        objective=kt.Objective(
            "val_segmentation_output_dice_coefficient", direction="max"
        ),
        max_trials=10,
        directory="tuner_results",
        project_name="histology_scalar_tuning",
    )

    print("Starting hyperparameter search...")
    tuner.search(
        train_gen.take(10),
        epochs=TUNER_EPOCHS,
        validation_data=val_gen,
    )

    best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]
    print("\nBest hyperparameters:")
    for param, value in best_hps.values.items():
        print(f"{param}: {value}")

    return build_model(best_hps)


def train_directly():
    """Train model using default hyperparameters."""
    return build_model()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train histology scalar model with or without hyperparameter tuning"
    )
    parser.add_argument(
        "--use-tuner",
        action="store_true",
        help="Use Keras Tuner for hyperparameter optimization",
    )
    args = parser.parse_args()

    processed_train, processed_validation, processed_test = get_processed_data(
        image_size=TARGET_SHAPE,
        batch_size=BATCH_SIZE,
    )

    if args.use_tuner:
        print("Using Keras Tuner for hyperparameter optimization...")
        model = train_with_tuner(processed_train, processed_validation)
    else:
        print("Training with default hyperparameters...")
        model = train_directly()

    vis_callback = ScalarVisualizationCallback(
        processed_validation, save_dir="vis/histology/scalar"
    )

    # Add learning rate scheduler
    lr_scheduler = ReduceLROnPlateau(
        monitor="val_segmentation_output_dice_coefficient",
        factor=0.5,
        patience=3,
        min_lr=1e-6,
        mode="max",
        verbose=1,
    )

    print("\nTraining final model...")

    history = model.fit(
        processed_train,
        epochs=TRAIN_EPOCHS,
        validation_data=processed_validation,
        callbacks=[
            vis_callback,
            lr_scheduler,
            EarlyStopping(
                monitor="val_segmentation_output_dice_coefficient",
                patience=5,
                mode="max",
                restore_best_weights=True,
            ),
        ],
    )

    plot_training_history(history, "Histology Scalar Model Training History")
    print_test_metrics(model, processed_test, "Histology Scalar")
