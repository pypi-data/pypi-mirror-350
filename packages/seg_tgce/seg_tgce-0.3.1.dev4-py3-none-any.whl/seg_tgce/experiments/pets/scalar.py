import argparse

import keras_tuner as kt
from keras.callbacks import EarlyStopping
from seg_tgce.data.oxford_pet.oxford_pet import (
    fetch_models,
    get_data_multiple_annotators,
)
from seg_tgce.experiments.plot_utils import plot_training_history, print_test_metrics
from seg_tgce.models.builders import build_scalar_model_from_hparams
from seg_tgce.models.ma_model import ScalarVisualizationCallback

TARGET_SHAPE = (64, 64)
BATCH_SIZE = 64
NUM_CLASSES = 3
NOISE_LEVELS = [-20.0, 0.0, 10.0]
NUM_SCORERS = len(NOISE_LEVELS)
TRAIN_EPOCHS = 50
TUNER_EPOCHS = 10
SEED = 42
LABELING_RATE = 0.7

# Default hyperparameters for direct training
DEFAULT_HPARAMS = {
    "learning_rate": 1e-4,
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
            "learning_rate": hp.Float(
                "learning_rate", min_value=1e-5, max_value=1e-2, sampling="LOG"
            ),
            "q": hp.Float("q", min_value=0.1, max_value=0.9, step=0.1),
            "noise_tolerance": hp.Float(
                "noise_tolerance", min_value=0.1, max_value=0.9, step=0.1
            ),
            "b": hp.Float("b", min_value=0.1, max_value=1.0, step=0.1),
            "a": hp.Float("a", min_value=0.1, max_value=1.0, step=0.1),
        }

    return build_scalar_model_from_hparams(
        learning_rate=params["learning_rate"],
        q=params["q"],
        noise_tolerance=params["noise_tolerance"],
        b=params["b"],
        a=params["a"],
        num_classes=NUM_CLASSES,
        target_shape=TARGET_SHAPE,
        n_scorers=NUM_SCORERS,
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
        project_name="pets_scalar_tuning",
    )

    print("Starting hyperparameter search...")
    tuner.search(
        train_gen.take(16).cache(),
        epochs=TUNER_EPOCHS,
        validation_data=val_gen.take(8).cache(),
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
        description="Train pets scalar model with or without hyperparameter tuning"
    )
    parser.add_argument(
        "--use-tuner",
        action="store_true",
        help="Use Keras Tuner for hyperparameter optimization",
    )
    args = parser.parse_args()

    disturbance_models = fetch_models(NOISE_LEVELS, seed=SEED)
    train, val, test = get_data_multiple_annotators(
        annotation_models=disturbance_models,
        target_shape=TARGET_SHAPE,
        batch_size=BATCH_SIZE,
        labeling_rate=LABELING_RATE,
    )

    if args.use_tuner:
        print("Using Keras Tuner for hyperparameter optimization...")
        model = train_with_tuner(train, val)
    else:
        print("Training with default hyperparameters...")
        model = train_directly()

    vis_callback = ScalarVisualizationCallback(val)

    print("\nTraining final model...")
    history = model.fit(
        train.take(16).cache(),
        epochs=TRAIN_EPOCHS,
        validation_data=val.take(8).cache(),
        callbacks=[
            vis_callback,
            EarlyStopping(
                monitor="val_segmentation_output_dice_coefficient",
                patience=5,
                mode="max",
                restore_best_weights=True,
            ),
        ],
    )

    plot_training_history(history, "Pets Scalar Model Training History")
    print_test_metrics(model, test, "Pets Scalar")
