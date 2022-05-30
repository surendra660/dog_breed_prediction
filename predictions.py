import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub

# Define image size
IMG_SIZE = 224

# Define BATCH_SIZE (32 is a good start)
BATCH_SIZE = 32

labels_csv = pd.read_csv("data/labels.csv")
labels = labels_csv.breed.to_numpy()

# Find the unique label values
unique_breeds = np.unique(labels)

# Lists of Top 3 labels and their confidence levels
top3_labels = []
confidence = []


# Create a function for preprocessing images
def process_image(image_path):
    """
    Takes an image file path and turns the image into a Tensor.
    """

    # Read in an image file
    image = tf.io.read_file(image_path)

    # Turn the jpg image into numerical Tensor with 3 colour channels (Red, Green, Blue)
    image = tf.image.decode_jpeg(image, channels=3)

    # Convert the colour channel values from 0-255 to 0-1 values.
    image = tf.image.convert_image_dtype(image, tf.float32)

    # Resize the image to our desired value (224, 224)
    image = tf.image.resize(image, size=[IMG_SIZE, IMG_SIZE])

    return image


# Create a simple function to return a tuple (image, label)
def get_image_label(image_path, label):
    """
    Takes an image file pathname and the assosiated label, processes the image and returns a tuple of (image, label)
    """
    image = process_image(image_path)
    return image, label


# Create a function to turn data into batches.
def create_data_batches(x):
    """
    Accepts test data as input (no labels).
    """
    data = tf.data.Dataset.from_tensor_slices((tf.constant(x)))  # only filepaths (no labels)
    data_batch = data.map(process_image).batch(BATCH_SIZE)
    return data_batch


# Turn prediction probabilities into their respective label (easier to understand)
def get_pred_label(prediction_probabilities):
    """
    Turns an array of prediction probabilities into a label.
    """
    return unique_breeds[np.argmax(prediction_probabilities)]


# Create a function to load a trained model
def load_model(model_path):
    """
    Loads a save model from a specified path.
    """
    print(f"Loading saved model from: {model_path}")
    model = tf.keras.models.load_model(model_path,
                                       custom_objects={"KerasLayer": hub.KerasLayer})
    return model


def pred_prob_labels(prediction_probabilities, labels):
    """
    Top 3 highest prediction confidences along with the truth label for sample n.
    """
    pred_prob, true_label = prediction_probabilities[0], labels[0]

    # Find the top 3 prediction confidence indexes
    top_3_pred_indexes = pred_prob.argsort()[-3:][::-1]

    # Find the top 3 prediction labels
    top_3_pred_labels = unique_breeds[top_3_pred_indexes]

    # Find the top 3 prediction confidence values
    top_3_pred_values = pred_prob[top_3_pred_indexes]

    # Convert confidence values to percentage
    confidence_in_percentage = [np.max(i) * 100 for i in top_3_pred_values]

    # Clear the lists
    top3_labels.clear(), confidence.clear()

    return top3_labels.append(top_3_pred_labels), confidence.append(confidence_in_percentage)


# Loading the full model
loaded_full_model = load_model("model/20200911-15481599839307-full-image-set-mobilenetv2-Adam.h5")


def custom_path(custom_image_path):
    # Turn custom images into batch datasets
    custom_data = create_data_batches(custom_image_path)

    # Make predictions on the custom data
    custom_preds = loaded_full_model.predict(custom_data)

    # Get custom prediction labels
    custom_pred_labels = [get_pred_label(custom_preds[i]) for i in range(len(custom_preds))]

    return pred_prob_labels(prediction_probabilities=custom_preds,
                            labels=custom_pred_labels)
