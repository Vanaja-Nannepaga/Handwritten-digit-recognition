import torch
import torch.nn as nn
import numpy as np
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_drawable_canvas import st_canvas

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=5, stride=1, padding=2)  # Output: 28x28x32
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)  # Output: 14x14x32

        self.conv2 = nn.Conv2d(32, 64, kernel_size=5, stride=1, padding=2)  # Output: 14x14x64
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)  # Output: 7x7x64

        self.fc1 = nn.Linear(7 * 7 * 64, 1024)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(1024, 10)

    def forward(self, x):
        x = self.pool1(self.relu1(self.conv1(x)))
        x = self.pool2(self.relu2(self.conv2(x)))
        x = x.view(-1, 7 * 7 * 64)  # Flatten
        x = self.relu3(self.fc1(x))
        x = self.fc2(x)
        return x

model = SimpleCNN()
model.load_state_dict(torch.load("handwritten_digit_model.pth", map_location=torch.device('cpu')))
model.eval()


# Define prediction function
def predict_digit(image):
    # Convert RGBA to grayscale
    image = ImageOps.grayscale(image)
    
    # Resize to 28x28
    img = image.resize((28, 28))
    
    # Convert to NumPy array and normalize
    img = np.array(img, dtype=np.float32) / 255.0
    img = (img - 0.5) / 0.5  # Normalize to range [-1, 1]
    
    # Display the processed image
    plt.imshow(img, cmap="gray")
    plt.show()
    
    # Convert to PyTorch tensor and add batch/channel dimensions
    img_tensor = torch.tensor(img).unsqueeze(0).unsqueeze(0)  # Shape: (1, 1, 28, 28)
    
    # Predict using the model
    with torch.no_grad():
        output = model(img_tensor)
        pred = torch.argmax(output, dim=1).item()
    return pred

# Streamlit Application
st.set_page_config(page_title='HDR with Adversarial robustness', layout='wide')
st.title('Handwritten Digit Recognition with Adversarial robustness')
st.subheader("Draw the digit on canvas and click on 'Predict Now'")

# Add canvas component
drawing_mode = "freedraw"
stroke_width = st.slider('Select Stroke Width', 1, 30, 15)
stroke_color = '#FFFFFF'  # Set stroke color to white
bg_color = '#000000'  # Set background color to black

# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=200,
    width=200,
    key="canvas",
)

# Add "Predict Now" button
if st.button('Predict Now'):
    if canvas_result.image_data is not None:
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'), 'RGBA')
        
        # Save and reload the image for processing
        input_image.save('prediction/img.png')
        img = Image.open("prediction/img.png")
        
        # Predict the digit
        res = predict_digit(img)
        st.header('Predicted Digit: ' + str(res))
    else:
        st.header('Please draw a digit on the canvas..')

# Add sidebar
st.sidebar.title("About")
st.sidebar.text("Created by Model Marvericks")
st.sidebar.text("Team Members: Arey Pragna Sri, Matcha Jhansi Lakshmi, Nannepaga Vanaja")
st.sidebar.write("[GitHub Repo Link](https://github.com/pragnasri74/Handwritten-Digit-Recognition-with-adversarial-robustness)")

