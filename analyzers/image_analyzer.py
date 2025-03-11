from PIL import Image
import google.generativeai as genai
import os

# Configuration for generation
generation_config = {
    "temperature": 0,
    "top_p": 0.8,
    "top_k": 128,
    "max_output_tokens": 4096,
    "response_mime_type": "application/json",
}


# Function to generate response from Gemini using the uploaded image
def generate_response_image(image_file, prompt):
    # Define the prompt for Gemini model

    try:
        # Open the image and convert to binary
        image = Image.open(image_file)
        # Define the model with configuration
        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-pro", generation_config=generation_config
        )
        response = model.generate_content([prompt, image])
        return response.text

    except Exception as e:
        return {"error": f"Error in generating response from Gemini: {str(e)}"}
