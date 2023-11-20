import os
from flask import Flask, request, render_template
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
model = load_model("inception-v3.h5")
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction.html')
def prediction():
    return render_template('prediction.html')

@app.route('/index.html')
def home():
    return render_template("index.html")

@app.route('/result', methods=["GET", "POST"])
def res():
    if request.method == "POST":
        f = request.files['image']
        basepath = os.path.dirname(__file__)
        upload_folder = os.path.join(basepath, 'uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        filepath = os.path.join(upload_folder, f.filename)
        f.save(filepath)

        img = Image.open(filepath).convert('RGB')
        img = img.resize((256, 256))  
        x = np.array(img)
        x = np.expand_dims(x, axis=0)
        x = x / 255.0  

        predictions = model.predict(x)

        class_names = ['Amoeba', 'Euglena', 'Hydra', 'Paramecium', 'Rod_bacteria', 'Spherical_bacteria', 'Spiral_bacteria', 'Yeast']
        predicted_class = class_names[np.argmax(predictions)]

        
        plt.imshow(img)
        plt.title(f"Predicted Class: {predicted_class}")
        plt.axis('off')
        plt.show()

        return render_template('prediction.html', prediction=predicted_class)

if __name__ == "__main__":
    app.run()

# import re
# import numpy as np
# import os
# from flask import Flask, app, request, render_template
# from tensorflow.keras import models
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
# from tensorflow.python.ops.gen_array_ops import concat
# from tensorflow.keras.applications.inception_v3 import preprocess_input

# model =  load_model("inception-v3.h5") 
# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/prediction.html')
# def prediction():
#     return render_template('prediction.html')

# @app.route('/index.html')
# def home():
#     return render_template("index.html")

# @app.route('/result',methods = ["GET","POST"])
# def res():
#     if request.method == "POST":
#         f=request.files['image']
#         basepath = os.path.dirname(__file__)
#         filepath = os.path.join(basepath,'uploads',f.filename)
#         f.save(filepath)

#         img = image.load_img(filepath,target_size=(299,299))
#         x = image.img_to_array(img)
#         x = np.expand_dims(x,axis=0)
#         x /= 255.0  # Normalize the pixel values
#         predictions = model.predict(x)

#         class_names = ['Amoeba', 'Euglena', 'Hydra', 'Paramecium', 'Rod_bacteria', 'Spherical_bacteria', 'Spiral_bacteria', 'Yeast']
#         predicted_class = class_names[np.argmax(predictions)]

#         # Print the predicted class
#         plt.imshow(img)
#         plt.title(f"Predicted Class: {predicted_class}")
#         plt.axis('off')
#         plt.show()
#         return render_template('prediction.html',prediction=result)
        
# if __name__ == "__main__":
#     app.run()