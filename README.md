# YouTube Comments Word Cloud

This application analyzes YouTube video comments and creates an interactive word cloud visualization of the most frequently used words.

## Features

- Fetches comments from YouTube videos using the YouTube Data API
- Processes and analyzes comment text to find the most common words
- Creates an interactive bubble chart visualization using D3.js
- Drag and drop functionality for the word bubbles
- Responsive design with modern UI

## Prerequisites

- Python 3.7 or higher
- YouTube Data API key

## Setup

1. Clone this repository
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your YouTube API key:
   ```
   YOUTUBE_API_KEY=your_api_key_here
   ```
   You can get a YouTube API key from the [Google Cloud Console](https://console.cloud.google.com/).

## Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to `http://localhost:5000`
3. Enter a YouTube video URL and click "Analyze Comments"

## Usage

1. Paste a YouTube video URL in the input field
2. Click "Analyze Comments" to start the analysis
3. Wait for the visualization to load
4. Interact with the word bubbles:
   - Hover over bubbles to see them highlighted
   - Drag bubbles to rearrange them
   - The size of each bubble represents the frequency of the word

## Note

- The application fetches up to 100 comments from the video
- Common words (stopwords) are filtered out from the analysis
- The visualization shows the top 50 most frequent words
# vibecoding
