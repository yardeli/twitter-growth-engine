# Twitter Growth Engine Configuration

# Target accounts to analyze (top performers in your niches)
TARGET_ACCOUNTS = [
    "naval",           # Naval Ravikant - philosophy, startups
    "pmarca",          # Marc Andreessen - tech, VCs
    "levelsio",        # Pieter Levels - indie hacking
    "andrewchen",      # Andrew Chen - product, growth
    "paulg",           # Paul Graham - startups, tech
    "sama",            # Sam Altman - AI, Y Combinator
    "karpathy",        # Andrej Karpathy - AI
    "emollick",        # Ethan Mollick - AI, productivity
    "jacksonfall",     # Jackson Fall - AI tools
    "hardmaru",        # David Ha - AI, creativity
]

# Search terms for finding viral patterns
SEARCH_TERMS = [
    "AI automation",
    "startups founder",
    "coding productivity",
    "machine learning",
    "indie hacking",
    "side hustle",
    "tech founder",
]

# Metrics to track
METRICS = {
    "likes": "engagement",
    "retweets": "reach",
    "replies": "conversation",
    "impressions": "visibility",
}

# Post quality scoring weights
SCORING_WEIGHTS = {
    "hook_strength": 0.25,      # Strong opening line
    "specificity": 0.20,        # Specific numbers/facts
    "actionability": 0.20,      # Can reader act on it?
    "originality": 0.20,        # Unique perspective
    "clarity": 0.15,            # Easy to understand
}

# Optimal posting times (hour in PT)
OPTIMAL_TIMES = [9, 12, 17, 20]  # 9am, 12pm, 5pm, 8pm PT

# Post length recommendations
POST_LENGTH = {
    "short": (50, 100),         # Tweet hook
    "medium": (100, 200),       # Single tweet
    "long": (200, 280),         # Full tweet
    "thread": 5,                # Number of tweets in thread
}

# Engagement thresholds (to identify viral)
VIRAL_THRESHOLDS = {
    "likes_min": 100,
    "retweets_min": 50,
    "replies_min": 20,
    "reply_ratio": 0.15,        # replies / likes should be > 15%
}

# Your account info
YOUR_ACCOUNT = {
    "handle": "@eliasyarden",
    "niches": ["AI automation", "startups", "coding"],
    "target_audience": "founders, builders, AI enthusiasts",
}

# API keys
OPENAI_API_KEY = ""  # Set via environment
TWITTER_API_KEY = ""  # Optional, for API calls

# Database
DB_PATH = "./twitter_data.db"

# Content generation
GENERATION_MODEL = "gpt-4"  # or claude-3-sonnet
ANALYSIS_MODEL = "gpt-4-turbo"

# Rate limits
POSTS_PER_DAY = 2
POST_INTERVAL_HOURS = 8

# Configuration loaded
