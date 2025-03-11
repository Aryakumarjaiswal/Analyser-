# Hotel Room Analyzer

![app](https://github.com/user-attachments/assets/b7965c4d-6851-45fd-bca2-fc84eb8fbd34)


The **Hotel Room Analyzer** is a Streamlit application that allows users to analyze hotel room setups, perform maintenance checks, and detect and count objects in images or videos. It uses Google Gemini (Generative AI) for image and video analysis, providing insightful feedback on the state of rooms and various objects.

## Features

- **Bedroom Setup Check**: Analyze images or videos of hotel rooms to determine if they are in a presentable condition for guests.
- **Maintenance Mode**: Perform a detailed maintenance check, detecting issues such as dust, tears, stains, cracks, and broken objects.
- **Detection & Counting**: Detect and count objects in various modes (General, Kitchen, Furniture) from images or videos.
  
## File Structure

```bash
.
├── analyzers/
│   ├── image_analyzer.py          # Handles image analysis
│   ├── video_analyzer.py          # Handles video analysis
├── components/
│   ├── display.py                 # Functions to display results in Streamlit
├── prompts/
│   ├── bedroom_prompt.py          # Prompt for bedroom setup analysis
│   ├── maintenance_prompt.py      # Prompt for maintenance analysis
│   ├── detect_and_count.py        # Prompt for general object detection
│   ├── kitchen_mode_prompt.py     # Prompt for kitchen mode detection
│   ├── furniture_mode_prompt.py   # Prompt for furniture mode detection
├── app.py                         # Main Streamlit app
├── requirements.txt               # Python dependencies
└── README.md                      # Project description
```

## Installation

### Prerequisites

- Python 3.8 or higher
- A Google Cloud account with access to the Gemini API (Generative AI)
- Streamlit for the web application interface

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/hotel-room-analyzer.git
   cd hotel-room-analyzer
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Google Gemini API key:

   Create a `.env` file in the root directory and add your API key like this:

   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```

4. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

## Usage

1. **Choose Analysis Mode**: When the app loads, you will be prompted to choose between:
   - **Bedroom Setup Check**
   - **Maintenance**
   - **Detection & Counting**

2. **Upload Media**: 
   - For **images**, you can upload files with extensions: `.png`, `.jpg`, `.jpeg`.
   - For **videos**, only `.mp4` is accepted.

3. **Analyze**:
   - Based on the mode and media type, the app will analyze the content and display the results.
   - The results are presented in a user-friendly format with relevant insights.

### Example Outputs:

- **Bedroom Setup Check**:
  ```json
  {
      "ai_rating": 4,
      "condition": "great",
      "description": "The room is well arranged, with the bed and pillows properly set."
  }
  ```

- **Maintenance**:
  ```json
  {
      "has_dust": false,
      "has_tear": true,
      "has_stain": false,
      "is_broken": false,
      "is_crack": true,
      "general_description": "Visible tear and crack, but no dust or stains."
  }
  ```

- **Detection & Counting**:
  ```json
  {
      "visible_objects": {
          "spoon": 4,
          "fork": 5,
          "plate": 6,
          "glass": 3
      },
      "general_description": "The image shows 4 spoons, 5 forks, 6 plates, and 3 glasses."
  }
  ```

## File Structure Explanation

- **analyzers/**: Contains the core logic for interacting with the Google Gemini API for both image and video analysis.
- **components/**: Handles the UI components and how the analysis results are displayed in Streamlit.
- **prompts/**: Contains the various prompts used to query the Gemini API for different modes (Bedroom Setup, Maintenance, Detection & Counting).
- **app.py**: The main entry point for the Streamlit app, where users can interact with the interface and choose the type of analysis.
- **requirements.txt**: Lists all the dependencies required to run the application.

## License

This project is licensed under the MIT License.
