import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from keras.preprocessing.image import img_to_array, load_img
from matplotlib import pyplot as plt

from seg_tgce.data.crowd_seg.__retrieve import (
    _BUCKET_NAME,
    MASKS_OBJECT_NAME,
    PATCHES_OBJECT_NAME,
)

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)


CLASSES_DEFINITION = {
    0: "Ignore",
    1: "Other",
    2: "Tumor",
    3: "Stroma",
    4: "Benign Inflammation",
    5: "Necrosis",
}

REAL_SCORERS = [
    "NP1",
    "NP2",
    "NP3",
    "NP4",
    "NP5",
    "NP6",
    "NP7",
    "NP8",
    "NP9",
    "NP10",
    "NP11",
    "NP12",
    "NP13",
    "NP14",
    "NP15",
    "NP16",
    "NP17",
    "NP18",
    "NP19",
    "NP20",
    "NP21",
]

AGGREGATED_SCORERS = ["MV", "STAPLE"]

ALL_SCORER_TAGS = REAL_SCORERS + AGGREGATED_SCORERS + ["expert"]

DEFAULT_IMG_SIZE = (512, 512)
METADATA_PATH = Path(__file__).resolve().parent / "metadata"

NUM_CLASSES = len(CLASSES_DEFINITION)
NUM_REAL_SCORERS = len(REAL_SCORERS)


def normalize_image(image: tf.Tensor) -> tf.Tensor:
    return tf.cast(image, tf.float32) / 255.0


def create_one_hot_mask(mask: tf.Tensor) -> tf.Tensor:
    mask = tf.cast(mask, tf.uint8)
    return tf.one_hot(mask, NUM_CLASSES, dtype=tf.float32)


def create_labeler_mask(labelers: tf.Tensor) -> tf.Tensor:
    labeler_mask = tf.zeros(NUM_REAL_SCORERS, dtype=tf.float32)

    for i, scorer in enumerate(REAL_SCORERS):
        labeler_mask = tf.tensor_scatter_nd_update(
            labeler_mask,
            [[i]],
            [tf.cast(tf.reduce_any(tf.equal(labelers, scorer)), tf.uint8)],
        )

    return labeler_mask


def process_sample(
    sample: Dict[str, tf.Tensor], image_size: Tuple[int, int]
) -> Dict[str, tf.Tensor]:
    image = normalize_image(sample["image"])

    real_scorer_indices = tf.where(
        tf.reduce_any(
            tf.equal(tf.expand_dims(sample["labelers"], 1), tf.constant(REAL_SCORERS)),
            axis=1,
        )
    )

    masks = tf.squeeze(
        tf.squeeze(tf.gather(sample["masks"], real_scorer_indices), axis=1), axis=-1
    )
    labelers = tf.gather(sample["labelers"], real_scorer_indices)

    masks = tf.map_fn(
        create_one_hot_mask,
        masks,
        fn_output_signature=tf.TensorSpec(
            shape=(*image_size, NUM_CLASSES), dtype=tf.float32
        ),
    )

    labeler_mask = create_labeler_mask(labelers)

    expanded_masks = tf.zeros(
        (NUM_REAL_SCORERS, *image_size, NUM_CLASSES), dtype=tf.float32
    )

    active_indices = tf.where(tf.equal(labeler_mask, 1))[:, 0]

    active_indices = tf.reshape(active_indices, [-1, 1])

    masks = tf.reshape(masks, [-1, *image_size, NUM_CLASSES])

    expanded_masks = tf.tensor_scatter_nd_update(expanded_masks, active_indices, masks)

    expanded_masks = tf.transpose(expanded_masks, perm=[1, 2, 3, 0])

    # Get the expert mask (last mask in the sequence)
    expert_mask = sample["masks"][-1]
    # Ensure the expert mask has the correct shape before one-hot encoding
    expert_mask = tf.reshape(expert_mask, image_size)

    return {
        "image": image,
        "masks": expanded_masks,
        "labelers_mask": labeler_mask,
        "ground_truth": create_one_hot_mask(expert_mask),
    }


