from flask import Flask, render_template, request, jsonify
from googleapiclient.discovery import build
from collections import Counter
import nltk
from nltk.corpus import stopwords
import re
import os
from dotenv import load_dotenv

# Download required NLTK data
nltk.download('stopwords')
nltk.download('punkt')

app = Flask(__name__)
load_dotenv()

# Get YouTube API key from environment variable
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def extract_video_id(url):
    """Extract video ID from YouTube URL."""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?]+)',
        r'youtube\.com\/embed\/([^&\n?]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_comments(video_id):
    """Fetch comments from YouTube video using the API."""
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    comments = []
    
    try:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100
        )
        
        while request and len(comments) < 100:
            response = request.execute()
            
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)
            
            request = youtube.commentThreads().list_next(request, response)
            
    except Exception as e:
        print(f"Error fetching comments: {str(e)}")
    
    return comments

def analyze_word_frequency(comments):
    """Analyze word frequency in comments."""
    # Combine all comments
    text = ' '.join(comments)
    
    # Tokenize and clean text
    words = nltk.word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    
    # Remove stopwords and non-alphabetic characters
    words = [word for word in words if word.isalpha() and word not in stop_words]
    
    # Count word frequencies
    word_freq = Counter(words)
    
    # Convert to list of dictionaries for D3.js
    return [{'text': word, 'size': count} for word, count in word_freq.most_common(50)]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.json.get('url')
    video_id = extract_video_id(url)
    
    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400
    
    comments = get_video_comments(video_id)
    if not comments:
        return jsonify({'error': 'No comments found or error fetching comments'}), 400
    
    word_freq = analyze_word_frequency(comments)
    return jsonify(word_freq)

if __name__ == '__main__':
    app.run(debug=True) 