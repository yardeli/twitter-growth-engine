#!/usr/bin/env python3
"""
Twitter Growth Engine - Main Script
Orchestrates data collection, analysis, generation, and posting
"""

import sys
import json
from datetime import datetime
from collector import TwitterDataCollector
from analyzer import PatternAnalyzer
from generator import PostGenerator
from poster import TwitterPoster

class TwitterGrowthEngine:
    def __init__(self):
        self.collector = TwitterDataCollector()
        self.analyzer = PatternAnalyzer()
        self.generator = PostGenerator()
        self.poster = TwitterPoster()
    
    def dashboard(self):
        """Display growth dashboard"""
        stats = self.collector.get_stats()
        
        print("\n" + "="*60)
        print("🚀 TWITTER GROWTH ENGINE - DASHBOARD")
        print("="*60)
        print(f"\n📊 COLLECTED DATA:")
        print(f"   Total tweets analyzed: {stats['total_tweets']}")
        print(f"   Viral tweets found: {stats['viral_tweets']}")
        print(f"   Viral rate: {stats['viral_percentage']}%")
        print(f"\n📈 ENGAGEMENT METRICS:")
        print(f"   Average likes: {stats['avg_likes']}")
        print(f"   Average retweets: {stats['avg_retweets']}")
        print(f"\n💡 IDEA GENERATION:")
        
        ideas = self.generator.get_unposted_ideas(3)
        for i, idea in enumerate(ideas, 1):
            print(f"\n   {i}. {idea['title']} (Score: {idea['score']}/100)")
            print(f"      {idea['content'][:80]}...")
        
        print("\n" + "="*60)
    
    def analyze(self):
        """Analyze viral patterns"""
        print("\n🔍 Analyzing viral patterns...")
        patterns = self.analyzer.analyze_viral_patterns()
        
        if "status" in patterns:
            print(f"⚠️  {patterns['status']}")
            print("   Add some tweets to database first with: python main.py add-tweet")
            return
        
        print("\n📊 VIRAL PATTERN ANALYSIS:")
        print(json.dumps(patterns, indent=2))
        
        # Save report
        with open("analysis_report.json", "w") as f:
            json.dump(patterns, f, indent=2)
        print("\n✅ Report saved to analysis_report.json")
    
    def generate(self, count=10):
        """Generate post ideas"""
        print(f"\n💡 Generating {count} post ideas...")
        ideas = self.generator.generate_ideas(count)
        
        print("\n🎯 POST IDEAS (Ranked by Score):")
        for i, idea in enumerate(ideas, 1):
            print(f"\n{i}. {idea['title']}")
            print(f"   Score: {idea['score']}/100")
            print(f"   Content: {idea['content'][:100]}...")
            
            # Save to database
            self.generator.save_idea(idea['title'], idea['content'])
        
        print(f"\n✅ Saved {count} ideas to database")
    
    def add_tweet(self, author, text, likes, retweets, replies):
        """Add a tweet to analysis database"""
        tweet_id = self.collector.log_tweet(author, text, likes, retweets, replies)
        print(f"✅ Tweet added: {tweet_id}")
    
    def ideas(self, limit=5):
        """Show top unposted ideas"""
        ideas = self.generator.get_unposted_ideas(limit)
        
        print(f"\n💡 TOP {limit} UNPOSTED IDEAS:")
        for i, idea in enumerate(ideas, 1):
            print(f"\n{i}. {idea['title']} (Score: {idea['score']}/100)")
            print(f"   Pattern: {idea['pattern']}")
            print(f"   Content: {idea['content'][:120]}...")
    
    def post(self, idea_id):
        """Post an idea (requires browser automation)"""
        ideas = self.generator.get_unposted_ideas(100)
        idea = next((i for i in ideas if i['id'] == idea_id), None)
        
        if not idea:
            print(f"❌ Idea {idea_id} not found")
            return
        
        print(f"\n📝 Posting: {idea['title']}")
        print(f"   Content: {idea['content']}")
        print(f"\n⚠️  To post, use browser automation:")
        print(f"   browser.open('https://x.com/compose/post')")
        print(f"   browser.type(text='{idea['content']}')")
        print(f"   browser.click()  # Post button")
    
    def stats(self):
        """Show statistics"""
        stats = self.collector.get_stats()
        patterns = self.analyzer.analyze_viral_patterns()
        
        print("\n📊 TWITTER GROWTH STATISTICS:")
        print(f"\nData Collection:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        if "status" not in patterns:
            print(f"\nViral Patterns:")
            if "hooks" in patterns:
                print(f"  Most common hooks: {len(patterns['hooks']['most_common'])}")
            if "topics" in patterns:
                print(f"  Top topics: {list(patterns['topics'].keys())[:5]}")

def show_help():
    """Show command help"""
    help_text = """
🚀 TWITTER GROWTH ENGINE - Commands

Usage: python main.py [command] [args]

Commands:
  dashboard              - Show growth dashboard
  analyze               - Analyze viral patterns
  generate [count]      - Generate post ideas (default: 10)
  ideas [limit]         - Show top unposted ideas (default: 5)
  add-tweet AUTHOR TEXT LIKES RTS REPLIES
                        - Add tweet to database for analysis
  post [idea_id]        - Post an idea (requires browser)
  stats                 - Show statistics
  help                  - Show this help

Examples:
  python main.py dashboard
  python main.py analyze
  python main.py generate 15
  python main.py add-tweet naval "The best advice is free" 5230 1240 450
  python main.py ideas 10

Next Steps:
  1. Add tweets: python main.py add-tweet [author] [text] [likes] [rts] [replies]
  2. Analyze: python main.py analyze
  3. Generate ideas: python main.py generate
  4. Post: Use browser automation or manual Twitter posting
  5. Track engagement and refine patterns
"""
    print(help_text)

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    engine = TwitterGrowthEngine()
    command = sys.argv[1].lower()
    
    try:
        if command == "dashboard":
            engine.dashboard()
        
        elif command == "analyze":
            engine.analyze()
        
        elif command == "generate":
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            engine.generate(count)
        
        elif command == "ideas":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            engine.ideas(limit)
        
        elif command == "add-tweet":
            if len(sys.argv) < 7:
                print("Usage: python main.py add-tweet AUTHOR TEXT LIKES RTS REPLIES")
                return
            author = sys.argv[2]
            text = sys.argv[3]
            likes = int(sys.argv[4])
            rts = int(sys.argv[5])
            replies = int(sys.argv[6])
            engine.add_tweet(author, text, likes, rts, replies)
        
        elif command == "post":
            if len(sys.argv) < 3:
                print("Usage: python main.py post [idea_id]")
                return
            idea_id = int(sys.argv[2])
            engine.post(idea_id)
        
        elif command == "stats":
            engine.stats()
        
        elif command == "help":
            show_help()
        
        else:
            print(f"Unknown command: {command}")
            show_help()
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
