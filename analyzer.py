"""
Twitter Pattern Analyzer
Identifies what makes tweets viral
"""

import re
import sqlite3
from collections import Counter
from config import DB_PATH, SCORING_WEIGHTS

class PatternAnalyzer:
    def __init__(self):
        self.db_path = DB_PATH
    
    def analyze_viral_patterns(self):
        """Analyze what makes tweets viral"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get viral tweets
        cursor.execute('''
            SELECT text, likes, retweets, replies 
            FROM tweets 
            WHERE is_viral = 1
            ORDER BY likes DESC
            LIMIT 100
        ''')
        
        viral_tweets = cursor.fetchall()
        conn.close()
        
        if not viral_tweets:
            return {"status": "No viral tweets in database yet"}
        
        patterns = {
            "hooks": self._analyze_hooks(viral_tweets),
            "length": self._analyze_length(viral_tweets),
            "formatting": self._analyze_formatting(viral_tweets),
            "topics": self._analyze_topics(viral_tweets),
            "engagement_patterns": self._analyze_engagement(viral_tweets),
        }
        
        return patterns
    
    def _analyze_hooks(self, tweets):
        """Find common opening patterns in viral tweets"""
        hooks = []
        for text, likes, rt, replies in tweets:
            first_line = text.split('\n')[0][:50]
            hooks.append(first_line)
        
        # Find most common patterns
        common_hooks = Counter(hooks).most_common(10)
        
        hook_types = {
            "question": sum(1 for h, _ in common_hooks if '?' in h),
            "statement": sum(1 for h, _ in common_hooks if any(word in h.lower() for word in ["the", "it's", "you"])),
            "number": sum(1 for h, _ in common_hooks if any(char.isdigit() for char in h)),
            "contrarian": sum(1 for h, _ in common_hooks if any(word in h.lower() for word in ["actually", "don't", "not"])),
        }
        
        return {
            "most_common": [{"hook": h, "count": c} for h, c in common_hooks],
            "hook_types": hook_types
        }
    
    def _analyze_length(self, tweets):
        """Analyze optimal tweet length"""
        lengths = [len(text) for text, _, _, _ in tweets]
        
        return {
            "avg_length": round(sum(lengths) / len(lengths), 0),
            "min_length": min(lengths),
            "max_length": max(lengths),
            "most_common_range": f"{min(lengths)}-{max(lengths)} characters"
        }
    
    def _analyze_formatting(self, tweets):
        """Analyze formatting patterns"""
        formatting = {
            "threads": 0,
            "lists": 0,
            "emojis": 0,
            "line_breaks": 0,
        }
        
        for text, _, _, _ in tweets:
            if text.count('\n') > 2:
                formatting["threads"] += 1
            if '-' in text or '•' in text:
                formatting["lists"] += 1
            if any(ord(char) > 127 for char in text):
                formatting["emojis"] += 1
            formatting["line_breaks"] += text.count('\n')
        
        return formatting
    
    def _analyze_topics(self, tweets):
        """Find common topics in viral tweets"""
        keywords = Counter()
        
        common_words = {
            "build", "startup", "founder", "code", "ai", "ml", "learn", 
            "money", "business", "product", "growth", "hack", "tool",
            "automation", "python", "javascript", "marketing", "sales"
        }
        
        for text, _, _, _ in tweets:
            words = text.lower().split()
            for word in words:
                if word in common_words:
                    keywords[word] += 1
        
        return dict(keywords.most_common(15))
    
    def _analyze_engagement(self, tweets):
        """Analyze engagement ratios"""
        engagement_ratios = []
        
        for text, likes, rt, replies in tweets:
            if likes > 0:
                rt_ratio = rt / likes
                reply_ratio = replies / likes
                engagement_ratios.append({
                    "likes": likes,
                    "retweet_ratio": round(rt_ratio, 2),
                    "reply_ratio": round(reply_ratio, 2),
                })
        
        avg_rt_ratio = sum(r["retweet_ratio"] for r in engagement_ratios) / len(engagement_ratios)
        avg_reply_ratio = sum(r["reply_ratio"] for r in engagement_ratios) / len(engagement_ratios)
        
        return {
            "avg_retweet_ratio": round(avg_rt_ratio, 2),
            "avg_reply_ratio": round(avg_reply_ratio, 2),
            "high_reply_tweets": [r for r in engagement_ratios if r["reply_ratio"] > 0.2][:5]
        }
    
    def score_post_idea(self, text):
        """Score a post idea 0-100 based on patterns"""
        score = 0
        
        # Hook strength (25 points)
        if len(text) > 0:
            first_line = text.split('\n')[0]
            if '?' in first_line:
                score += 10
            if any(word in first_line.lower() for word in ["actually", "you", "the"]):
                score += 8
            if any(char.isdigit() for char in first_line):
                score += 7
        
        # Specificity (20 points)
        if any(char.isdigit() for char in text):
            score += 10
        if "%" in text or "x" in text:
            score += 10
        
        # Actionability (20 points)
        action_words = ["try", "learn", "do", "build", "start", "check out"]
        if any(word in text.lower() for word in action_words):
            score += 15
        if text.endswith("?"):
            score += 5
        
        # Originality (20 points)
        unique_phrases = len(set(text.split()))
        if unique_phrases > 15:
            score += 20
        elif unique_phrases > 10:
            score += 10
        
        # Clarity (15 points)
        line_count = text.count('\n')
        if 0 < line_count < 5:
            score += 15
        elif line_count == 0 and len(text) < 280:
            score += 10
        
        return min(100, max(0, score))

# Example usage
if __name__ == "__main__":
    analyzer = PatternAnalyzer()
    patterns = analyzer.analyze_viral_patterns()
    
    print("🔍 Viral Tweet Patterns:")
    for pattern_type, details in patterns.items():
        print(f"\n{pattern_type}:")
        if isinstance(details, dict):
            for key, value in details.items():
                print(f"  {key}: {value}")
        else:
            print(f"  {details}")
    
    # Score test post
    test_post = "Just shipped a new AI tool. It saves 10 hours/week. Here's what I learned:"
    print(f"\n📊 Test Post Score: {analyzer.score_post_idea(test_post)}/100")
