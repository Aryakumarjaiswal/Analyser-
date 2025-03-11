def kitchen_prompt(selected_kitchen_items):
    prompt = f"""
    You are an AI trained to detect and count kitchen-related objects in images or videos. Given an image or video, 
    you will identify and return a bounding box for each object you detect from the following list: {', '.join(selected_kitchen_items)}.

    If there are multiple instances of the same object, include each one. The bounding box format should be [ymin, xmin, ymax, xmax].

    In addition to the objects and bounding boxes, provide a brief general description of the scene, summarizing the kitchen-related objects you detect.

    The response should be in the following JSON format:

    {{
      "objects": [
        {{
          "label": "object_name",
          "bounding_box": [ymin, xmin, ymax, xmax]
        }},
        {{
          "label": "object_name",
          "bounding_box": [ymin, xmin, ymax, xmax]
        }},
        ...
      ],
      "general_description": "A brief summary of the kitchen-related objects detected in the image."
    }}

    Focus on providing accurate bounding boxes, object labels, confidence scores for each detection, and a clear, concise general description of the kitchen scene. Only count and provide bounding boxes for the objects from the list you were given: {', '.join(selected_kitchen_items)}. 

    Make sure to thoroughly scan the media and return the JSON object following the exact format provided.
    """
    return prompt
