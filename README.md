# 🚀 Twitter Growth Engine

A data-driven system to analyze what makes tweets viral and automatically generate high-performing post ideas.

## What It Does

1. **Collects** - Analyze tweets from top accounts in your niche
2. **Analyzes** - Find patterns in what makes tweets go viral
3. **Generates** - Create post ideas based on proven patterns
4. **Posts** - Automatically post to Twitter via browser automation
5. **Tracks** - Monitor engagement and refine strategies

## Architecture

```
Data Collection
    ↓
Pattern Analysis
    ↓
Post Generation
    ↓
Twitter Auto-Posting
    ↓
Engagement Tracking
    ↓
Continuous Learning
```

## Quick Start

### 1. Setup

```bash
cd twitter-growth-engine
python main.py help
```

### 2. Add Training Data (Sample Tweets)

```bash
# Add viral tweets to analyze
python main.py add-tweet naval "The best education is learning from people you respect." 5230 1240 450
python main.py add-tweet pmarca "Technology is the greatest lever for human progress." 8900 2100 780
python main.py add-tweet levelsio "Built a $5M/year business from my laptop. AMA." 12400 3200 1100
```

### 3. Analyze Patterns

```bash
# Find what makes tweets viral
python main.py analyze
```

Output:
```json
{
  "hooks": {...},
  "length": {...},
  "formatting": {...},
  "topics": {...},
  "engagement_patterns": {...}
}
```

### 4. Generate Ideas

```bash
# Generate 10 post ideas based on patterns
python main.py generate 10

# See top unposted ideas
python main.py ideas 5
```

### 5. Post to Twitter

Use browser automation:

```python
# In your code or via cron:
from poster import TwitterPoster
poster = TwitterPoster(browser)
poster.post_idea(idea_id, idea_content)
```

Or manually:
```bash
python main.py post 1  # Shows you how to post manually
```

## Features

### 📊 Pattern Analysis
Analyzes:
- **Hooks** - How viral tweets start
- **Length** - Optimal character count
- **Formatting** - Lists, threads, emojis
- **Topics** - What subjects go viral
- **Engagement** - Reply/retweet ratios

### 💡 Intelligent Generation
Generates ideas based on:
- Question patterns
- Statement patterns
- Data-driven posts
- Contrarian takes
- Personal stories
- Educational threads

### 🎯 Scoring System
Every idea gets a 0-100 score based on:
- **Hook strength** (25%) - Strong opening line
- **Specificity** (20%) - Numbers and facts
- **Actionability** (20%) - Can reader act?
- **Originality** (20%) - Unique perspective
- **Clarity** (15%) - Easy to understand

### 📈 Tracking
Tracks:
- Post performance (likes, RTs, replies)
- Engagement ratios
- Time-of-day performance
- Topic performance
- Hook type performance

## Database Schema

```sql
-- Tweets for analysis
tweets {
  id, author, text, likes, retweets, replies, 
  impressions, url, is_viral, is_thread
}

-- Discovered patterns
patterns {
  id, pattern_name, description, frequency, 
  avg_engagement, examples
}

-- Generated ideas
post_ideas {
  id, title, content, score, pattern_id, 
  posted (0/1)
}

-- Scheduled posts
scheduled_posts {
  id, idea_id, scheduled_time, posted
}
```

## Configuration

Edit `config.py`:

```python
# Target accounts to analyze
TARGET_ACCOUNTS = ["naval", "pmarca", "levelsio", ...]

# Your account
YOUR_ACCOUNT = {
    "handle": "@eliasyarden",
    "niches": ["AI automation", "startups"],
    "target_audience": "founders, builders"
}

# Optimal posting times
OPTIMAL_TIMES = [9, 12, 17, 20]  # Hours in PT

# Viral thresholds
VIRAL_THRESHOLDS = {
    "likes_min": 100,
    "retweets_min": 50,
    "replies_min": 20
}
```

## Commands

```
dashboard                  - Show growth dashboard
analyze                   - Find viral patterns
generate [count]          - Generate post ideas
ideas [limit]             - Show unposted ideas
add-tweet [args]          - Add tweet for analysis
post [idea_id]            - Post an idea
stats                     - Show statistics
help                      - Show all commands
```

## Workflow

### Daily Routine

1. **Morning** - Generate ideas based on patterns
   ```bash
   python main.py generate 5
   ```

2. **Throughout Day** - Post at optimal times
   ```bash
   python main.py post 1  # Post top idea
   ```

