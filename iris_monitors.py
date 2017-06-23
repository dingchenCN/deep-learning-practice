from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import numpy as np
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.INFO)
# https://www.tensorflow.org/get_started/monitors
# https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/tutorials/monitors/iris_monitors.py
# Data sets
IRIS_TRAINING = os.path.join(os.path.dirname(__file__), "iris_training.csv")
IRIS_TEST = os.path.join(os.path.dirname(__file__), "iris_test.csv")

def main(unused_argv):
    # Load datasets.
    training_set = tf.contrib.learn.datasets.base.load_csv_with_header(
        filename=IRIS_TRAINING, target_dtype=np.int, features_dtype=np.float32)
    test_set = tf.contrib.learn.datasets.base.load_csv_with_header(
        filename=IRIS_TEST, target_dtype=np.int, features_dtype=np.float32)

    # Specify that all features have real-value data
    feature_columns = [tf.contrib.layers.real_valued_column("", dimension=4)]

    # Customizing the Evaluation Metrics with MetricSpec
    validation_metrics = {
      "accuracy":
          tf.contrib.learn.MetricSpec(
              metric_fn=tf.contrib.metrics.streaming_accuracy,
              prediction_key="classes"),
      "precision":
          tf.contrib.learn.MetricSpec(
              metric_fn=tf.contrib.metrics.streaming_precision,
              prediction_key="classes"),
      "recall":
          tf.contrib.learn.MetricSpec(
              metric_fn=tf.contrib.metrics.streaming_recall,
              prediction_key="classes")
    }

    # simultaneously evaluate against test data to see how well the model is generalizing
    validation_monitor = tf.contrib.learn.monitors.ValidationMonitor(
        test_set.data,
        test_set.target,
        every_n_steps=50,
        # customized matrix above
        metrics=validation_metrics,
        # early stop condition: 200 steps, loss no decreasing
        early_stopping_metric="loss",
        early_stopping_metric_minimize=True,
        early_stopping_rounds=200)

    # Build 3 layer DNN with 10, 20, 10 units respectively.
    classifier = tf.contrib.learn.DNNClassifier(
        feature_columns=feature_columns,
        hidden_units=[10, 20, 10],
        n_classes=3,
        model_dir="/tmp/iris_model",
        # how many seconds should elapse between checkpoint saves during training
        config=tf.contrib.learn.RunConfig(save_checkpoints_secs=1))

    # Fit model.
    classifier.fit(x=training_set.data,
                   y=training_set.target,
                   steps=2000,
                   # takes a list of all monitors to run during model training
                   monitors=[validation_monitor])

    # Evaluate accuracy.
    accuracy_score = classifier.evaluate(x=test_set.data,
                                         y=test_set.target)["accuracy"]
    print('Accuracy: {0:f}'.format(accuracy_score))

    # Classify two new flower samples.
    new_samples = np.array(
        [[6.4, 3.2, 4.5, 1.5], [5.8, 3.1, 5.0, 1.7]], dtype=float)
    y = list(classifier.predict(new_samples, as_iterable=True))
    print('Predictions: {}'.format(str(y)))

if __name__ == "__main__":
  tf.app.run()
