def kitchen_video_prompt(selected_kitchen_items):
    prompt = f"""
    You are an AI trained to detect and count kitchen-related objects in visual media. Given a video, 
    you will identify and count the visible kitchen items from the following list: {', '.join(selected_kitchen_items)}.
    Return a JSON object containing the following fields:

    visible_objects: A dictionary where the keys are kitchen items (such as "spoon", "fork", "plate", "cooking pan", etc.) 
    and the values are the number of occurrences of each item (integer).
    
    general_description: A brief summary describing the identified kitchen objects and their quantities.

    Your task is to thoroughly scan the media (video) and return the appropriate JSON response, focusing only on the count of visible kitchen items.

    For example, the output JSON may look like this:

    {{
        "visible_objects": {{
            "spoon": 4,
            "fork": 5,
            "plate": 6
        }},
        "general_description": "The media shows 4 spoons, 5 forks, and 6 plates."
    }}
    """
    return prompt
