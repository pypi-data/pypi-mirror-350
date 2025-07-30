import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from keras.losses import Loss
from tensorflow import float32 as tf_float32

TARGET_DATA_TYPE = tf_float32


class TgceScalarDebug(Loss):
    """
    Debuggable version of Truncated generalized cross entropy
    for semantic segmentation loss.
    """

    def __init__(
        self,
        *,
        num_classes: int,
        name: str = "TGCE_SS_DEBUG",
        q: float = 0.1,
        noise_tolerance: float = 0.1,
        lambda_reg_weight: float = 0.1,
        lambda_entropy_weight: float = 0.1,
        lambda_sum_weight: float = 0.1,
        epsilon: float = 1e-8,
    ) -> None:
        self.q = q
        self.num_classes = num_classes
        self.noise_tolerance = noise_tolerance
        self.lambda_reg_weight = lambda_reg_weight
        self.lambda_entropy_weight = lambda_entropy_weight
        self.lambda_sum_weight = lambda_sum_weight
        self.epsilon = epsilon
        super().__init__(name=name)

    def visualize_tensors(self, tensors_dict):
        """Helper function to visualize multiple tensors in subplots"""
        n_tensors = len(tensors_dict)
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.flatten()

        for idx, (title, tensor) in enumerate(tensors_dict.items()):
            im = axes[idx].imshow(tensor[0, :, :, 0].numpy(), cmap="viridis")
            axes[idx].set_title(title)
            plt.colorbar(im, ax=axes[idx])

        # Hide any unused subplots
        for idx in range(n_tensors, len(axes)):
            axes[idx].set_visible(False)

        plt.tight_layout()
        plt.show()

    def call(
        self,
        y_true: tf.Tensor,
        y_pred: tf.Tensor,
        lambda_r: tf.Tensor,
        labeler_mask: tf.Tensor,
    ) -> tf.Tensor:
        print("\n=== Starting TGCE Loss Computation ===")
        print(f"Input shapes:")
        print(f"y_true: {y_true.shape}")
        print(f"y_pred: {y_pred.shape}")
        print(f"lambda_r: {lambda_r.shape}")
        print(f"labeler_mask: {labeler_mask.shape}")

        # Clip predictions and reliability
        y_pred = tf.clip_by_value(y_pred, self.epsilon, 1.0 - self.epsilon)
        lambda_r = tf.clip_by_value(lambda_r, self.epsilon, 1.0 - self.epsilon)

        print("\nAfter clipping:")
        print(f"y_pred range: [{tf.reduce_min(y_pred)}, {tf.reduce_max(y_pred)}]")
        print(f"lambda_r range: [{tf.reduce_min(lambda_r)}, {tf.reduce_max(lambda_r)}]")

        # Expand predictions
        y_pred_exp = tf.expand_dims(y_pred, axis=-1)
        y_pred_exp = tf.tile(y_pred_exp, [1, 1, 1, 1, tf.shape(y_true)[-1]])
        print(f"\nExpanded y_pred shape: {y_pred_exp.shape}")

        # Expand and tile lambda_r
        lambda_r = tf.expand_dims(tf.expand_dims(lambda_r, 1), 1)
        lambda_r = tf.tile(lambda_r, [1, tf.shape(y_pred)[1], tf.shape(y_pred)[2], 1])
        print(f"Expanded lambda_r shape: {lambda_r.shape}")

        # Apply labeler mask
        lambda_r = lambda_r * tf.expand_dims(tf.expand_dims(labeler_mask, 1), 1)
        print("\nAfter applying labeler mask:")
        print(f"lambda_r range: [{tf.reduce_min(lambda_r)}, {tf.reduce_max(lambda_r)}]")

        # Compute correct probabilities
        correct_probs = tf.reduce_sum(y_true * y_pred_exp, axis=-2)
        correct_probs = tf.clip_by_value(
            correct_probs, self.epsilon, 1.0 - self.epsilon
        )
        print(f"\nCorrect probabilities shape: {correct_probs.shape}")
        print(
            f"Correct probabilities range: [{tf.reduce_min(correct_probs)}, {tf.reduce_max(correct_probs)}]"
        )

        # Compute loss terms
        term1 = (
            lambda_r * (1.0 - tf.pow(correct_probs, self.q)) / (self.q + self.epsilon)
        )
        term2 = (1.0 - lambda_r) * (
            (1.0 - tf.pow(self.noise_tolerance, self.q)) / (self.q + self.epsilon)
        )

        print("\nLoss terms:")
        print(f"term1 range: [{tf.reduce_min(term1)}, {tf.reduce_max(term1)}]")
        print(f"term2 range: [{tf.reduce_min(term2)}, {tf.reduce_max(term2)}]")

        # Compute regularization terms
        valid_lambda_r = lambda_r * tf.expand_dims(tf.expand_dims(labeler_mask, 1), 1)
        lambda_reg = self.lambda_reg_weight * tf.reduce_mean(
            tf.square(valid_lambda_r - 0.5)
        )
        lambda_entropy = -self.lambda_entropy_weight * tf.reduce_mean(
            valid_lambda_r * tf.math.log1p(valid_lambda_r)
            + (1 - valid_lambda_r) * tf.math.log1p(1 - valid_lambda_r)
        )
        lambda_sum = self.lambda_sum_weight * tf.reduce_mean(
            tf.square(tf.reduce_sum(valid_lambda_r, axis=-1) - 1.0)
        )

        print("\nRegularization terms:")
        print(f"lambda_reg: {lambda_reg}")
        print(f"lambda_entropy: {lambda_entropy}")
        print(f"lambda_sum: {lambda_sum}")

        # Compute total loss
        total_loss = (
            tf.reduce_mean(term1 + term2) + lambda_reg + lambda_entropy + lambda_sum
        )
        total_loss = tf.where(
            tf.math.is_nan(total_loss),
            tf.constant(1e6, dtype=total_loss.dtype),
            total_loss,
        )

        print(f"\nTotal loss: {total_loss}")
        print("=== End of TGCE Loss Computation ===\n")

        # Visualize all tensors in a single figure with subplots
        tensors_to_plot = {
            "Predictions": y_pred,
            "Reliability Map": lambda_r,
            "Correct Probabilities": correct_probs,
            "Combined Loss Terms": term1 + term2,
        }
        self.visualize_tensors(tensors_to_plot)

        return total_loss

    def get_config(self):
        """Retrieves loss configuration."""
        base_config = super().get_config()
        return {
            **base_config,
            "q": self.q,
            "lambda_reg_weight": self.lambda_reg_weight,
            "lambda_entropy_weight": self.lambda_entropy_weight,
            "lambda_sum_weight": self.lambda_sum_weight,
            "epsilon": self.epsilon,
        }


