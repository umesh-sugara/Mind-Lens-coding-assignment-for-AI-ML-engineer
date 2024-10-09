import os
import base64
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import openai
from openai import OpenAI
import instructor
from PIL import Image
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')
# Set your OpenAI API Key
openai.api_key = openai_api_key
client = instructor.patch(OpenAI())

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if an image file is uploaded
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Save the file to uploads directory
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(image_path)

        # Process the image
        base64_image = encode_image(image_path)

        try:
            # Prepare the OpenAI API request
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Instructions:

                                Tasks: 
                                ● Object Identification: 
                                    ○ Detect specific objects in the image and display the count for each: 
                                        ■ Screens (monitors, laptops, etc.) 
                                        ■ Laptops 
                                        ■ Keyboard and mouse 
                                    ○ Output Requirement: Display the results in a table format showing each element and its count. 
                                ● Back Support Analysis: 
                                    ○ Determine which parts of the person back (upper, mid, lower) are in contact with the chair’s back support. 
                                    ○ For each section, specify whether it is "Supported" or "Not Supported." 
                                    ○ Output Requirement: Display the analysis for upper, mid, and lower back in a simple list format. 
                                ● Distance from Screen Analysis: 
                                    ○ Measure the distance between the person and the screen. 
                                    ○ Indicate whether the distance is "Less than one arm’s length," "One arm’s length," or "More than one arm’s length." 
                                    ○ Output Requirement: Just Display the distance assessment clearly on the result screen.

                                Dont include any further instuction like "I hope this helps! If you need further assistance, feel free to ask."
                                or "You can adjust the counts and analysis based on the most accurate assessment of the image"
                            """,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }],
                max_tokens=300,
            )
        
            # Get the response content
            response_content = response.choices[0].message.content

            # Extract the part between ### Object Identification and the first line after ### Distance from Screen Analysis
            start = response_content.find("### Object Identification") 
            end = response_content.find("### Distance from Screen Analysis")
            if start != -1 and end != -1:
                # Extract content between the headers
                processed_content = response_content[start:].strip()
            else:
                processed_content = response_content  # Fallback if markers are not found
            
        except Exception as e:
            flash(f"Error during API call: {str(e)}")
            return redirect(request.url)

        # Return the results to the index.html template
        return render_template('index.html', image_path=url_for('uploaded_file', filename=file.filename), response_content=processed_content)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
