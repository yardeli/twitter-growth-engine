"""
Twitter Data Collector
Scrapes tweets and metrics from top accounts to find patterns
"""

import json
import sqlite3
from datetime import datetime
from config import TARGET_ACCOUNTS, VIRAL_THRESHOLDS, DB_PATH

class TwitterDataCollector:
    def __init__(self):
        self.db_path = DB_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for storing tweets"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tweets (
                id TEXT PRIMARY KEY,
                author TEXT NOT NULL,
                text TEXT NOT NULL,
                likes INTEGER DEFAULT 0,
                retweets INTEGER DEFAULT 0,
                replies INTEGER DEFAULT 0,
                impressions INTEGER DEFAULT 0,
                url TEXT,
                posted_at TIMESTAMP,
                collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_viral INTEGER DEFAULT 0,
                is_thread INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_name TEXT NOT NULL,
                description TEXT,
                frequency INTEGER,
                avg_engagement REAL,
                examples TEXT,
                discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS post_ideas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                score REAL,
                pattern_id INTEGER,
                based_on TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                posted INTEGER DEFAULT 0,
                FOREIGN KEY(pattern_id) REFERENCES patterns(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Database initialized at {self.db_path}")
    
    def log_tweet(self, author, text, likes, retweets, replies, impressions=0, url="", posted_at=None):
        """Log a tweet to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        tweet_id = f"{author}_{hash(text) % 1000000}"
        is_viral = 1 if likes >= VIRAL_THRESHOLDS["likes_min"] else 0
        is_thread = 1 if text.count("1/") > 0 else 0
        
        cursor.execute('''
            INSERT OR REPLACE INTO tweets 
            (id, author, text, likes, retweets, replies, impressions, url, posted_at, is_viral, is_thread)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (tweet_id, author, text, likes, retweets, replies, impressions, url, posted_at, is_viral, is_thread))
        
        conn.commit()
        conn.close()
        return tweet_id
    
    def get_viral_tweets(self):
        """Get all viral tweets from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT author, text, likes, retweets, replies, url
            FROM tweets
            WHERE is_viral = 1
            ORDER BY likes DESC
            LIMIT 50
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                "author": r[0],
                "text": r[1],
                "likes": r[2],
                "retweets": r[3],
                "replies": r[4],
                "url": r[5]
            }
            for r in results
        ]
    
    def save_pattern(self, pattern_name, description, frequency, avg_engagement, examples):
        """Save discovered pattern"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO patterns 
            (pattern_name, description, frequency, avg_engagement, examples)
            VALUES (?, ?, ?, ?, ?)
        ''', (pattern_name, description, frequency, avg_engagement, json.dumps(examples)))
        
        conn.commit()
        conn.close()
    
    def get_stats(self):
        """Get statistics from collected data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM tweets')
        total_tweets = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM tweets WHERE is_viral = 1')
        viral_tweets = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(likes) FROM tweets')
        avg_likes = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT AVG(retweets) FROM tweets')
        avg_retweets = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "total_tweets": total_tweets,
            "viral_tweets": viral_tweets,
            "avg_likes": round(avg_likes, 1),
            "avg_retweets": round(avg_retweets, 1),
            "viral_percentage": round((viral_tweets / total_tweets * 100) if total_tweets > 0 else 0, 1)
        }

# Example usage
if __name__ == "__main__":
    collector = TwitterDataCollector()
    
    # Example: Log some sample tweets
    collector.log_tweet(
        author="naval",
        text="The best education is learning from people you respect.",
        likes=5230,
        retweets=1240,
        replies=450,
        url="https://twitter.com/naval/status/123"
    )
    
    print("📊 Database Stats:")
    stats = collector.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
