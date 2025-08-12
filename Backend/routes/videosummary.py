from flask import request
from flask_restful import Resource
from flask_login import login_required, current_user
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore
from transformers import pipeline  # type: ignore
from datetime import datetime
from extension import db
from models.lecture import Lecture
import re

# Initialize summarization pipeline
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6",
    device=-1  # CPU
)

def get_video_id(youtube_url):
    """Extract YouTube video ID from both youtube.com and youtu.be URLs."""
    parsed_url = urlparse(youtube_url)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        query_params = parse_qs(parsed_url.query)
        return query_params.get('v', [None])[0]
    if parsed_url.hostname in ['youtu.be']:
        return parsed_url.path.lstrip('/')
    return None


# def add_fake_punctuation(text, every_n=15):
#     """Add fake punctuation to improve summarizer results."""
#     question_triggers = {'did you know', 'have you noticed', 'can you guess', 'do you think'}
#     words, result, chunk = text.split(), [], []

#     for idx, word in enumerate(words, 1):
#         chunk.append(word)
#         if len(chunk) >= every_n:
#             joined = ' '.join(chunk).strip()
#             punctuated = (joined.rstrip('.!?') + 
#                           ('?' if any(joined.lower().startswith(q) for q in question_triggers) else '.'))
#             result.append(punctuated)
#             chunk = []

#     if chunk:
#         joined = ' '.join(chunk).strip()
#         result.append(joined.rstrip('.!?') + '.')

#     return ' '.join(s.capitalize() for s in result)

def add_fake_punctuation(text, every_n=15):
    """
    Return the text as-is, without adding any punctuation.
    """
    return text

def split_into_chunks(text, max_tokens=500):
    """Split long text into smaller chunks for summarization."""
    words = text.split()
    return [' '.join(words[i:i + max_tokens]) for i in range(0, len(words), max_tokens)]


def fetch_transcript_text(youtube_url):
    """Fetch and clean YouTube transcript."""
    video_id = get_video_id(youtube_url)
    if not video_id:
        return None, "Invalid YouTube URL or no video ID found."

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        cleaned_text = " ".join(
            line['text'] for line in transcript if line['text'].strip() and '[Music]' not in line['text']
        )
        return add_fake_punctuation(cleaned_text), None
    except Exception as e:
        return None, f"Could not fetch transcript: {e}"


def generate_summary(text):
    """Generate summary using HuggingFace pipeline."""
    chunks = split_into_chunks(text)
    summary_parts = []

    for idx, chunk in enumerate(chunks, 1):
        try:
            result = summarizer(chunk, max_length=200, min_length=50, do_sample=False)
            summary_parts.append(result[0]['summary_text'].strip())
        except Exception as e:
            print(f"Summarization failed for chunk {idx}: {e}")

    return " ".join(summary_parts)


class VideoSummaryResource(Resource):
    def get(self, lecture_id):
        """Generate and return a summary for a lecture's YouTube video."""
        lecture = Lecture.query.get(lecture_id)
        if not lecture or not lecture.link:
            return {"error": "Lecture not found or missing link."}, 404

        transcript, error = fetch_transcript_text(lecture.link)
        if error:
            return {"error": error}, 500

        summary = generate_summary(transcript)
        if not summary:
            return {"error": "Failed to generate summary."}, 500

        return {
            "lecture_id": lecture_id,
            "summary": summary,
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }, 200
# This code provides a RESTful API endpoint to generate summaries for YouTube videos linked to lectures.