class CrowdSegDataset(tfds.core.GeneratorBasedBuilder):
    """DatasetBuilder for crowd segmentation dataset."""

    VERSION = tfds.core.Version("1.0.0")
    RELEASE_NOTES = {
        "1.0.0": "Initial release.",
    }

    def __init__(
        self,
        *,
        image_size: Tuple[int, int] = DEFAULT_IMG_SIZE,
    ):
        """Initialize the dataset builder.

        Args:
            image_size: Tuple[int, int] = DEFAULT_IMG_SIZE: Image size for the dataset.
        """
        self.image_size = image_size
        super().__init__()

    def _info(self) -> tfds.core.DatasetInfo:
        return tfds.core.DatasetInfo(
            builder=self,
            description="Crowd segmentation dataset for histology images.",
            features=tfds.features.FeaturesDict(
                {
                    "image": tfds.features.Image(shape=(*self.image_size, 3)),
                    "masks": tfds.features.Sequence(
                        tfds.features.Tensor(
                            shape=(*self.image_size, 1), dtype=tf.uint8
                        )
                    ),
                    "labelers": tfds.features.Sequence(tfds.features.Text()),
                }
            ),
            supervised_keys=("image", "masks"),
            homepage="https://github.com/your-repo/crowd-seg",
            citation="""@article{your-citation}""",
        )

    def _split_generators(self, dl_manager: tfds.download.DownloadManager):
        patches_url = f"https://{_BUCKET_NAME}.s3.amazonaws.com/{PATCHES_OBJECT_NAME}"
        masks_url = f"https://{_BUCKET_NAME}.s3.amazonaws.com/{MASKS_OBJECT_NAME}"

        patches_path = dl_manager.download_and_extract(patches_url)
        masks_path = dl_manager.download_and_extract(masks_url)

        patches_dir = os.path.join(patches_path, "patches")
        masks_dir = os.path.join(masks_path, "masks")

        return {
            "train": self._generate_examples(
                os.path.join(patches_dir, "Train"),
                os.path.join(masks_dir, "Train"),
            ),
            "validation": self._generate_examples(
                os.path.join(patches_dir, "Val"),
                os.path.join(masks_dir, "Val"),
            ),
            "test": self._generate_examples(
                os.path.join(patches_dir, "Test"),
                os.path.join(masks_dir, "Test"),
            ),
        }

    def _generate_examples(self, image_dir: str, mask_dir: str):
        image_filenames = self._get_image_filenames(image_dir)

        for filename in image_filenames:
            image, masks, labelers = self._load_sample(filename, image_dir, mask_dir)
            yield filename, {
                "image": image,
                "masks": masks,
                "labelers": labelers,
            }

    def _get_image_filenames(self, image_dir: str) -> List[str]:
        return sorted(
            [
                filename
                for filename in os.listdir(image_dir)
                if filename.endswith(".png")
            ]
        )

    def _load_sample(
        self,
        filename: str,
        image_dir: str,
        mask_dir: str,
    ) -> Tuple[np.ndarray, List[np.ndarray], List[str]]:
        img_path = os.path.join(image_dir, filename)
        image = load_img(img_path, target_size=self.image_size)
        image = img_to_array(image, dtype=np.uint8)

        masks = []
        labelers = []

        for scorer_dir in ALL_SCORER_TAGS:
            scorer_mask_dir = os.path.join(mask_dir, scorer_dir)
            mask_path = os.path.join(scorer_mask_dir, filename)

            if os.path.exists(mask_path):
                mask_raw = load_img(
                    mask_path,
                    color_mode="grayscale",
                    target_size=self.image_size,
                )
                mask = img_to_array(mask_raw, dtype=np.uint8)

                if not np.all(np.isin(np.unique(mask), list(CLASSES_DEFINITION))):
                    LOGGER.warning(
                        "Mask %s contains invalid values. "
                        "Expected values: %s. "
                        "Values found: %s",
                        mask_path,
                        list(CLASSES_DEFINITION),
                        np.unique(mask),
                    )

                masks.append(mask)
                labelers.append(scorer_dir)

        return image, masks, labelers


