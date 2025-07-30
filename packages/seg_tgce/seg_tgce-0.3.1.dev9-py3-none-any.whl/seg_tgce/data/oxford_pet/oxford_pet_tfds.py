from typing import Dict, List, Tuple

import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from keras.models import Model

from seg_tgce.data.oxford_pet.disturbance.model import (
    ResizeToInput,
    download_base_model,
    find_last_encoder_conv_layer,
    produce_disturbed_models,
)
from seg_tgce.data.oxford_pet.oxford_pet import visualize_data
from seg_tgce.data.utils import LabelerAssignmentManager

from .oxford_iiit_pet import OxfordIiitPet

MODEL_ORIGINAL_SHAPE = (512, 512)


class OxfordPetMultipleAnnotators(tfds.core.GeneratorBasedBuilder):
    """DatasetBuilder for Oxford Pet dataset with multiple annotators."""

    VERSION = tfds.core.Version("1.0.0")
    RELEASE_NOTES = {
        "1.0.0": "Initial release.",
    }

    def __init__(
        self,
        *,
        noise_levels_snr: List[float],
        target_shape: Tuple[int, int] = (256, 256),
        labeling_rate: float = 0.7,
        seed: int | None = None,
    ):
        """Initialize the dataset builder.

        Args:
            noise_levels_snr: List of SNR values for each annotator
            target_shape: Target shape for images and masks
            labeling_rate: Probability that each labeler will label a sample
            seed: Random seed for reproducibility
        """
        self.noise_levels_snr = noise_levels_snr
        self.target_shape = target_shape
        self.labeling_rate = labeling_rate
        self.seed = seed
        super().__init__()

    def _info(self) -> tfds.core.DatasetInfo:
        """Returns the dataset metadata."""
        return tfds.core.DatasetInfo(
            builder=self,
            description="Oxford Pet dataset with multiple noisy annotators.",
            features=tfds.features.FeaturesDict(
                {
                    "image": tfds.features.Tensor(
                        shape=(*self.target_shape, 3), dtype=tf.float32
                    ),
                    "masks": tfds.features.Tensor(
                        shape=(*self.target_shape, 3, len(self.noise_levels_snr)),
                        dtype=tf.float32,
                    ),
                    "labeler_mask": tfds.features.Tensor(
                        shape=(len(self.noise_levels_snr),), dtype=tf.float32
                    ),
                    "ground_truth": tfds.features.Tensor(
                        shape=(*self.target_shape, 3), dtype=tf.float32
                    ),
                }
            ),
            supervised_keys=("image", "ground_truth"),
            homepage="https://www.robots.ox.ac.uk/~vgg/data/pets/",
            citation="""@InProceedings{parkhi12a,
              author       = "Parkhi, O. M. and Vedaldi, A. and Zisserman, A. and Jawahar, C.~V.",
              title        = "Cats and Dogs",
              booktitle    = "IEEE Conference on Computer Vision and Pattern Recognition",
              year         = "2012",
            }""",
        )

    def _split_generators(self, dl_manager: tfds.download.DownloadManager):
        """Returns SplitGenerators."""

        base_dataset = OxfordIiitPet()
        train, val, test = base_dataset()

        # Get dataset sizes
        train_size = sum(1 for _ in train)
        val_size = sum(1 for _ in val)
        test_size = sum(1 for _ in test)

        # Create labeler managers
        train_labeler_manager = LabelerAssignmentManager(
            num_samples=train_size,
            num_labelers=len(self.noise_levels_snr),
            labeling_rate=self.labeling_rate,
            seed=self.seed,
        )

        # Download and prepare the disturbance models
        model_path = download_base_model()
        model_ann = tf.keras.models.load_model(
            model_path,
            compile=False,
            safe_mode=False,
            custom_objects={"ResizeToInput": ResizeToInput},
        )
        last_conv_encoder_layer = find_last_encoder_conv_layer(model_ann)
        disturbance_models, measured_snr_values = produce_disturbed_models(
            self.noise_levels_snr,
            model_path,
            last_conv_encoder_layer,
            seed=self.seed,
        )

        return {
            "train": self._generate_examples(
                train, train_labeler_manager, disturbance_models
            ),
            "validation": self._generate_examples(val, None, disturbance_models),
            "test": self._generate_examples(test, None, disturbance_models),
        }

    def _generate_examples(
        self,
        dataset: tf.data.Dataset,
        labeler_manager: LabelerAssignmentManager | None,
        disturbance_models: List[Model],
    ):
        """Yields examples."""
        # Process images in batches for efficiency
        batch_size = 4  # Adjust based on your GPU memory
        current_batch = []
        current_indices = []
        current_masks = []

        for idx, (img, mask, _, _) in enumerate(dataset):
            # Resize image and mask
            img = tf.image.resize(img, self.target_shape)
            mask = tf.image.resize(mask, self.target_shape)

            # Add to current batch
            current_batch.append(tf.image.resize(img, MODEL_ORIGINAL_SHAPE))
            current_indices.append(idx)
            current_masks.append(mask)

            # Process batch when it's full or at the end
            if len(current_batch) == batch_size or idx == sum(1 for _ in dataset) - 1:
                # Stack images into a single batch
                batch_images = tf.stack(current_batch)

                # Process each model's predictions for the entire batch
                batch_predictions = []
                for model in disturbance_models:
                    # Get predictions for all images in batch
                    pred = model(batch_images)
                    # Resize predictions to target shape
                    pred = tf.image.resize(pred, self.target_shape)
                    batch_predictions.append(pred)

                # Stack predictions from all models
                # Shape: (batch_size, height, width, channels, num_models)
                batch_predictions = tf.stack(batch_predictions, axis=-1)

                # Process each example in the batch
                for i, (batch_idx, batch_mask) in enumerate(
                    zip(current_indices, current_masks)
                ):
                    # Get predictions for this example
                    noisy_masks = batch_predictions[i]

                    # Get labeler mask
                    if labeler_manager is not None:
                        labeler_mask = labeler_manager.get_labeler_mask(batch_idx)
                    else:
                        labeler_mask = tf.ones(len(disturbance_models))

                    # Apply labeler mask to noisy annotations
                    noisy_masks = tf.multiply(
                        noisy_masks, tf.reshape(labeler_mask, [1, 1, 1, -1])
                    )

                    # Convert tensors to numpy arrays and ensure correct shapes
                    yield batch_idx, {
                        "image": tf.image.resize(
                            current_batch[i], self.target_shape
                        ).numpy(),
                        "masks": noisy_masks.numpy(),
                        "labeler_mask": labeler_mask.numpy(),
                        "ground_truth": batch_mask.numpy(),
                    }

                # Clear batch
                current_batch = []
                current_indices = []
                current_masks = []


