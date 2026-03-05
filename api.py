"""
Twitter Growth Engine API
Simple Flask API to serve dashboard data
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import json
from config import DB_PATH
from collector import TwitterDataCollector
from analyzer import PatternAnalyzer
from generator import PostGenerator

app = Flask(__name__)
CORS(app)

collector = TwitterDataCollector()
analyzer = PatternAnalyzer()
generator = PostGenerator()

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    stats = collector.get_stats()
    return jsonify(stats)

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """Get full dashboard data"""
    stats = collector.get_stats()
    ideas = generator.get_unposted_ideas(5)
    
    return jsonify({
        "stats": stats,
        "top_ideas": ideas,
        "timestamp": __import__('datetime').datetime.now().isoformat()
    })

@app.route('/api/ideas', methods=['GET'])
def get_ideas():
    """Get all unposted ideas"""
    limit = request.args.get('limit', 10, type=int)
    ideas = generator.get_unposted_ideas(limit)
    return jsonify({"ideas": ideas, "count": len(ideas)})

@app.route('/api/ideas/generate', methods=['POST'])
def generate_ideas():
    """Generate new ideas"""
    count = request.json.get('count', 10)
    ideas = generator.generate_ideas(count)
    
    # Save all ideas
    for idea in ideas:
        generator.save_idea(idea['title'], idea['content'])
    
    return jsonify({
        "status": "success",
        "generated": len(ideas),
        "ideas": ideas
    })

@app.route('/api/tweets', methods=['GET'])
def get_tweets():
    """Get all tweets in database"""
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

@app.route('/api/patterns', methods=['GET'])
def get_patterns():
    """Get analyzed viral patterns"""
    patterns = analyzer.analyze_viral_patterns()
    return jsonify(patterns)

@app.route('/api/posted', methods=['GET'])
def get_posted():
    """Get posted tweets history"""
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

@app.route('/api/ideas/<int:idea_id>/post', methods=['POST'])
def post_idea(idea_id):
    """Mark idea as posted"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('UPDATE post_ideas SET posted = 1 WHERE id = ?', (idea_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "idea_id": idea_id})

@app.route('/api/ideas/<int:idea_id>/score', methods=['GET'])
def score_idea(idea_id):
    """Get score for an idea"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT score FROM post_ideas WHERE id = ?', (idea_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return jsonify({"score": result[0]})
    else:
        return jsonify({"error": "Idea not found"}), 404

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({"status": "healthy", "service": "Twitter Growth Engine API"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
