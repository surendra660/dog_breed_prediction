# This is the GUI version created using PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from predictions import custom_path, top3_labels, confidence
from dog_breed_prediction_term import terminal_printer
from PIL import Image
import json
import time

# Make it False to disable printing predictions in terminal.
TERM_VIEW = True

# Folder with our resized images
resized_images = "data/resized_images/"


# Creating the base class
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(280, 374)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(10, 10, 950, 500))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.upload_image_main = QtWidgets.QLabel(self.frame)
        self.upload_image_main.setGeometry(QtCore.QRect(11, 10, 224, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(70)
        self.upload_image_main.setFont(font)
        self.upload_image_main.setAlignment(QtCore.Qt.AlignCenter)
        self.upload_image_main.setObjectName("upload_image_main")

        self.top3_predicted_main = QtWidgets.QLabel(self.frame)
        self.top3_predicted_main.setGeometry(QtCore.QRect(300, 10, 1500, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(70)
        self.top3_predicted_main.setFont(font)
        self.top3_predicted_main.setAlignment(QtCore.Qt.AlignLeft)
        self.top3_predicted_main.setObjectName("top3_predicted_main")
        

        self.pred_label_2 = QtWidgets.QTextBrowser(self.frame)
        self.pred_label_2.setGeometry(QtCore.QRect(540, 50, 400, 15))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(70)
        self.pred_label_2.setFont(font)
        self.pred_label_2.setAutoFillBackground(False)
        self.pred_label_2.setObjectName("pred_label_2")

        self.pred_label_3 = QtWidgets.QTextBrowser(self.frame)
        self.pred_label_3.setGeometry(QtCore.QRect(540, 65, 400, 270))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(70)
        self.pred_label_3.setFont(font)
        self.pred_label_3.setAutoFillBackground(False)
        self.pred_label_3.setObjectName("pred_label_3")
        



        self.uploaded_image = QtWidgets.QLabel(self.frame)
        self.uploaded_image.setGeometry(QtCore.QRect(11, 50, 224, 224))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(50)
        self.uploaded_image.setFont(font)
        self.uploaded_image.setText("Upload a jpg image")
        self.uploaded_image.setAlignment(QtCore.Qt.AlignCenter)
        self.uploaded_image.setObjectName("uploaded_image")

        self.filePath = QtWidgets.QTextBrowser(self.frame)
        self.filePath.setGeometry(QtCore.QRect(10, 280, 224, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.filePath.setFont(font)
        self.filePath.setObjectName("filePath")

        self.browseImageAndPredict_btn = QtWidgets.QPushButton(self.frame)
        self.browseImageAndPredict_btn.setGeometry(QtCore.QRect(11, 320, 224, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.browseImageAndPredict_btn.setFont(font)
        self.browseImageAndPredict_btn.setObjectName("browseImageAndPredict_btn")

        self.pred_image_1 = QtWidgets.QLabel(self.frame)
        self.pred_image_1.setGeometry(QtCore.QRect(300, 50, 224, 224))
        self.pred_image_1.setObjectName("pred_image_1")

        self.pred_label_1 = QtWidgets.QTextBrowser(self.frame)
        self.pred_label_1.setGeometry(QtCore.QRect(300, 280, 224, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(70)
        self.pred_label_1.setFont(font)
        self.pred_label_1.setAutoFillBackground(False)
        self.pred_label_1.setObjectName("pred_label_1")



        self.pred_prob_1 = QtWidgets.QProgressBar(self.frame)
        self.pred_prob_1.setGeometry(QtCore.QRect(300, 320, 224, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(70)
        self.pred_prob_1.setFont(font)
        self.pred_prob_1.setMinimum(0)
        self.pred_prob_1.setMaximum(100)
        self.pred_prob_1.setObjectName("pred_prob_1")


 

        self.line_1 = QtWidgets.QFrame(self.frame)
        self.line_1.setGeometry(QtCore.QRect(11, 30, 224, 16))
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")



        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Dog breed Prediction"))
        self.upload_image_main.setText(_translate("Form", ""))
        self.top3_predicted_main.setText(_translate("Form", ""))
        self.pred_label_1.setText(_translate("Form", ""))
        self.pred_label_2.setText(_translate("Form", ""))
        self.pred_label_3.setText(_translate("Form", ""))
        self.browseImageAndPredict_btn.setText(_translate("Form", "Browse Image and Predict!"))
        self.browseImageAndPredict_btn.clicked.connect(self.open_file_explorer)

    # This function is defined to bind the Browse image and Predict button.
    def open_file_explorer(self):
        f_json = open("data/unique_breeds.json", "r")
        get_images = json.load(f_json)
        filename = QFileDialog.getOpenFileName(filter=".jpg files (*.jpg)")
        path = filename[0]
        image = Image.open(path)
        new_image = image.resize((224, 224))
        new_image.save(resized_images + 'uploaded_image.jpg')
        self.uploaded_image.setPixmap(QtGui.QPixmap(resized_images + 'uploaded_image.jpg'))

        # Here we pass the uploaded image filepath to the function custom_path() to make our predictions.
        custom_path([path])
        self.filePath.setText(path)
        self.upload_image_main.setText("Uploaded Image and Path")
        self.top3_predicted_main.setText("Predicted Breed and its appetite")
        
        
         

        # Here we append the predicted labels and their respective images from the lists "top3_labels" and "confidence"
        # We are resizing the windows to make a kind of a transition animation.
        Form.resize(280, 374)
        time.sleep(0.5)
        Form.resize(1000, 374)
        self.pred_label_1.setText(top3_labels[0][0].replace("_", " ").title())
        self.pred_label_2.setText(top3_labels[0][0].replace("_", " ").title())
        self.pred_label_3.setText("MEAL \n Protein. Many manufacturers use vegetable proteins in their dog food which are hard for dogs to digest.Find a dog food that contains mostly animal protein. Dogs need a minimum of 18% protein in their diet for maintenance when they are adults and 22% for reproduction and growth. Do not overfeed your dog; too much protein can lead to hyperactivity. \n\n Fat. Fats keep your dog's coat healthy and provide energy. Do not buy fat-free dog foods. Adult dogs need a minimum of 5% fat in their diet.\n\n Vitamins. A vitamin supplement will provide those nutrients above and beyond the minimum, which are required to meet his particular needs. Consult your veterinarian to see what vitamin types and amounts your dog needs.\n\n Water- Your dog's water needs depend on his activity level. Also, eating a lot of dry food will make your dog thirsty. A good rule of thumb to follow: give your pet at least one quart of water for every pound of dry food.")
        self.pred_label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.pred_image_1.setPixmap(QtGui.QPixmap(resized_images + get_images[top3_labels[0][0]]))
        self.pred_prob_1.setProperty("value", float(confidence[0][0]))
        

              # Print the results in terminal if TERM_VIEW is True
        if TERM_VIEW:
            terminal_printer(path)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
   
    Form.show()
    
    sys.exit(app.exec_())
