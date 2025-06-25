import re
from utils.text_cleaning import clean_text

def analyze_sentiment(text):
    """
    Simple rule-based sentiment analysis
    Returns: 'Positive', 'Negative', or 'Neutral'
    """
    cleaned_text = clean_text(text).lower()
    
    # Define positive and negative words
    positive_words = [
        'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 
        'awesome', 'perfect', 'love', 'like', 'happy', 'satisfied', 'helpful',
        'useful', 'clear', 'easy', 'fast', 'quick', 'efficient', 'thank',
        'thanks', 'appreciate', 'brilliant', 'outstanding', 'superb'
    ]
    
    negative_words = [
        'bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'angry',
        'frustrated', 'disappointed', 'useless', 'confusing', 'difficult',
        'slow', 'poor', 'worst', 'annoying', 'irritating', 'problem',
        'issue', 'error', 'wrong', 'fail', 'broken', 'stupid', 'ridiculous'
    ]
    
    # Count positive and negative words
    positive_count = sum(1 for word in positive_words if word in cleaned_text)
    negative_count = sum(1 for word in negative_words if word in cleaned_text)
    
    # Determine sentiment
    if positive_count > negative_count:
        return "Positive"
    elif negative_count > positive_count:
        return "Negative"
    else:
        return "Neutral"