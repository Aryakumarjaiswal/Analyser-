import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from analyzers.image_analyzer import generate_response_image
from analyzers.video_analyzer import generate_response_video
from components.display import (
    display_bedroom_result,
    display_maintenance_result,
    display_detection_result,
    display_detection_result_image,
    draw_bounding_boxes,
)
import concurrent.futures
from prompts.bedroom_prompt import bedroom_prompt
from prompts.maintenance_prompt import maintenance_prompt
from prompts.general_prompt import general_prompt
from prompts.general_video_prompt import general_video_prompt
from prompts.kitchen_prompt import kitchen_prompt
from prompts.furniture_prompt import furniture_prompt
from prompts.furniture_video_prompt import furniture_video_prompt
from prompts.kitchen_video_prompt import kitchen_video_prompt
import os
import base64
import google.generativeai as genai
import json
import tempfile
from io import BytesIO


def video_to_base64(video_file):
    """
    Convert a video file to a Base64-encoded string.

    Args:
        video_file: A file-like object representing the video.

    Returns:
        str: A Base64-encoded string of the video file.
    """
    video_data = video_file.read()
    encoded_video = base64.b64encode(video_data).decode("utf-8")
    return f"data:video/mp4;base64,{encoded_video}"


# Function to save uploaded video as a temporary file
def save_temp_video(video_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(video_file.read())
        temp_video.flush()
        return temp_video.name


# Function to handle JSON parsing with error handling
def safe_json_loads(response_text):
    
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        st.error("There was an issue processing the response. Please try again.")
        return None


# Function to encode the uploaded image to Base64
def encode_image_to_base64(image_file):
    image_data = image_file.read()
    encoded_image = base64.b64encode(image_data).decode()
    return f"data:image/jpeg;base64,{encoded_image}"


def pil_to_base64(image: Image.Image, format: str = "PNG") -> str:
    """
    Convert a PIL image to a Base64-encoded string.

    Args:
        image (Image.Image): The PIL image to convert.
        format (str): The format to save the image in (e.g., "PNG", "JPEG"). Defaults to "PNG".

    Returns:
        str: Base64-encoded string of the image.
    """
    # Create an in-memory byte buffer
    buffer = BytesIO()
    # Save the image to the buffer in the specified format
    image.save(buffer, format=format)
    # Retrieve the byte data from the buffer
    buffer.seek(0)
    image_bytes = buffer.read()
    # Encode the byte data to Base64
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    return image_base64


# Configure the Google API key (Set it in your environment)
if os.getenv("GEMINI_API_KEY") is None:
    st.error("API key not found. The app will not function appropriately.")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# Add logo using raw HTML
logo_path = os.path.join("static", "logo.png")

if os.path.exists(logo_path):
    # Use the base64 module to encode the logo
    with open(logo_path, "rb") as logo_file:
        logo_data = logo_file.read()
    encoded_logo = f"data:image/jpeg;base64,{base64.b64encode(logo_data).decode()}"

    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="{encoded_logo}" alt="logo" style="max-width: 200px;">
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.warning(f"Logo file not found at {logo_path}")
    st.write("Current working directory:", os.getcwd())
    st.write("Files in current directory:", os.listdir())

# Streamlit App
st.title("Maitri AI Intellinspect")

# User selects the analysis mode
mode = st.radio(
    "Choose an analysis mode:",
    ("Inspection", "Maintenance", "Detection & Counting"),
)

if mode == "Inspection":
    media_type = st.radio("Select media type:", ("Image", "Video"))
    
    if media_type == "Image":
        media_files = st.file_uploader(
            "Upload images to analyze", type=["png", "jpg", "jpeg"], accept_multiple_files=True
        )
    else:
        media_files = st.file_uploader("Upload a video to analyze", type=["mp4"])

    analysis_result = None  # Initialize analysis_result to use in both cases

    if media_files:
        if media_type == "Image":
            st.write("Analyzing images concurrently... Please wait.")

            def process_image(image_file):
                encoded_image = encode_image_to_base64(image_file)
                result = generate_response_image(image_file, prompt=bedroom_prompt)
                return {"image": encoded_image, "result": result}

            # Use ThreadPoolExecutor for concurrent image processing
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_image = {executor.submit(process_image, img): img for img in media_files}  

                analysis_results = []  # Keep this as a list

                for future in concurrent.futures.as_completed(future_to_image):
                    result = future.result()
                    analysis_results.append(result["result"])  # Append only result text

                    st.markdown(
            f'<img src="{result["image"]}" alt="Uploaded Image" style="max-width: 100%;">',
            unsafe_allow_html=True,
        )
                    
                    if isinstance(result["result"], dict):
                        parsed_result = result["result"]
                    else:
                        parsed_result = safe_json_loads(result["result"])  # Parse result safely
                    if parsed_result:
                        display_bedroom_result(parsed_result)
                    else:
                        st.write("Failed to analyze the room or parse the response.")
                   

    # Debugging: Print parsed AI response

        





        elif media_type == "Video":
            st.write("Processing the video... Please wait.")
            video_data = media_files.read()
            media_files.seek(0)

            # Create a copy for displaying the video
            video_copy_for_display = BytesIO(video_data)

            # Pass the original media_file to the analysis function
            analysis_result = generate_response_video(media_files, prompt=bedroom_prompt)

            # Encode the video copy for display
            encoded_video = base64.b64encode(video_copy_for_display.read()).decode("utf-8")

            # Embed the video in an HTML <video> tag
            st.markdown(
                f"""
                <video controls style="max-width: 100%;">
                    <source src="data:video/mp4;base64,{encoded_video}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                """,
                unsafe_allow_html=True,
            )

            if analysis_result:
                analysis_result = safe_json_loads(analysis_result)
                if analysis_result:
                    display_bedroom_result(analysis_result)
            else:
                st.write("Failed to analyze the room or parse the response.")
            
# File uploader section based on selected mode

elif mode == "Maintenance":
    media_type = st.radio("Select media type:", ("Image", "Video"))
    if media_type == "Image":
        media_file = st.file_uploader(
            "Upload an image for maintenance analysis", type=["png", "jpg", "jpeg"],accept_multiple_files=True
        )
    else:
        media_file = st.file_uploader(
            "Upload a video for maintenance analysis", type=["mp4"]
        )

    if media_file:
        if media_type == "Image":
            def process_image(image_file):
                encoded_image = encode_image_to_base64(image_file)
                result = generate_response_image(image_file, prompt=maintenance_prompt)
                return {"image": encoded_image, "result": result}
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_image = {executor.submit(process_image, img): img for img in media_file}  

                analysis_results = []  # Keep this as a list

                for future in concurrent.futures.as_completed(future_to_image):
                    result = future.result()
                    analysis_results.append(result["result"])  # Append only result text

                    st.markdown(
            f'<img src="{result["image"]}" alt="Uploaded Image" style="max-width: 100%;">',
            unsafe_allow_html=True,
        )
                    
                    if isinstance(result["result"], dict):
                        parsed_result = result["result"]
                    else:
                        parsed_result = safe_json_loads(result["result"])  # Parse result safely
                    if parsed_result:
                        display_maintenance_result(parsed_result)
                    else:
                        st.write("Failed to analyze the room or parse the response.")
                   
            

        elif media_type == "Video":
            st.write("Detecting objects in the video... Please wait.")
            video_data = media_file.read()

            media_file.seek(0)
            # Create two independent file-like objects
            video_copy_for_display = BytesIO(video_data)

            # Pass the original media_file to the analysis function
            analysis_result = generate_response_video(
                media_file, prompt=maintenance_prompt
            )

            # Encode the video copy for display
            encoded_video = base64.b64encode(video_copy_for_display.read()).decode(
                "utf-8"
            )

            # Embed the video in an HTML <video> tag
            st.markdown(
                f"""
                <video controls style="max-width: 100%;">
                    <source src="data:video/mp4;base64,{encoded_video}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                """,
                unsafe_allow_html=True,
            )

            if analysis_result:
                analysis_result = safe_json_loads(analysis_result)
                if analysis_result:
                    display_maintenance_result(analysis_result)
            else:
                st.write("Failed to analyze for maintenance or parse the response.")

elif mode == "Detection & Counting":
    # Dropdown for detection mode selection
    detection_mode = st.selectbox(
        "Select Detection Mode:", ("General Mode", "Kitchen Mode", "Furniture Mode")
    )

    media_type = st.radio("Select media type:", ("Image", "Video"))

    # Set the correct prompt based on the detection mode
    if detection_mode == "Kitchen Mode":
        # Multi-select for kitchen objects
        kitchen_items = [
            "cup",
            "plate",
            "spoon",
            "fork",
            "knife",
            "scissor",
            "glass",
            "container",
            "cooking pan",
            "big serving spoon",
            "oven",
            "coffee maker",
            "mixer",
        ]
        selected_kitchen_items = st.multiselect(
            "Select kitchen objects to detect:", kitchen_items, default=kitchen_items
        )
        if media_type == "Image":
            prompt = kitchen_prompt(selected_kitchen_items)
        else:
            prompt = kitchen_video_prompt(selected_kitchen_items)

    elif detection_mode == "Furniture Mode":
        # Multi-select for furniture objects
        furniture_items = [
            "sofa",
            "pillow",
            "bed",
            "chair",
            "table",
            "planter",
            "artifact",
            "painting",
            "musical instrument",
            "carpet",
            "fish tank",
        ]
        selected_furniture_items = st.multiselect(
            "Select furniture objects to detect:",
            furniture_items,
            default=furniture_items,
        )

        if media_type == "Image":
            prompt = furniture_prompt(selected_furniture_items)
        else:
            prompt = furniture_video_prompt(selected_furniture_items)

    # General Mode
    else:
        if media_type == "Image":
            prompt = general_prompt
        else:
            prompt = general_video_prompt

    # Set file type restrictions
    if media_type == "Image":
        media_file = st.file_uploader(
            "Upload an image for object detection and counting",
            type=["png", "jpg", "jpeg"],accept_multiple_files=True
        )
    else:
        media_file = st.file_uploader(
            "Upload a video for object detection and counting", type=["mp4"]
        )

    if media_file:
        if media_type == "Image":
            # Show the uploaded image
            st.write("Processing images concurrently... Please wait.")

            def process_image(image_file):
                """Processes an image and returns analysis results."""
                encoded_image = encode_image_to_base64(image_file)
                analysis_result = generate_response_image(image_file, prompt=prompt)
                return {"image": encoded_image, "result": analysis_result}

    # Use ThreadPoolExecutor for parallel processing
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_image = {executor.submit(process_image, img): img for img in media_file}

                for future in concurrent.futures.as_completed(future_to_image):

                    result = future.result()

            # Display uploaded image
                    st.markdown(
                f'<img src="{result["image"]}" alt="Uploaded Image" style="max-width: 100%;">',
                unsafe_allow_html=True,
            )

            # Process and display the analysis result
                    if isinstance(result["result"], str):  
                        analysis_result = safe_json_loads(result["result"])
                    else:
                        analysis_result = result["result"]

                    if analysis_result and "objects" in analysis_result:
                        bounding_boxes = analysis_result["objects"]

                        if bounding_boxes:
                            image_with_boxes = draw_bounding_boxes(future_to_image[future], bounding_boxes)
                            image_format = image_with_boxes.format if image_with_boxes.format else "JPEG"
                            encoded_image = pil_to_base64(image_with_boxes, format=image_format)

                    # Display image with bounding boxes
                            st.markdown(
                        f'<img src="data:image/{image_format.lower()};base64,{encoded_image}" alt="Detected Objects" style="max-width: 100%;">',
                        unsafe_allow_html=True,
                    )
                        else:
                            st.write("No objects detected.")

                    display_detection_result_image(analysis_result)

        elif media_type == "Video":
            st.write("Detecting objects in the video... Please wait.")
            video_data = media_file.read()

            media_file.seek(0)
            # Create two independent file-like objects
            video_copy_for_display = BytesIO(video_data)

            # Pass the original media_file to the analysis function
            analysis_result = generate_response_video(media_file, prompt=prompt)

            # Encode the video copy for display
            encoded_video = base64.b64encode(video_copy_for_display.read()).decode(
                "utf-8"
            )

            # Embed the video in an HTML <video> tag
            st.markdown(
                f"""
                <video controls style="max-width: 100%;">
                    <source src="data:video/mp4;base64,{encoded_video}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                """,
                unsafe_allow_html=True,
            )

            if analysis_result:
                analysis_result = safe_json_loads(analysis_result)
                if analysis_result:
                    display_detection_result(analysis_result)
        else:
            st.write("Failed to analyze the video or parse the response.")
