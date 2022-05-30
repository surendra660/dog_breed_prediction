# This is the terminal version.
import sys
from predictions import custom_path, top3_labels, confidence


def terminal_printer(argv):
    print("-" * 54)
    print("Path: " + argv)
    print("Top 3 predicted breeds and confidence levels in %")
    print("-" * 54)
    print("")
    print("Prediction 1")
    print("-" * 54)
    print("{}  |  {:.2f}%".format(top3_labels[0][0].replace("_", " ").title(), confidence[0][0]))
    print("-" * 54)
    print("")
    print("Prediction 2")
    print("-" * 54)
    print("{}  |  {:.2f}%".format(top3_labels[0][1].replace("_", " ").title(), confidence[0][1]))
    print("-" * 54)
    print("")
    print("Prediction 3")
    print("-" * 54)
    print("{}  |  {:.2f}%".format(top3_labels[0][2].replace("_", " ").title(), confidence[0][2]))
    print("-" * 54)
    print("")
    return


if __name__ == "__main__":
    try:
        # We give filepath at the 1 index (python dog_breed_prediction_term.py [image_file_path])
        custom_path([(sys.argv[1])])
        terminal_printer(sys.argv[1])

    except IndexError:
        print("")
        print("Please enter a valid image filepath like: python dog_breed_prediction_term.py image_file_path.jpg")
        print("")
