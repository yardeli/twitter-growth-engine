"""
Vercel Serverless Function for Twitter Growth Engine API
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import dependencies
try:
    from config import DB_PATH
    from collector import TwitterDataCollector
    from analyzer import PatternAnalyzer
    from generator import PostGenerator
except ImportError as e:
    print(f"Import error: {e}")
    DB_PATH = "./twitter_data.db"

# Create Flask app
app = Flask(__name__)
CORS(app)

# Initialize collectors (lazy load to avoid startup issues)
_collector = None
_analyzer = None
_generator = None

def get_collector():
    global _collector
    if _collector is None:
        try:
            _collector = TwitterDataCollector()
        except Exception as e:
            print(f"Error initializing collector: {e}")
            _collector = None
    return _collector

def get_analyzer():
    global _analyzer
    if _analyzer is None:
        try:
            _analyzer = PatternAnalyzer()
        except Exception as e:
            print(f"Error initializing analyzer: {e}")
            _analyzer = None
    return _analyzer

def get_generator():
    global _generator
    if _generator is None:
        try:
            _generator = PostGenerator()
        except Exception as e:
            print(f"Error initializing generator: {e}")
            _generator = None
    return _generator

# Routes
@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    collector = get_collector()
    if collector:
        stats = collector.get_stats()
        return jsonify(stats)
    return jsonify({"error": "Database not available"}), 500

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """Get full dashboard data"""
    collector = get_collector()
    generator = get_generator()
    
    if collector and generator:
        stats = collector.get_stats()
        ideas = generator.get_unposted_ideas(5)
        return jsonify({
            "stats": stats,
            "top_ideas": ideas,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        })
    return jsonify({"error": "Services not available"}), 500

@app.route('/api/ideas', methods=['GET'])
def get_ideas():
    """Get all unposted ideas"""
    generator = get_generator()
    if generator:
        limit = request.args.get('limit', 10, type=int)
        ideas = generator.get_unposted_ideas(limit)
        return jsonify({"ideas": ideas, "count": len(ideas)})
    return jsonify({"error": "Service not available"}), 500

@app.route('/api/ideas/generate', methods=['POST'])
def generate_ideas():
    """Generate new ideas"""
    generator = get_generator()
    if generator:
        count = request.json.get('count', 10)
        ideas = generator.generate_ideas(count)
        
        for idea in ideas:
            generator.save_idea(idea['title'], idea['content'])
        
        return jsonify({
            "status": "success",
            "generated": len(ideas),
            "ideas": ideas
        })
    return jsonify({"error": "Service not available"}), 500

@app.route('/api/tweets', methods=['GET'])
def get_tweets():
    """Get all tweets in database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT author, text, likes, retweets, replies, is_viral
            FROM tweets
            ORDER BY likes DESC
            LIMIT 50
        ''')
        
        tweets = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({"tweets": tweets, "count": len(tweets)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/patterns', methods=['GET'])
def get_patterns():
    """Get analyzed viral patterns"""
    analyzer = get_analyzer()
    if analyzer:
        patterns = analyzer.analyze_viral_patterns()
        return jsonify(patterns)
    return jsonify({"error": "Service not available"}), 500

@app.route('/api/posted', methods=['GET'])
def get_posted():
    """Get posted tweets history"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, content, score, posted
            FROM post_ideas
            WHERE posted = 1
            ORDER BY id DESC
            LIMIT 20
        ''')
        
        posts = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({"posts": posts, "count": len(posts)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ideas/<int:idea_id>/post', methods=['POST'])
def post_idea(idea_id):
    """Mark idea as posted"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE post_ideas SET posted = 1 WHERE id = ?', (idea_id,))
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "idea_id": idea_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ideas/<int:idea_id>', methods=['DELETE'])
def delete_idea(idea_id):
    """Delete an idea"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM post_ideas WHERE id = ?', (idea_id,))
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": f"Idea {idea_id} deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({"status": "healthy", "service": "Twitter Growth Engine API"})

# Export for Vercel
