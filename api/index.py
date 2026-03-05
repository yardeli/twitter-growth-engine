"""
Vercel Serverless Function - Minimal version to avoid import issues
"""
from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Use absolute path for database
DB_PATH = "/tmp/twitter_data.db" if os.path.exists("/tmp") else "./twitter_data.db"

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "Twitter Growth Engine"})

@app.route("/api/stats", methods=["GET"])
def stats():
    try:
        if not os.path.exists(DB_PATH):
            return jsonify({
                "total_tweets": 0,
                "viral_tweets": 0,
                "avg_likes": 0,
                "avg_retweets": 0,
                "viral_percentage": 0
            })
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM tweets")
        total = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(*) FROM tweets WHERE is_viral = 1")
        viral = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT AVG(likes) FROM tweets")
        avg_likes = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT AVG(retweets) FROM tweets")
        avg_retweets = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return jsonify({
            "total_tweets": total,
            "viral_tweets": viral,
            "avg_likes": round(avg_likes, 1),
            "avg_retweets": round(avg_retweets, 1),
            "viral_percentage": round((viral / total * 100) if total > 0 else 0, 1)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/ideas", methods=["GET"])
def ideas():
    try:
        if not os.path.exists(DB_PATH):
            return jsonify({"ideas": [], "count": 0})
        
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, title, content, score FROM post_ideas WHERE posted = 0 LIMIT 20")
        ideas_list = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return jsonify({"ideas": ideas_list, "count": len(ideas_list)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    try:
        stats_response = stats()
        ideas_response = ideas()
        
        return jsonify({
            "stats": stats_response.json if hasattr(stats_response, 'json') else stats_response.get_json(),
            "top_ideas": ideas_response.json[:5] if hasattr(ideas_response, 'json') else ideas_response.get_json().get("ideas", [])[:5]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Server error"}), 500
