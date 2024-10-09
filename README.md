# AI-Image Analyzer
The goal of this assignment is to develop a simple app that analyzes images of a person's workspace setup. The app will perform specific tasks based on the uploaded image, providing clear and actionable results on the screen.

## Objective
Build an app that allows users to upload an image of a workspace and returns an analysis with specific findings. The analysis will focus on identifying workstation objects, assessing back support, and evaluating the distance from the screen. Provide clear instructions on what kind of images can be uploaded. [side angle, top angle etc.] 

![image](https://github.com/user-attachments/assets/aee029c5-5bf1-48d7-82c7-c42df12ad276)

![image](https://github.com/user-attachments/assets/a0e55a31-5c10-4462-be91-8ecceebc2b2f)

## Files Overview
  - requirements.txt :  This file contains all the necessary modules that need to pre-install before running the project.
  - app.py: This is the main pyhon flask application which contains the actual logic for image analyzing.
  - .env: This configuiration file stores OPENAI_API_KEY. User need to update this api key to run the code.
  - templates/index.html: This directory stores the html file to prepare the frontend of the application.
  - uploads: This directory stores all the images that are uploaded by the user.

## Setup Instructions
1. **Clone the Repository**

   ```bash
   git clone git@github.com:umesh-sugara/Catalys-Task.git
   
2. **Create and activate a virtual environment:**

   - Windows
     ```bash
      python -m venv venv
      .\venv\Scripts\activate
    - macOS/Linux:
       ```bash
        python3 -m venv venv
        source venv/bin/activate

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt


## Note
 - Update the .env file with your own OPENAI_API_KEY

## Usage

  - Run the app:
     ```bash
     python app.py

  - Upload an image of a workspace setup (side or top angle) via the app's interface.

  - View the analysis results, including object identification, back support assessment, and screen distance evaluation.

## Feedback
 - For further enquires reach out to umeshratansinghsugara@gmail.com || https://in.linkedin.com/in/umesh-sugara