if __name__ == "__main__":
    # Create sample tensors for testing
    batch_size = 1
    height = 8
    width = 8
    num_classes = 2
    num_labelers = 3

    # Create underlying ground truth (a simple pattern)
    ground_truth = np.zeros((height, width, num_classes))
    # Create a checkerboard pattern for class 0
    ground_truth[::2, ::2, 0] = 1
    ground_truth[1::2, 1::2, 0] = 1
    # Class 1 is the complement
    ground_truth[:, :, 1] = 1 - ground_truth[:, :, 0]
    ground_truth = tf.convert_to_tensor(ground_truth, dtype=tf.float32)
    ground_truth = tf.expand_dims(ground_truth, 0)  # Add batch dimension

    # Create labeler-specific distortions
    y_true = []
    for i in range(num_labelers):
        # Different noise levels for each labeler
        noise_level = 0.1 * (i + 1)  # Increasing noise for each labeler
        # Add noise to ground truth
        noisy_gt = ground_truth + tf.random.normal(
            ground_truth.shape, mean=0.0, stddev=noise_level
        )
        # Apply softmax to get valid probabilities
        noisy_gt = tf.nn.softmax(noisy_gt, axis=-1)
        y_true.append(noisy_gt)

    # Stack labeler annotations
    y_true = tf.stack(y_true, axis=-1)

    # Create predictions (another distortion of ground truth)
    pred_noise = tf.random.normal(ground_truth.shape, mean=0.0, stddev=0.15)
    y_pred = ground_truth + pred_noise
    y_pred = tf.nn.softmax(y_pred, axis=-1)

    # Create reliability scores (higher for labelers with less noise)
    lambda_r = tf.constant(
        [[0.9, 0.7, 0.5]], dtype=tf.float32
    )  # Decreasing reliability

    # Create labeler mask (all labelers active)
    labeler_mask = tf.ones((batch_size, num_labelers))

    # Visualize the underlying ground truth
    plt.figure(figsize=(8, 4))
    plt.subplot(121)
    plt.imshow(ground_truth[0, :, :, 0].numpy(), cmap="viridis")
    plt.title("Ground Truth - Class 0")
    plt.colorbar()
    plt.subplot(122)
    plt.imshow(ground_truth[0, :, :, 1].numpy(), cmap="viridis")
    plt.title("Ground Truth - Class 1")
    plt.colorbar()
    plt.tight_layout()
    plt.show()

    # Visualize annotations from each labeler
    fig, axes = plt.subplots(num_labelers, 2, figsize=(10, 4 * num_labelers))
    for i in range(num_labelers):
        # Class 0
        im0 = axes[i, 0].imshow(y_true[0, :, :, 0, i].numpy(), cmap="viridis")
        axes[i, 0].set_title(
            f"Labeler {i+1} - Class 0 (Reliability: {lambda_r[0, i]:.2f})"
        )
        plt.colorbar(im0, ax=axes[i, 0])

        # Class 1
        im1 = axes[i, 1].imshow(y_true[0, :, :, 1, i].numpy(), cmap="viridis")
        axes[i, 1].set_title(
            f"Labeler {i+1} - Class 1 (Reliability: {lambda_r[0, i]:.2f})"
        )
        plt.colorbar(im1, ax=axes[i, 1])

    plt.tight_layout()
    plt.show()

    # Initialize and call the loss
    loss_fn = TgceScalarDebug(num_classes=num_classes)
    loss = loss_fn.call(y_true, y_pred, lambda_r, labeler_mask)
