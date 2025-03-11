def furniture_video_prompt(selected_furniture_items):
    prompt = f"""
    You are an AI trained to detect and count furniture-related objects in visual media. Given a video, 
    you will identify and count the visible furniture items from the following list: {', '.join(selected_furniture_items)}. 
    Return a JSON object containing the following fields:

    visible_objects: A dictionary where the keys are furniture types (such as "chair", "table", "sofa", "bed", etc.) 
    and the values are the number of occurrences of each furniture item (integer).
    
    general_description: A brief summary describing the identified furniture objects and their quantities.

    Your task is to thoroughly scan the media (video) and return the appropriate JSON response, focusing only on the count of visible furniture items.

    For example, the output JSON may look like this:

    {{
        "visible_objects": {{
            "chair": 4,
            "table": 2,
            "sofa": 3
        }},
        "general_description": "The media shows 4 chairs, 2 tables, and 3 sofas."
    }}
    """
    return prompt