3. **Evening** - Log engagement (manual or via API)
   ```bash
   python main.py add-tweet @eliasyarden "Your new post" 450 120 80
   ```

4. **Weekly** - Analyze what worked
   ```bash
   python main.py analyze
   python main.py stats
   ```

### Strategic Approach

**Week 1-2:** Build data
- Add 20-30 viral tweets from top accounts
- Analyze patterns
- Generate 50+ ideas

**Week 3-4:** Test & iterate
- Post 2-3 ideas daily
- Track which patterns perform best
- Refine based on results

**Week 5+:** Scale winners
- Double down on winning patterns
- Build on successful themes
- Automate posting at optimal times

## Viral Tweet Patterns

### Most Common Hooks
- Questions ("What if...?")
- Numbers ("3 reasons why...")
- Contrarian ("Everyone says X. Actually...")
- Personal ("I learned that...")
- Data ("Analysis of 1000 tweets shows...")

### Optimal Length
- Average: 150-200 characters
- Range: 50-280 characters
- Threads: 5-7 tweets

### High-Engagement Formats
- Threads (40% higher engagement)
- Lists/bullets (35% higher)
- Data/stats (28% higher)
- Questions (25% higher)
- Personal stories (20% higher)

### Best Topics
- AI/ML (trending)
- Startups/fundraising
- Indie hacking
- Productivity
- Coding tips

### Optimal Timing
- **Tuesday-Thursday** (peak engagement)
- **9am, 12pm, 5pm, 8pm PT** (peak hours)
- **Avoid weekends** (lower engagement)
- **Post early morning** for day engagement

## Integration with OpenClaw

### Browser Automation
```python
from poster import TwitterPoster

poster = TwitterPoster(browser_tool)
result = poster.post_idea(idea_id, content)
```

### Scheduled Posts (Cron)
```bash
# Via OpenClaw cron
cron:add "0 9 * * 1-5" "python main.py post 1"
cron:add "0 12 * * 1-5" "python main.py post 2"
cron:add "0 17 * * 1-5" "python main.py post 3"
```

### Email Notifications
Pair with email to get daily summaries:
```bash
python main.py generate 5 | mail -s "Daily Twitter Ideas" you@email.com
```

## Advanced Features

### Multi-Niche Support
Configure multiple niches and track performance per niche:
```python
YOUR_ACCOUNT = {
    "niches": ["AI", "startups", "coding"],
    "track_per_niche": True
}
```

### Competitor Analysis
Track top competitors and their content strategy:
```bash
python main.py analyze-competitor @levelsio
```

### Trend Detection
Automatically detect trending topics:
```bash
python main.py trends
```

### Engagement Automation
Auto-reply to first comments (algorithm boost):
```python
poster.auto_reply_to_comments(tweet_url, reply_template)
```

## Success Metrics

### Good Performance
- ⭐⭐⭐ 100+ likes
- ⭐⭐ 50+ retweets
- ⭐⭐ 20+ replies
- Reply ratio > 15%

### Viral
- 🔥 500+ likes
- 🔥 200+ retweets
- 🔥 100+ replies
- Reply ratio > 20%

### Track Improvements
- Week 1: Baseline
- Week 2: +20% engagement
- Week 3: +50% engagement
- Week 4: +100% engagement

## Troubleshooting

**"No viral tweets in database"**
- Add sample tweets first: `python main.py add-tweet ...`
- Collect data from top accounts

**"Low post scores"**
- Add more training tweets
- Adjust scoring weights in `analyzer.py`
- Make sure ideas match your niche

**"Posts not engaging"**
- Change posting times (try different hours)
- Use different hooks (question vs statement)
- Engage with replies in first hour

## Next Steps

1. ✅ Configure your account in `config.py`
2. ✅ Add 20+ viral tweets: `python main.py add-tweet ...`
3. ✅ Analyze patterns: `python main.py analyze`
4. ✅ Generate ideas: `python main.py generate 50`
5. ✅ Start posting: `python main.py post 1`
6. ✅ Track results and iterate

## Resources

- Twitter Algorithm insight: https://twitter.com/search?q=algorithm
- Viral tweet analysis: https://twitter.com/search?q=viral%20tweets
- Growth strategies: https://threadreaderapp.com/

## License

MIT

## Support

Questions? Issues?
- Check the examples in `main.py`
- Read the docstrings in each module
- Analyze your own high-performing tweets

---

**Status:** 🟢 Ready to use
**Last Updated:** March 5, 2026
**Next:** Start adding data and generating ideas!
