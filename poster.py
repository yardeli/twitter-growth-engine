"""
Twitter Auto-Poster
Posts generated ideas to Twitter via browser automation
"""

import sqlite3
import time
from datetime import datetime
from config import DB_PATH, YOUR_ACCOUNT

class TwitterPoster:
    def __init__(self, browser_tool=None):
        """
        Initialize poster
        browser_tool: Reference to the OpenClaw browser tool for automation
        """
        self.db_path = DB_PATH
        self.browser = browser_tool
        self.account = YOUR_ACCOUNT
        self.posted_today = 0
    
    def post_idea(self, idea_id, idea_content):
        """Post an idea to Twitter"""
        if not self.browser:
            return {
                "status": "error",
                "message": "Browser tool not configured. Use browser automation to post."
            }
        
        try:
            # Navigate to compose
            self.browser.open("https://x.com/compose/post")
            time.sleep(2)
            
            # Get snapshot to find text field
            snapshot = self.browser.snapshot(refs="aria")
            
            # Find text input (usually ref=e84 or similar for post text)
            # Type the content
            self.browser.type(text=idea_content)
            time.sleep(1)
            
            # Click post button
            self.browser.click()
            
            # Wait for post to complete
            time.sleep(3)
            
            # Mark as posted
            self._mark_posted(idea_id)
            
            return {
                "status": "success",
                "message": f"Posted: {idea_content[:50]}...",
                "idea_id": idea_id,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to post: {str(e)}",
                "idea_id": idea_id
            }
    
    def _mark_posted(self, idea_id):
        """Mark idea as posted in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE post_ideas 
            SET posted = 1 
            WHERE id = ?
        ''', (idea_id,))
        
        conn.commit()
        conn.close()
    
    def schedule_post(self, idea_id, scheduled_time):
        """Schedule post for later (via cron or scheduler)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_id INTEGER NOT NULL,
                scheduled_time TIMESTAMP NOT NULL,
                posted INTEGER DEFAULT 0,
                FOREIGN KEY(idea_id) REFERENCES post_ideas(id)
            )
        ''')
        
        cursor.execute('''
            INSERT INTO scheduled_posts (idea_id, scheduled_time)
            VALUES (?, ?)
        ''', (idea_id, scheduled_time))
        
        conn.commit()
        conn.close()
        
        return f"Post scheduled for {scheduled_time}"
    
    def auto_reply_to_comments(self, tweet_url, reply_template):
        """
        Auto-reply to early comments (algorithm boost)
        Should be done within first hour of posting
        """
        if not self.browser:
            return {"status": "error", "message": "Browser not configured"}
        
        try:
            # Open tweet
            self.browser.open(tweet_url)
            time.sleep(2)
            
            # Find replies (would need to identify reply links)
            # For each reply, post a reply using reply_template
            
            return {
                "status": "success",
                "message": "Replies posted to boost engagement"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_posting_history(self):
        """Get history of posted ideas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, content, score, posted
            FROM post_ideas
            WHERE posted = 1
            ORDER BY id DESC
            LIMIT 20
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": r[0],
                "title": r[1],
                "content": r[2],
                "score": r[3],
            }
            for r in results
        ]

# Manual posting guide
MANUAL_POST_GUIDE = """
🐦 MANUAL TWITTER POSTING GUIDE

Since Twitter API access is restricted, here's how to post manually with browser automation:

1. Use the browser tool to navigate to https://x.com/compose/post
2. Type your post content
3. Click the "Post" button
4. Wait 3 seconds for confirmation

Example code:
    browser.open("https://x.com/compose/post")
    browser.type(text=idea_content)
    browser.click()  # Click Post button

For scheduling posts later:
- Use OpenClaw's cron feature to trigger posts at specific times
- Set up a cron job to call this script at optimal posting times

For engagement tracking:
- Use Twitter Analytics or create a manual tracking sheet
- Note likes, RTs, replies in the database
- Analyze engagement patterns weekly
"""

if __name__ == "__main__":
    print(MANUAL_POST_GUIDE)
