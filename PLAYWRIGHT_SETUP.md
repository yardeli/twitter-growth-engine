# Playwright Twitter Automation Setup

## Why Playwright Headless?

Instead of controlling your visible computer:
- ✅ Browser runs **invisibly in background**
- ✅ You can use your computer normally
- ✅ Posts scheduled while you sleep/work
- ✅ No window stealing focus
- ✅ Fast and efficient

## Installation

### 1. Install Playwright

```bash
pip install playwright
playwright install chromium
```

### 2. Login to Twitter (One-time)

Before automating, you need to save your session:

```bash
# Create a session file (run once)
python
```

```python
import asyncio
from playwright.async_api import async_playwright

async def save_twitter_session():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Shows window
        context = await browser.new_context()
        page = await context.new_page()
        
        # Go to Twitter
        await page.goto("https://x.com/home")
        
        # Wait for YOU to login manually
        print("👤 Log in to Twitter in the browser window")
        print("⏳ Waiting 60 seconds for you to complete login...")
        await page.wait_for_timeout(60000)
        
        # Save cookies
        cookies = await context.cookies()
        
        import json
        with open("twitter_cookies.json", "w") as f:
            json.dump(cookies, f)
        
        print("✅ Cookies saved to twitter_cookies.json")
        await browser.close()

asyncio.run(save_twitter_session())
```

After running this, you'll have `twitter_cookies.json` - keep this file safe!

### 3. Use Saved Session

Now you can post without logging in each time:

```python
import asyncio
import json
from playwright.async_api import async_playwright

async def post_with_saved_session():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Invisible!
        
        # Load saved cookies
        with open("twitter_cookies.json") as f:
            cookies = json.load(f)
        
        context = await browser.new_context()
        await context.add_cookies(cookies)
        page = await context.new_page()
        
        # Now you're logged in! Post a tweet
        await page.goto("https://x.com/compose/post")
        await page.click('[data-testid="tweetTextarea_0"]')
        await page.type('[data-testid="tweetTextarea_0"]', "Hello from Playwright!")
        await page.click('[data-testid="tweetButton"]')
        
        print("✅ Tweet posted (invisibly!)")
        await browser.close()

asyncio.run(post_with_saved_session())
```

## Usage Examples

### Example 1: Post a Single Tweet

```bash
python -c "
import asyncio
from playwright_poster import PlaywrightTwitterPoster

async def main():
    poster = PlaywrightTwitterPoster(headless=True)
    await poster.init()
    await poster.post_tweet('Check out my new project!')
    await poster.close()

asyncio.run(main())
"
```

### Example 2: Post Multiple Tweets

```python
# file: post_tweets.py
import asyncio
from playwright_poster import PlaywrightTwitterPoster

async def main():
    poster = PlaywrightTwitterPoster(headless=True)
    await poster.init()
    
    tweets = [
        ("Morning insight: AI is changing everything", 1),
        ("Here's my 3-step framework for productivity", 2),
        ("Just shipped a new feature!", 3),
    ]
    
    # 5 minutes between posts
    await poster.post_multiple(tweets, delay_seconds=300)
    await poster.close()

asyncio.run(main())
```

Run it:
```bash
python post_tweets.py
```

### Example 3: Schedule Posts at Specific Times

```python
# file: schedule_posts.py
import asyncio
from playwright_poster import PlaywrightTwitterPoster

async def main():
    poster = PlaywrightTwitterPoster(headless=True)
    await poster.init()
    
    tweets = [
        ("Good morning! 🌅 Starting my day right", 1),
        ("Lunch break thoughts: productivity tips", 2),
        ("Evening reflection on today's wins", 3),
    ]
    
    times = [
        "09:00",  # 9 AM PT
        "12:00",  # 12 PM PT
        "17:00",  # 5 PM PT
    ]
    
    await poster.schedule_posts(tweets, times)
    await poster.close()

asyncio.run(main())
```

### Example 4: Auto-Engage (Reply to Comments)

```python
# file: engage.py
import asyncio
from playwright_poster import PlaywrightTwitterPoster

async def main():
    poster = PlaywrightTwitterPoster(headless=True)
    await poster.init()
    
    tweet_url = "https://x.com/@eliasyarden/status/YOUR_TWEET_ID"
    reply_template = "Thanks for engaging! Really appreciate the feedback. Check out..."
    
    replies = await poster.auto_engage(tweet_url, reply_template, max_replies=5)
    print(f"Posted {replies} replies!")
    await poster.close()

asyncio.run(main())
```

## Integration with Twitter Growth Engine

Update `main.py` to support Playwright:

