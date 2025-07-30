import argparse

import keras_tuner as kt
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from seg_tgce.data.crowd_seg.tfds_builder import (
    create_one_hot_mask,
    get_crowd_seg_dataset_tfds,
)
from seg_tgce.experiments.plot_utils import plot_training_history, print_test_metrics
from seg_tgce.models.builders import (
    build_baseline_model_from_hparams,
)
from seg_tgce.models.ma_model import BaselineVisualizationCallback

TARGET_SHAPE = (128, 128)
BATCH_SIZE = 64
NUM_CLASSES = 6
TRAIN_EPOCHS = 20
TUNER_EPOCHS = 2
MAX_TRIALS = 5
# Default hyperparameters for direct training
DEFAULT_HPARAMS = {
    "q": 0.6,
    "noise_tolerance": 0.2,
    "dropout_rate": 0.2,
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
            "q": hp.Float("q", min_value=0.1, max_value=0.9, step=0.1),
            "noise_tolerance": hp.Float(
                "noise_tolerance", min_value=0.1, max_value=0.9, step=0.1
            ),
            "dropout_rate": hp.Float(
                "dropout_rate", min_value=0.0, max_value=0.5, step=0.1
            ),
        }

    return build_baseline_model_from_hparams(
        learning_rate=1e-3,
        q=params["q"],
        noise_tolerance=params["noise_tolerance"],
        num_classes=NUM_CLASSES,
        target_shape=TARGET_SHAPE,
        dropout_rate=params["dropout_rate"],
    )


def train_with_tuner(train_gen, val_gen):
    """Train model using Keras Tuner for hyperparameter optimization."""
    tuner = kt.BayesianOptimization(
        build_model,
        objective=kt.Objective("val_dice_coefficient", direction="max"),
        max_trials=MAX_TRIALS,
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

    def map_dataset_to_baseline(x):
        expert_mask = x["masks"][-1]
        # Ensure the expert mask has the correct shape before one-hot encoding
        expert_mask = tf.reshape(expert_mask, TARGET_SHAPE)
        return (x["image"], create_one_hot_mask(expert_mask))

    train, validation, test = get_crowd_seg_dataset_tfds(image_size=TARGET_SHAPE)
    processed_train = train.map(map_dataset_to_baseline).cache().batch(BATCH_SIZE)
    processed_validation = (
        validation.map(map_dataset_to_baseline).cache().batch(BATCH_SIZE)
    )
    processed_test = test.map(map_dataset_to_baseline).cache().batch(BATCH_SIZE)

    # Visualize first batch samples
    print("\nVisualizing first batch samples...")
    first_batch = next(iter(processed_train))
    images, masks = first_batch

    # Plot first 4 samples
    num_samples = 6
    fig, axes = plt.subplots(num_samples, 2, figsize=(10, 20))
    for i in range(num_samples):
        # Plot image
        axes[i, 0].imshow(images[i])
        axes[i, 0].set_title(f"Image {i+1}")
        axes[i, 0].axis("off")

        # Convert one-hot mask to class indices for visualization
        mask_class = np.argmax(masks[i], axis=-1)
        axes[i, 1].imshow(mask_class, cmap="viridis")
        axes[i, 1].set_title(f"Ground Truth {i+1}")
        axes[i, 1].axis("off")

    plt.tight_layout()
    plt.show()

    if args.use_tuner:
        print("Using Keras Tuner for hyperparameter optimization...")
        model = train_with_tuner(processed_train, processed_validation)
    else:
        print("Training with default hyperparameters...")
        model = train_directly()

    vis_callback = BaselineVisualizationCallback(processed_validation)

    # Add learning rate scheduler
    lr_scheduler = ReduceLROnPlateau(
        monitor="val_dice_coefficient",
        factor=0.2,
        patience=2,
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
                monitor="val_dice_coefficient",
                patience=3,
                mode="max",
                restore_best_weights=True,
            ),
        ],
    )

    plot_training_history(
        history,
        "Histology Baseline Model Training History",
        ["dice_coefficient", "jaccard_coefficient"],
    )
    print_test_metrics(
        model,
        processed_test,
        "Histology Baseline Model",
    )
