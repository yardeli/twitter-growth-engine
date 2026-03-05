# Quick Start Guide

## Setup (5 minutes)

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/twitter-growth-engine.git
cd twitter-growth-engine

# Install dependencies (if any Python deps needed)
pip install -r requirements.txt  # (none needed yet)

# Verify installation
python main.py help
```

## First Run

### Step 1: Initialize Database
```bash
python main.py stats
```
This creates the SQLite database.

### Step 2: Add Training Data
Add some viral tweets to analyze:

```bash
python main.py add-tweet naval "The best education is learning from people you respect." 5230 1240 450
python main.py add-tweet pmarca "Technology is the greatest lever for human progress." 8900 2100 780
python main.py add-tweet levelsio "Built a $5M/year business from my laptop. AMA." 12400 3200 1100
python main.py add-tweet sama "The key to making good decisions is understanding the feedback loops." 6700 1890 520
python main.py add-tweet karpathy "The future of AI is much more about systems and less about single models." 9200 2450 680
```

### Step 3: Analyze Patterns
```bash
python main.py analyze
```

This shows you:
- Hook patterns (how viral tweets start)
- Optimal length
- Formatting tips
- Topic trends
- Engagement ratios

### Step 4: Generate Ideas
```bash
python main.py generate 10
```

Get 10 post ideas ranked by score (0-100).

### Step 5: See Ideas
```bash
python main.py ideas 5
```

Shows your top 5 unposted ideas.

### Step 6: Post to Twitter

Option A: Manual posting via browser
```bash
python main.py post 1  # Shows instructions
```

Option B: Automated (requires browser tool)
```python
from poster import TwitterPoster
poster = TwitterPoster(browser_tool)
poster.post_idea(1, "Your content here")
```

## Daily Workflow

**Morning:**
```bash
python main.py generate 5
python main.py ideas 1
```

**Throughout Day:**
- Post using browser automation

**Evening:**
```bash
python main.py stats
```

## Dashboard

See your overall progress:
```bash
python main.py dashboard
```

Shows:
- Tweets analyzed
- Viral rate
- Average engagement
- Top ideas

## Key Files

- `main.py` - Command-line interface
- `config.py` - Configuration (edit your account here)
- `analyzer.py` - Pattern analysis engine
- `generator.py` - Post idea generation
- `collector.py` - Data collection
- `poster.py` - Twitter posting
- `twitter_data.db` - Your database (created after first run)

## Configuration

Edit `config.py` to customize:

```python
# Your Twitter account
YOUR_ACCOUNT = {
    "handle": "@eliasyarden",
    "niches": ["AI automation", "startups"],
    "target_audience": "founders, builders"
}

# Target accounts to analyze
TARGET_ACCOUNTS = ["naval", "pmarca", "levelsio", ...]

# Optimal posting times (in PT)
OPTIMAL_TIMES = [9, 12, 17, 20]
```

## Troubleshooting

**"ModuleNotFoundError"**
- Make sure you're in the right directory
- Run: `python main.py help`

**"Database error"**
- Delete `twitter_data.db` and rerun
- It will recreate automatically

**"No ideas generated"**
- Add more training tweets first
- Run: `python main.py add-tweet ...`
- Run: `python main.py generate 10`

**"Posts aren't engaging"**
- Try different hooks (questions vs statements)
- Post at different times
- Add more training data

## Next Steps

1. ✅ Clone the repo
2. ✅ Run setup
3. ✅ Add training data
4. ✅ Generate ideas
5. ✅ Start posting!

## Tips for Success

- **Start with data** - Add 20+ viral tweets
- **Analyze thoroughly** - Understand patterns
- **Test ideas** - Post 2-3 daily
- **Track results** - Note what works
- **Iterate** - Double down on winners

---

**Status:** Ready to launch
**Time to first post:** ~15 minutes