```python
# Add to config.py
PLAYWRIGHT_ENABLED = True
PLAYWRIGHT_HEADLESS = True  # Invisible
TWITTER_COOKIES_FILE = "twitter_cookies.json"

# Add to main.py
from playwright_poster import PlaywrightTwitterPoster

def post_with_playwright(idea_id, content):
    """Post using Playwright (headless)"""
    async def async_post():
        poster = PlaywrightTwitterPoster(headless=True)
        await poster.init()
        result = await poster.post_tweet(content, idea_id)
        await poster.close()
        return result
    
    import asyncio
    return asyncio.run(async_post())
```

## Advanced: Run via Cron (Automated Daily Posts)

```bash
# Edit crontab
crontab -e

# Add these lines (posts daily at 9am, 12pm, 5pm PT)
0 9 * * * cd /path/to/twitter-growth-engine && python -c "from cron_poster import post_morning; post_morning()"
0 12 * * * cd /path/to/twitter-growth-engine && python -c "from cron_poster import post_noon; post_noon()"
0 17 * * * cd /path/to/twitter-growth-engine && python -c "from cron_poster import post_evening; post_evening()"
```

Create `cron_poster.py`:
```python
import asyncio
from playwright_poster import PlaywrightTwitterPoster
from generator import PostGenerator

async def post_scheduled():
    generator = PostGenerator()
    ideas = generator.get_unposted_ideas(limit=1)
    
    if not ideas:
        print("No ideas to post")
        return
    
    idea = ideas[0]
    poster = PlaywrightTwitterPoster(headless=True)
    await poster.init()
    await poster.post_tweet(idea['content'], idea['id'])
    await poster.close()
    print(f"✅ Posted: {idea['title']}")

def post_morning():
    asyncio.run(post_scheduled())

def post_noon():
    asyncio.run(post_scheduled())

def post_evening():
    asyncio.run(post_scheduled())
```

## Headless vs Visible Mode

### Headless Mode (Default)
```python
poster = PlaywrightTwitterPoster(headless=True)
```
- ✅ Browser invisible
- ✅ No window shown
- ✅ Runs in background
- ✅ Doesn't steal focus
- ✅ Best for automation

### Visible Mode (Debugging)
```python
poster = PlaywrightTwitterPoster(headless=False)
```
- 👀 Shows browser window
- 🐛 Good for debugging
- ⚠️ Steals focus from other apps
- Use only when troubleshooting

## Tips & Tricks

### Faster Posts
```python
# Disable images/wait for network
await page.goto("https://x.com/compose/post", wait_until="domcontentloaded")
```

### Faster Loading
```python
# Set viewport size (affects load time)
await poster.page.set_viewport_size({"width": 1280, "height": 720})
```

### Error Handling
```python
async def safe_post(content):
    try:
        poster = PlaywrightTwitterPoster(headless=True)
        await poster.init()
        result = await poster.post_tweet(content, idea_id=1)
        if result["status"] == "success":
            print("✅ Posted successfully")
        else:
            print(f"❌ Error: {result['message']}")
    except Exception as e:
        print(f"💥 Crash: {e}")
    finally:
        await poster.close()
```

### Session Management
```python
# Refresh session if expired
import json

async def refresh_session():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        
        # Load old cookies
        with open("twitter_cookies.json") as f:
            cookies = json.load(f)
        
        await context.add_cookies(cookies)
        await page.goto("https://x.com/home")
        
        # Save refreshed cookies
        new_cookies = await context.cookies()
        with open("twitter_cookies.json", "w") as f:
            json.dump(new_cookies, f)
        
        await browser.close()
```

## Troubleshooting

**"Element not found"**
- Twitter UI changes - update selectors
- Run in `headless=False` to see what's happening
- Wait longer: `await page.wait_for_timeout(2000)`

**"Login expired"**
- Refresh session: `asyncio.run(refresh_session())`
- Re-login manually if needed

**"Port already in use"**
- Multiple instances running
- Kill old processes: `pkill -f playwright`

**"Slow posts"**
- Network latency
- Try headless mode (faster than visible)
- Increase wait times

## Security

⚠️ **Keep `twitter_cookies.json` safe!**
- Don't commit to git (add to .gitignore)
- Don't share publicly
- Treat like a password

**Better: Use environment variables**
```python
import os
import json

# Load from env var instead of file
cookies_json = os.getenv("TWITTER_COOKIES")
cookies = json.loads(cookies_json)
```

## Next Steps

1. ✅ Install Playwright: `pip install playwright && playwright install chromium`
2. ✅ Save your session: Run the login script
3. ✅ Test posting: `python playwright_poster.py`
4. ✅ Schedule posts: Set up cron job
5. ✅ Integrate with Growth Engine: Update `main.py`

---

**Status:** Ready to automate
**Next:** Save your Twitter session, then start posting invisibly! 🤖
