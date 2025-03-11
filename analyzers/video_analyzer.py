import tempfile
import time
import os
import google.generativeai as genai

# Configuration for generation
generation_config = {
    "temperature": 0,
    "top_p": 0.8,
    "top_k": 128,
    "max_output_tokens": 4096,
    "response_mime_type": "application/json",
}


def generate_response_video(video_file, prompt):
    try:
        # Get the original file name and extension
        original_filename = video_file.name
        file_extension = os.path.splitext(original_filename)[1].lower()

        # Determine the correct MIME type and suffix based on the file extension
        if file_extension == ".mp4":
            mime_type = "video/mp4"
            suffix = ".mp4"
        elif file_extension == ".mov":
            mime_type = "video/quicktime"  # Correct MIME type for MOV
            suffix = ".mov"
        else:
            raise ValueError(
                "Unsupported video format. Only .mp4 and .mov are allowed."
            )

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_video:
            temp_video.write(video_file.read())  # Write the video file to the temp file
            temp_video.flush()
            temp_video_path = temp_video.name

        video_upload = genai.upload_file(path=temp_video_path, mime_type=mime_type)

        # Polling to check status of video processing
        while video_upload.state.name == "PROCESSING":
            time.sleep(10)  # Wait for the video to be processed
            video_upload = genai.get_file(video_upload.name)

        if video_upload.state.name == "FAILED":
            raise ValueError("Video processing failed.")

        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-pro", generation_config=generation_config
        )
        response = model.generate_content(
            [prompt, video_upload], request_options={"timeout": 600}
        )

        genai.delete_file(video_upload.name)
        os.remove(temp_video_path)
        return response.text

    except Exception as e:
        return {"error": f"Error in generating response from Gemini: {str(e)}"}
