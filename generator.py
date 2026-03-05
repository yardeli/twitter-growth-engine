"""
Post Idea Generator
Creates tweet ideas based on viral patterns and your niche
"""

import json
import sqlite3
from config import DB_PATH, YOUR_ACCOUNT, GENERATION_MODEL
from analyzer import PatternAnalyzer

class PostGenerator:
    def __init__(self):
        self.db_path = DB_PATH
        self.analyzer = PatternAnalyzer()
        self.account_info = YOUR_ACCOUNT
    
    def generate_ideas(self, count=10):
        """Generate post ideas based on patterns"""
        patterns = self.analyzer.analyze_viral_patterns()
        
        if "status" in patterns and patterns["status"] == "No viral tweets in database yet":
            return self._generate_template_ideas(count)
        
        ideas = []
        
        # Generate based on common topics
        topics = patterns.get("topics", {})
        for i in range(count // 2):
            idea = self._generate_idea_from_topic(list(topics.keys())[i % len(topics)])
            ideas.append(idea)
        
        # Generate based on hooks
        hooks = patterns.get("hooks", {}).get("hook_types", {})
        for hook_type in list(hooks.keys())[:count // 2]:
            idea = self._generate_idea_from_hook_type(hook_type)
            ideas.append(idea)
        
        # Score all ideas
        scored_ideas = [
            {
                **idea,
                "score": self.analyzer.score_post_idea(idea["content"])
            }
            for idea in ideas
        ]
        
        # Sort by score
        scored_ideas.sort(key=lambda x: x["score"], reverse=True)
        
        return scored_ideas[:count]
    
    def _generate_template_ideas(self, count):
        """Generate template ideas for your niches"""
        templates = [
            {
                "title": "AI Tool Discovery",
                "content": "Just discovered an AI tool that cuts my [TASK] time in half. It's called [TOOL NAME] and here's why it's a game-changer: [WHY]",
                "pattern": "discovery",
            },
            {
                "title": "Founder Insight",
                "content": "Most founders don't realize this about [TOPIC]: [INSIGHT]. I learned this the hard way. Here's what changed everything: [STORY]",
                "pattern": "insight",
            },
            {
                "title": "Quick Hack",
                "content": "3-minute hack that saves hours: [HACK]. Try it and tell me if it works for you.",
                "pattern": "hack",
            },
            {
                "title": "Contrarian Take",
                "content": "Everyone says [COMMON BELIEF]. Wrong. Here's what actually works: [YOUR TAKE]",
                "pattern": "contrarian",
            },
            {
                "title": "Learning Share",
                "content": "Spent 10 hours learning [SKILL]. Here are the 5 biggest mistakes I made and how to avoid them:",
                "pattern": "educational",
            },
            {
                "title": "Question Thread",
                "content": "If you're building in AI/startups, what's the one thing nobody tells you? I'll go first: [ANSWER]",
                "pattern": "question",
            },
            {
                "title": "Data Insight",
                "content": "Analyzed [DATA_SET]. Found something interesting: [FINDING]. This means: [IMPLICATION]",
                "pattern": "data",
            },
            {
                "title": "Personal Win",
                "content": "Hit [MILESTONE] this month. Here's the exact system that got me here: [SYSTEM]",
                "pattern": "milestone",
            },
            {
                "title": "Hot Take",
                "content": "The best investment in 2026 won't be [COMMON]. It'll be [YOUR_TAKE]. Here's why:",
                "pattern": "prediction",
            },
            {
                "title": "Practical Advice",
                "content": "If I were starting [PROJECT] today, I'd do these 3 things first: 1) [THING1] 2) [THING2] 3) [THING3]",
                "pattern": "advice",
            },
        ]
        
        scored_templates = [
            {
                **template,
                "score": 65 + (i * 2),  # Bias higher templates slightly
                "needs_personalization": True
            }
            for i, template in enumerate(templates[:count])
        ]
        
        return scored_templates
    
    def _generate_idea_from_topic(self, topic):
        """Generate post from a topic"""
        return {
            "title": f"{topic.capitalize()} Thread",
            "content": f"Thread about {topic}:\n\n1/ The best insight about {topic} is that... [YOUR INSIGHT]",
            "pattern": f"topic_{topic}",
            "topic": topic,
        }
    
    def _generate_idea_from_hook_type(self, hook_type):
        """Generate post from hook type"""
        hook_templates = {
            "question": "What's the #1 misconception about building in AI?",
            "statement": "The future of work is AI automation. Here's what that means for you:",
            "number": "3 tools that changed how I code: [TOOL1], [TOOL2], [TOOL3]",
            "contrarian": "Everyone says learn X first. Wrong. You should learn Y instead because:",
        }
        
        hook = hook_templates.get(hook_type, f"The {hook_type} everyone needs to know:")
        
        return {
            "title": f"{hook_type.capitalize()} Hook",
            "content": f"{hook}\n\n[EXPAND ON YOUR POINT HERE]",
            "pattern": f"hook_{hook_type}",
            "hook_type": hook_type,
        }
    
    def save_idea(self, title, content, pattern_id=None):
        """Save post idea to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        score = self.analyzer.score_post_idea(content)
        
        cursor.execute('''
            INSERT INTO post_ideas 
            (title, content, score, pattern_id, based_on)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, content, score, pattern_id, pattern_id or "template"))
        
        conn.commit()
        idea_id = cursor.lastrowid
        conn.close()
        
        return idea_id
    
    def get_unposted_ideas(self, limit=5):
        """Get top unposted ideas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, content, score, based_on
            FROM post_ideas
            WHERE posted = 0
            ORDER BY score DESC
            LIMIT ?
        ''', (limit,))
        
        ideas = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": i[0],
                "title": i[1],
                "content": i[2],
                "score": i[3],
                "pattern": i[4],
            }
            for i in ideas
        ]

# Example usage
if __name__ == "__main__":
    generator = PostGenerator()
    
    # Generate ideas
    ideas = generator.generate_ideas(5)
    
    print("💡 Generated Post Ideas:")
    for i, idea in enumerate(ideas, 1):
        print(f"\n{i}. {idea['title']} (Score: {idea['score']}/100)")
        print(f"   Content: {idea['content'][:100]}...")