def get_data_multiple_annotators_tfds(
    noise_levels_snr: List[float],
    target_shape: Tuple[int, int] = (256, 256),
    batch_size: int = 32,
    labeling_rate: float = 0.7,
    seed: int | None = None,
) -> Tuple[tf.data.Dataset, tf.data.Dataset, tf.data.Dataset]:
    """Get datasets with multiple annotators and ground truth.

    Args:
        noise_levels_snr: List of SNR values for each annotator
        target_shape: Target shape for images and masks
        batch_size: Batch size for the datasets
        labeling_rate: Probability that each labeler will label a sample
        seed: Random seed for reproducibility

    Returns:
        Tuple of (train_dataset, val_dataset, test_dataset)
    """
    builder = OxfordPetMultipleAnnotators(
        noise_levels_snr=noise_levels_snr,
        target_shape=target_shape,
        labeling_rate=labeling_rate,
        seed=seed,
    )
    builder.download_and_prepare()

    return builder.as_dataset(
        split=("train", "validation", "test"),
        batch_size=batch_size,
        as_supervised=False,
    )


if __name__ == "__main__":
    noise_levels_snr = [-20.0, 0.0, 20.0]

    train_data, val_data, test_data = get_data_multiple_annotators_tfds(
        noise_levels_snr=noise_levels_snr,
        target_shape=(256, 256),
        batch_size=16,
        labeling_rate=0.7,
    )

    print("Visualizing training data samples...")
    visualize_data(
        train_data,
        num_samples=6,
        batch_index=0,
        noise_levels=noise_levels_snr,
        # save_path="oxford_pet_training_data.png",
    )
