import streamlit as st
from PIL import Image, ImageDraw, ImageFont


# Function to display bedroom setup analysis result
def display_bedroom_result(analysis_result):
    st.subheader("AI Rating")
    st.write(f"**Rating:** {analysis_result.get('ai_rating', 'N/A')} / 5")

    st.subheader("Condition")
    st.write(f"**Condition:** {analysis_result.get('condition', 'N/A')}")

    st.subheader("Description")
    st.write(analysis_result.get("description", "N/A"))


# Function to display maintenance analysis result
def display_maintenance_result(analysis_result):
    if "visible_objects" in analysis_result:
        st.subheader("Visible Objects Count")
        for obj, count in analysis_result["visible_objects"].items():
            st.write(f"**{obj.capitalize()}**: {count}")

    st.subheader("Condition Analysis")
    condition_fields_mapping = {
        "Dust Free": "has_dust",
        "Tear Free": "has_tear",
        "Stain Free": "has_stain",
        "Damage Free": "is_broken",
        "Crack Free": "is_crack",
    }

    for field, json_key in condition_fields_mapping.items():
        if json_key in analysis_result:
            status = analysis_result[json_key]
            color = "green" if status else "red"
            st.markdown(
                f"**{field}:** <span style='color:{color}'>{'❌' if status else '✅'}</span>",
                unsafe_allow_html=True,
            )

    if "general_description" in analysis_result:
        st.subheader("General Description")
        st.write(analysis_result["general_description"])


# Function to display detection and counting results
def display_detection_result(analysis_result):
    if "visible_objects" in analysis_result:
        st.subheader("Object Count")
        for obj, count in analysis_result["visible_objects"].items():
            st.write(f"**{obj.capitalize()}**: {count}")
        st.write("**General Description:** ", analysis_result["general_description"])
    else:
        st.write("No objects detected.")


def display_detection_result_image(analysis_result):
    if "objects" in analysis_result:
        st.subheader("Object Count")

        # Create a dictionary to hold object counts
        object_count = {}

        # Count occurrences of each object
        for obj in analysis_result["objects"]:
            label = obj["label"]
            if label in object_count:
                object_count[label] += 1
            else:
                object_count[label] = 1

        # Display the count of each detected object
        for obj, count in object_count.items():
            st.write(f"**{obj.capitalize()}**: {count}")

        # Optionally, if there's any general description, display it (depending on your response structure)
        if "general_description" in analysis_result:
            st.write(
                "**General Description:** ", analysis_result["general_description"]
            )
    else:
        st.write("No objects detected.")


# Function to draw bounding boxes on the image
def draw_bounding_boxes(image, bounding_boxes):
    img = Image.open(image)
    draw = ImageDraw.Draw(img)
    width, height = img.size

    # Load a font
    try:
        font = ImageFont.truetype(
            "fonts/Arial.ttf", 16
        )  # Adjust the font size as necessary
    except IOError:
        font = ImageFont.load_default()

    for obj in bounding_boxes:
        label = obj["label"]
        box = obj["bounding_box"]

        # Convert the bounding box values to the image dimensions
        ymin = int((box[0] / 1000) * height)
        xmin = int((box[1] / 1000) * width)
        ymax = int((box[2] / 1000) * height)
        xmax = int((box[3] / 1000) * width)

        # Draw the bounding box
        draw.rectangle([xmin, ymin, xmax, ymax], outline="green", width=2)

        # Draw the label and confidence above the bounding box
        text = f"{label}"

        # Get the size of the text using getbbox()
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        text_x = xmin
        text_y = ymin - text_height if ymin - text_height > 0 else ymin + 5

        # Create a rectangle behind the text for better visibility
        draw.rectangle(
            [text_x, text_y, text_x + text_width, text_y + text_height], fill="green"
        )

        # Draw the label and confidence text
        draw.text((text_x, text_y), text, fill="white", font=font)

    return img
