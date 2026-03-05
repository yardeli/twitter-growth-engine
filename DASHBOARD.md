# Twitter Growth Engine Dashboard

A beautiful web UI for managing your Twitter Growth Engine.

## Quick Start

### 1. Install Dependencies

```bash
pip install flask flask-cors
```

### 2. Start the API Server

```bash
python api.py
```

You'll see:
```
 * Running on http://127.0.0.1:5000
```

### 3. Open the Dashboard

Open your browser and go to:
```
file:///path/to/twitter-growth-engine/dashboard.html
```

Or serve it with a local server:
```bash
cd twitter-growth-engine
python -m http.server 8000
# Then visit http://localhost:8000/dashboard.html
```

## Features

### 📊 Dashboard Stats
- **Total Tweets Analyzed** - Count of tweets in your database
- **Viral Tweets** - Tweets that exceeded viral threshold
- **Average Likes** - Mean engagement per tweet
- **Average Retweets** - Mean shares per tweet
- **Viral Rate** - Percentage of tweets that went viral
- **Ideas Pending** - Post ideas waiting to be published

### 💡 Ideas Tab
- View all generated post ideas
- Score: 0-100 (higher = better chance of going viral)
- **Post Button** - Mark idea as posted
- **Copy Button** - Copy to clipboard for manual posting

### 🔍 Patterns Tab
Shows analysis of what makes tweets viral:
- **Hook Types** - How viral tweets start (questions, statements, numbers, contrarian)
- **Optimal Length** - Character count for best engagement
- **Top Topics** - Keywords that appear in viral tweets
- **Engagement Ratios** - Reply/retweet patterns

### 📝 Posted Tab
See all tweets you've already posted through the system.

### 🐦 All Tweets Tab
View all tweets in your analysis database with stats:
- 🔥 VIRAL badge for high-performing tweets
- Engagement numbers (likes, retweets, replies)
- Tweet author and content

## API Endpoints

The backend API (Flask) provides these endpoints:

```
GET /api/stats              - Overall statistics
GET /api/dashboard          - Full dashboard data
GET /api/ideas              - Get unposted ideas
POST /api/ideas/generate    - Generate new ideas
GET /api/tweets             - All tweets in database
GET /api/patterns           - Viral pattern analysis
GET /api/posted             - Posted tweets history
POST /api/ideas/{id}/post   - Mark idea as posted
GET /api/health             - Health check
```

## Architecture

```
Frontend (dashboard.html/css/js)
         ↓ HTTP (fetch API)
Backend (api.py - Flask)
         ↓ SQLite queries
Database (twitter_data.db)
```

## Real-Time Updates

- Dashboard auto-refreshes every 30 seconds
- Manual refresh button available
- Stats update in real-time

## Generate Ideas

1. Click **"💡 Generate Ideas"** button
2. Enter number of ideas (1-100)
3. Click "Generate"
4. Ideas appear in the Ideas tab

## Post Ideas

Two ways to post:

### Method 1: Via Dashboard
1. View idea in "Ideas" tab
2. Click "📤 Post" button
3. Marked as posted in database

### Method 2: Manual via Playwright
```python
import asyncio
from playwright_poster import PlaywrightTwitterPoster

async def post():
    poster = PlaywrightTwitterPoster(headless=True)
    await poster.init()
    await poster.post_tweet("Your idea content", idea_id=1)
    await poster.close()

asyncio.run(post())
```

## Customization

### Change API Port
Edit `api.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Change 5000 to your port
```

Also update `dashboard.js`:
```javascript
const API_BASE = 'http://localhost:5000/api';  // Change port here
```

### Dark Mode
Edit `dashboard.css` to change colors:
```css
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* Change these colors */
}
```

### Add More Stats
Edit `api.py` to add new endpoints, then update `dashboard.js` to display them.

## Troubleshooting

**"Cannot GET /api/stats"**
- Make sure `api.py` is running
- Check port (default 5000)
- Run: `python api.py`

**"CORS error"**
- Flask CORS is enabled in `api.py`
- Make sure to run API first

**"Dashboard not loading"**
- Open developer console (F12)
- Check for JavaScript errors
- Ensure API is running

**"No data showing"**
- Add tweets first: `python main.py add-tweet ...`
- Generate ideas: `python main.py generate 10`
- Refresh dashboard: Click 🔄 button

## Performance

- Dashboard loads instantly (stats cached)
- Auto-refresh every 30 seconds (configurable)
- All data stored locally in SQLite
- No external dependencies except Flask/CORS

## Mobile Support

Dashboard is responsive and works on:
- ✅ Desktop
- ✅ Tablet
- ✅ Mobile

Just open the URL on any device!

## Advanced: Deploy Remotely

Host the API on a server:

```bash
# Install
pip install flask flask-cors gunicorn

# Run with Gunicorn (production)
gunicorn -w 4 -b 0.0.0.0:5000 api:app

# Dashboard can be served from any web server
# Access from: https://yourdomain.com/dashboard.html
```

Update API URL in dashboard.js:
```javascript
const API_BASE = 'https://yourdomain.com/api';
```

## Next Steps

1. ✅ Start API: `python api.py`
2. ✅ Open dashboard.html
3. ✅ Add training data: `python main.py add-tweet ...`
4. ✅ Generate ideas: Click 💡 button
5. ✅ Post ideas: Click 📤 button
6. ✅ Track engagement: Watch stats update

---

**Status:** 🟢 Production Ready
**Updated:** March 5, 2026
