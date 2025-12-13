"""
Utility functions for the Facebook crawler
"""
import logging
from typing import List, Dict, Any
from datetime import datetime
import re

logger = logging.getLogger(__name__)


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and special characters

    Args:
        text: Input text

    Returns:
        Cleaned text
    """
    if not text:
        return ""
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_urls(text: str) -> List[str]:
    """
    Extract URLs from text

    Args:
        text: Input text

    Returns:
        List of URLs found
    """
    url_pattern = r"https?://[^\s]+"
    return re.findall(url_pattern, text)


def extract_mentions(text: str) -> List[str]:
    """
    Extract @mentions from text

    Args:
        text: Input text

    Returns:
        List of mentions
    """
    mention_pattern = r"@(\w+)"
    return re.findall(mention_pattern, text)


def extract_hashtags(text: str) -> List[str]:
    """
    Extract #hashtags from text

    Args:
        text: Input text

    Returns:
        List of hashtags
    """
    hashtag_pattern = r"#(\w+)"
    return re.findall(hashtag_pattern, text)


def normalize_post_data(post: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize post data for consistent formatting

    Args:
        post: Raw post dictionary

    Returns:
        Normalized post dictionary
    """
    normalized = {
        "post_id": str(post.get("post_id", "")),
        "author": clean_text(str(post.get("author", ""))),
        "timestamp": str(post.get("timestamp", "")),
        "content": clean_text(str(post.get("content", ""))),
        "highlighted_text": clean_text(str(post.get("highlighted_text", ""))),
        "likes": int(post.get("likes", 0)),
        "comments": int(post.get("comments", 0)),
        "shares": int(post.get("shares", 0)),
        "url": str(post.get("url", "")),
    }
    return normalized


def filter_posts_by_keywords(
    posts: List[Dict],
    keywords: List[str],
    case_sensitive: bool = False
) -> List[Dict]:
    """
    Filter posts containing specific keywords

    Args:
        posts: List of posts
        keywords: Keywords to filter by
        case_sensitive: Whether to perform case-sensitive matching

    Returns:
        Filtered list of posts
    """
    filtered = []

    for post in posts:
        content = post.get("content", "")
        if not case_sensitive:
            content = content.lower()
            search_keywords = [kw.lower() for kw in keywords]
        else:
            search_keywords = keywords

        if any(kw in content for kw in search_keywords):
            filtered.append(post)

    return filtered


def sort_posts_by_engagement(posts: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Sort posts by engagement (likes + comments + shares)

    Args:
        posts: List of posts
        reverse: Sort in descending order (highest engagement first)

    Returns:
        Sorted list of posts
    """
    return sorted(
        posts,
        key=lambda x: x.get("likes", 0) + x.get("comments", 0) + x.get("shares", 0),
        reverse=reverse
    )


def get_post_statistics(posts: List[Dict]) -> Dict[str, Any]:
    """
    Calculate statistics from posts

    Args:
        posts: List of posts

    Returns:
        Dictionary with statistics
    """
    if not posts:
        return {
            "total_posts": 0,
            "total_likes": 0,
            "total_comments": 0,
            "total_shares": 0,
            "avg_likes": 0,
            "avg_comments": 0,
            "avg_shares": 0,
        }

    total_likes = sum(p.get("likes", 0) for p in posts)
    total_comments = sum(p.get("comments", 0) for p in posts)
    total_shares = sum(p.get("shares", 0) for p in posts)
    num_posts = len(posts)

    return {
        "total_posts": num_posts,
        "total_likes": total_likes,
        "total_comments": total_comments,
        "total_shares": total_shares,
        "avg_likes": round(total_likes / num_posts, 2),
        "avg_comments": round(total_comments / num_posts, 2),
        "avg_shares": round(total_shares / num_posts, 2),
    }
