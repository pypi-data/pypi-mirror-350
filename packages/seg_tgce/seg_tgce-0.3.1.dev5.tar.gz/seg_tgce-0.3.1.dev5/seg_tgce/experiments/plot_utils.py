import matplotlib.pyplot as plt
import numpy as np


def plot_training_history(history, title, save_path=None):
    """Plot training and validation metrics from model history.

    Args:
        history: Model training history object
        title: Title for the plot
        save_path: Optional path to save the plot. If None, plot is shown instead.
    """
    metrics = [
        "loss",
        "segmentation_output_dice_coefficient",
        "segmentation_output_jaccard_coefficient",
    ]

    plt.figure(figsize=(15, 5))
    for i, metric in enumerate(metrics, 1):
        plt.subplot(1, 3, i)
        plt.plot(history.history[metric], label=f"Training {metric}")
        plt.plot(history.history[f"val_{metric}"], label=f"Validation {metric}")
        plt.title(f'{metric.replace("_", " ").title()}')
        plt.xlabel("Epoch")
        plt.ylabel(metric)
        plt.legend()

    plt.suptitle(title)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()


def print_test_metrics(model, test_data, model_name):
    """Print test metrics for a model including mean and standard deviation.

    Args:
        model: Trained model
        test_data: Test dataset
        model_name: Name of the model for printing
    """
    print(f"\nEvaluating {model_name} model:")

    # Get predictions for all test data
    predictions = []
    true_values = []

    for x, y in test_data:
        pred = model.predict(x, verbose=0)
        predictions.append(pred)
        true_values.append(y)

    # Convert to numpy arrays
    predictions = np.concatenate(predictions, axis=0)
    true_values = np.concatenate(true_values, axis=0)

    # Calculate metrics for each sample
    metric_values = {}
    for metric in model.metrics:
        metric_values[metric.name] = []
        for i in range(len(predictions)):
            value = metric(true_values[i : i + 1], predictions[i : i + 1])
            metric_values[metric.name].append(float(value))

    # Print results with mean and std
    print("\nTest Results:")
    for metric_name, values in metric_values.items():
        mean_value = np.mean(values)
        std_value = np.std(values)
        print(f"{metric_name}:")
        print(f"  Mean: {mean_value:.4f}")
        print(f"  Std:  {std_value:.4f}")