def get_crowd_seg_dataset_tfds(
    image_size: Tuple[int, int] = DEFAULT_IMG_SIZE,
) -> Tuple[tf.data.Dataset, tf.data.Dataset, tf.data.Dataset]:
    """Get crowd segmentation dataset.

    Args:
        image_size: Tuple[int, int] = DEFAULT_IMG_SIZE: Image size for the dataset.

    Returns:
        Tuple[tf.data.Dataset, tf.data.Dataset, tf.data.Dataset]: TensorFlow datasets for train, validation, and test.
    """
    builder = CrowdSegDataset(
        image_size=image_size,
    )
    builder.download_and_prepare()

    return builder.as_dataset(split=("train", "validation", "test"))


def get_processed_data(
    image_size: Tuple[int, int] = DEFAULT_IMG_SIZE,
    batch_size: int = 32,
):
    train, validation, test = get_crowd_seg_dataset_tfds(
        image_size=image_size,
    )

    processed_train, processed_validation, processed_test = tuple(
        dataset.map(
            lambda x: process_sample(x, image_size),
            num_parallel_calls=tf.data.AUTOTUNE,
        )
        for dataset in (train, validation, test)
    )

    return (
        processed_train.batch(batch_size),
        processed_validation.batch(batch_size),
        processed_test.batch(batch_size),
    )


if __name__ == "__main__":
    target_size = (64, 64)
    batch_size = 32

    train, validation, test = get_crowd_seg_dataset_tfds(
        image_size=target_size,
    )

    # Add batching to the datasets

    processed_train, processed_validation, processed_test = tuple(
        dataset.map(
            lambda x: process_sample(x, target_size),
            num_parallel_calls=tf.data.AUTOTUNE,
        )
        for dataset in (train, validation, test)
    )
    processed_train = processed_train.batch(batch_size)
    processed_validation = processed_validation.batch(batch_size)
    processed_test = processed_test.batch(batch_size)

    # Get a single batch from each dataset
    for batch, processed_batch in zip(train.take(1), processed_train.take(1)):
        print("\nOriginal Batch Shapes:")
        print(
            "Image shape:", batch["image"].shape
        )  # Should be (batch_size, height, width, channels)
        print(
            "Masks shape:", batch["masks"].shape
        )  # Should be (batch_size, num_masks, height, width, 1)
        print(
            "Labelers shape:", tf.shape(batch["labelers"])
        )  # Should be (batch_size, num_masks)

        print("\nProcessed Batch Shapes:")
        print("Processed image shape:", processed_batch["image"].shape)
        print("Processed masks shape:", processed_batch["masks"].shape)
        print("Processed labelers mask shape:", processed_batch["labelers_mask"].shape)
        print("Processed ground truth shape:", processed_batch["ground_truth"].shape)

        # Visualize first image and its masks from the batch
        first_image = batch["image"][0]
        first_masks = batch["masks"][0]

        n_masks = first_masks.shape[0]
        n_cols = 3
        n_rows = (n_masks + n_cols) // n_cols

        plt.figure(figsize=(15, 5 * n_rows))

        plt.subplot(n_rows, n_cols, 1)
        plt.imshow(first_image)
        plt.title("Original Image")

        for i, mask in enumerate(first_masks):
            plt.subplot(n_rows, n_cols, i + 2)
            plt.imshow(mask, cmap="viridis")
            plt.title(f"Mask {i}")
            plt.colorbar()

        plt.tight_layout()
        plt.show()
