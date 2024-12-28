# Handwritten-Digit-Recognition-with-adversarial-robustness
## Overview
This repository contains the code and documentation for the Handwritten Digit Recognition with Adversarial Robustness as part of CS550 Machine Learning Course at IIT Bhilai. 
### Team Name: Model Mavericks

### Team Members:
- *Arey Pragna Sri* - 12240230
- *Matcha Jhansi Lakshmi* - 12241000
- *Nannepaga Vanaja* - 12241110
## Project Desciption 
This project focuses on improving the robustness of handwritten digit recognition using adversarial training. We implemented two CNN architectures (Simple CNN and Deep CNN) and trained them with adversarial examples generated using Projected Gradient Descent (PGD) and Fast Gradient Sign Method (FGSM). The MNIST dataset was used for training and testing.
## Methodology
![image](https://github.com/user-attachments/assets/78eb79e1-acd7-4d68-9f9b-bfa132dcbcd0)

## Importing Libraries  
We used the following libraries for building and training the models:
- *PyTorch*: For model building, training, tensor operations, and loss functions.
- *Torchvision*: For downloading and transforming the MNIST dataset.
- *NumPy*: For data manipulation and handling.

## Data Downloading and Preprocessing  
The MNIST dataset was downloaded and normalized to the range of -1 to 1. The features (images) and targets (labels) were separated for training and testing. This preprocessing step helps ensure better convergence during model training.

## Adversarial Attack Strategies

### PGD Attack  
- An iterative attack that adds small perturbations to input images in an attempt to maximize model error while keeping changes within a specified bound.

### FGSM Attack  
- A faster, single-step attack that perturbs images based on gradient calculations, aiming to mislead the model while controlling the perturbation magnitude.

## Neural Network Architectures

### Simple CNN  
- A two-layer convolutional network with max-pooling and fully connected layers.
- Structure:
  - Convolutional layers: 2
  - Max-pooling layers: 2
  - Fully connected layers: 2

### Deep CNN  
- A deeper architecture with four convolutional layers, max-pooling, and dropout to prevent overfitting.
- Structure:
  - Convolutional layers: 4
  - Max-pooling layers: 2
  - Fully connected layers: 3
  - Dropout layers to prevent overfitting.

## Creating Adversarial Datasets  
Adversarial examples were generated for both the training and testing sets using PGD and FGSM attacks. These perturbed images were combined with the clean images to create a new, augmented dataset with double the number of samples. This helps improve the model's robustness by training it on more challenging data.

## Model Training  
The models were trained using the augmented dataset with the Adam optimizer and cross-entropy loss. Training involved several epochs, during which we tracked the loss and accuracy to monitor the model's performance.

## Model Evaluation  
After training, the models were evaluated using both clean and adversarial test sets. We assessed the models' ability to classify digits correctly, even under the influence of adversarial perturbations, to gauge their robustness.

## Saving the Trained Model  
After successful training and evaluation, the models were saved in a .pth file for future use, making it easier to load and use them for predictions or further fine-tuning.

## Predicting the Output  
The trained model was used to predict labels for new, unseen images, demonstrating its ability to handle both clean and adversarially perturbed inputs. This process shows how the model can generalize and perform reliably in real-world scenarios, even in the presence of adversarial attacks.
## Observations

- Accuracy of Simple CNN: 99.19% (PGD) & 98.99% (FGSM)
- Accuracy of Deep CNN: 99.41% (PGD) & 99.22% (FGSM)


## Simple CNN PGD vs FGSM
![image](https://github.com/user-attachments/assets/f0456419-2db8-4bd2-908e-cd0533a60234)

## Simple CNN vs Deep CNN (PGD)
![image](https://github.com/user-attachments/assets/3a66c26f-be8e-4f15-9b34-6b9b1f99782a)

## Installation Guide

Follow these steps to set up and run the project:

### 1. Clone the Repository
Use the following command to clone the project repository to your local machine:
`git clone https://github.com/pragnasri74/Handwritten-Digit-Recognition-with-adversarial-robustness.git`

### Navigate to the MyApp directory and Install Necessary Dependencies
`pip install torch torchvision`
`pip install streamlit-drawable-canvas`
### Run the App
Execute the following command to start the Streamlit app:
`streamlit run app.py`
### Now Explore the handwritten digit recognition with adversarial robustness!!

