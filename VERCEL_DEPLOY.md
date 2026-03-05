# Deploy to Vercel

## One-Click Deploy (Easiest)

1. Go to: https://vercel.com/import/project
2. Connect your GitHub: `https://github.com/yardeli/twitter-growth-engine`
3. Click **Import Project**
4. Vercel will auto-detect and configure
5. Click **Deploy**
6. Get your live URL!

## Manual Deploy with Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Navigate to project
cd twitter-growth-engine

# Deploy
vercel
```

## Environment Setup

The app requires:
- Python 3.8+
- Flask + Flask-CORS
- SQLite (included)

Vercel handles installation automatically via `requirements.txt`

## Database Note

Since Vercel is serverless:
- Database is recreated on each deployment
- For production, you'd want to use PostgreSQL or another cloud DB
- Currently uses SQLite for local storage

## Custom Domain (Optional)

After deployment:
1. Go to Vercel project settings
2. Add custom domain
3. Update DNS records

## Live Deployment Status

After deploying to Vercel, your dashboard will be at:
```
https://your-project-name.vercel.app
```

The API will be at:
```
https://your-project-name.vercel.app/api/
```

## Troubleshooting

**"Module not found"**
- Vercel needs requirements.txt ✅ (included)
- Check Python version compatibility

**"Database errors"**
- Vercel's ephemeral filesystem resets between deployments
- Use a persistent database for production (Postgres, MongoDB, etc.)

**"API 502 errors"**
- Check logs in Vercel dashboard
- May need to increase timeout (set in vercel.json)

## Production Ready

For production deployment, you'd want to:
1. Use PostgreSQL instead of SQLite
2. Add authentication
3. Set up monitoring/logging
4. Configure rate limiting
5. Add error tracking (Sentry)

But for development/demo, this works great!

---

**Deploy now:** https://vercel.com/import/project
