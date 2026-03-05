// Twitter Growth Engine Dashboard
// Frontend logic for real-time analytics

const API_BASE = 'http://localhost:5000/api';

// Tab management
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;
        
        // Hide all tabs
        tabContents.forEach(tab => tab.classList.remove('active'));
        tabBtns.forEach(b => b.classList.remove('active'));
        
        // Show selected tab
        document.getElementById(tabName).classList.add('active');
        btn.classList.add('active');
        
        // Load tab content
        loadTabContent(tabName);
    });
});

// Button event listeners
document.getElementById('refreshBtn').addEventListener('click', refreshDashboard);
document.getElementById('generateBtn').addEventListener('click', showGenerateModal);
document.getElementById('confirmGenerate').addEventListener('click', generateIdeas);
document.getElementById('cancelGenerate').addEventListener('click', hideGenerateModal);

// Load data on page load
document.addEventListener('DOMContentLoaded', refreshDashboard);

// Refresh dashboard
async function refreshDashboard() {
    console.log('📊 Refreshing dashboard...');
    try {
        const response = await fetch(`${API_BASE}/dashboard`);
        const data = await response.json();
        
        // Update stats
        document.getElementById('totalTweets').textContent = data.stats.total_tweets;
        document.getElementById('viralTweets').textContent = data.stats.viral_tweets;
        document.getElementById('avgLikes').textContent = Math.round(data.stats.avg_likes);
        document.getElementById('avgRetweets').textContent = Math.round(data.stats.avg_retweets);
        document.getElementById('viralRate').textContent = data.stats.viral_percentage + '%';
        
        // Update pending ideas
        const ideasResponse = await fetch(`${API_BASE}/ideas`);
        const ideasData = await ideasResponse.json();
        document.getElementById('pendingIdeas').textContent = ideasData.count;
        
        // Update timestamp
        const now = new Date();
        document.getElementById('lastUpdate').textContent = now.toLocaleTimeString();
        
        // Load initial tab
        loadTabContent('ideas');
        
        console.log('✅ Dashboard refreshed');
    } catch (error) {
        console.error('❌ Error refreshing dashboard:', error);
        showError('Failed to load dashboard data');
    }
}

// Load tab content
async function loadTabContent(tabName) {
    try {
        switch (tabName) {
            case 'ideas':
                await loadIdeas();
                break;
            case 'patterns':
                await loadPatterns();
                break;
            case 'posted':
                await loadPosted();
                break;
            case 'tweets':
                await loadTweets();
                break;
        }
    } catch (error) {
        console.error(`Error loading ${tabName}:`, error);
        showError(`Failed to load ${tabName}`);
    }
}

// Load and display ideas
async function loadIdeas() {
    const container = document.getElementById('ideasList');
    
    try {
        const response = await fetch(`${API_BASE}/ideas?limit=20`);
        const data = await response.json();
        
        if (data.ideas.length === 0) {
            container.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: white;">No ideas yet. Generate some ideas!</p>';
            return;
        }
        
        container.innerHTML = data.ideas.map(idea => `
            <div class="idea-card">
                <div class="idea-score">Score: ${idea.score}/100</div>
                <div class="idea-title">${idea.title}</div>
                <div class="idea-content">${idea.content}</div>
                <div class="idea-actions">
                    <button class="btn-post" onclick="postIdea(${idea.id}, '${idea.content.replace(/'/g, "\\'")}')">📤 Post</button>
                    <button class="btn-copy" onclick="copyToClipboard('${idea.content.replace(/'/g, "\\'")}')">📋 Copy</button>
                    <button class="btn-delete" onclick="deleteIdea(${idea.id}, '${idea.title.replace(/'/g, "\\'")}')">🗑️ Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = '<p style="grid-column: 1/-1; color: red;">Error loading ideas</p>';
        throw error;
    }
}

// Load and display patterns
async function loadPatterns() {
    const container = document.getElementById('patternsList');
    
    try {
        const response = await fetch(`${API_BASE}/patterns`);
        const patterns = await response.json();
        
        let html = '';
        
        // Hooks
        if (patterns.hooks) {
            html += `
                <div class="pattern-box">
                    <div class="pattern-title">Hook Types</div>
                    <div class="pattern-content">
                        ${Object.entries(patterns.hooks.hook_types || {}).map(([type, count]) => `
                            <div class="pattern-item">
                                <span class="pattern-label">${type}</span>
                                <span class="pattern-value">${count}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }
        
        // Length
        if (patterns.length) {
            html += `
                <div class="pattern-box">
                    <div class="pattern-title">Optimal Length</div>
                    <div class="pattern-content">
                        <div class="pattern-item">
                            <span class="pattern-label">Average</span>
                            <span class="pattern-value">${patterns.length.avg_length} chars</span>
                        </div>
                        <div class="pattern-item">
                            <span class="pattern-label">Range</span>
                            <span class="pattern-value">${patterns.length.min_length}-${patterns.length.max_length}</span>
                        </div>
                    </div>
                </div>
            `;
        }
        
        // Topics
        if (patterns.topics) {
            html += `
                <div class="pattern-box">
                    <div class="pattern-title">Top Topics</div>
                    <div class="pattern-content">
                        ${Object.entries(patterns.topics).slice(0, 5).map(([topic, count]) => `
                            <div class="pattern-item">
                                <span class="pattern-label">#${topic}</span>
                                <span class="pattern-value">${count}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }
        
        // Engagement
        if (patterns.engagement_patterns) {
            html += `
                <div class="pattern-box">
                    <div class="pattern-title">Engagement Ratios</div>
                    <div class="pattern-content">
                        <div class="pattern-item">
                            <span class="pattern-label">Avg Retweet</span>
                            <span class="pattern-value">${patterns.engagement_patterns.avg_retweet_ratio}</span>
                        </div>
                        <div class="pattern-item">
                            <span class="pattern-label">Avg Reply</span>
                            <span class="pattern-value">${patterns.engagement_patterns.avg_reply_ratio}</span>
                        </div>
                    </div>
                </div>
            `;
        }
        
        container.innerHTML = html || '<p style="color: white;">No patterns analyzed yet</p>';
    } catch (error) {
        container.innerHTML = '<p style="color: red;">Error loading patterns</p>';
        throw error;
    }
}

// Load and display posted tweets
async function loadPosted() {
    const container = document.getElementById('postedList');
    
    try {
        const response = await fetch(`${API_BASE}/posted`);
        const data = await response.json();
        
        if (data.posts.length === 0) {
            container.innerHTML = '<p style="color: white;">No posted tweets yet</p>';
            return;
        }
        
        container.innerHTML = data.posts.map(post => `
            <div class="tweet-item">
                <div class="tweet-author">📤 Posted</div>
                <div class="tweet-text">${post.content}</div>
                <div style="color: #999; font-size: 0.9em;">
                    Score: ${post.score}/100 • ID: ${post.id}
                </div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = '<p style="color: red;">Error loading posted tweets</p>';
        throw error;
    }
}

// Load and display all tweets
async function loadTweets() {
    const container = document.getElementById('tweetsList');
    
    try {
        const response = await fetch(`${API_BASE}/tweets`);
        const data = await response.json();
        
        if (data.tweets.length === 0) {
            container.innerHTML = '<p style="color: white;">No tweets in database</p>';
            return;
        }
        
        container.innerHTML = data.tweets.map(tweet => `
            <div class="tweet-item">
                <div class="tweet-author">@${tweet.author}</div>
                <div class="tweet-text">${tweet.text}</div>
                <div class="tweet-stats">
                    <div class="tweet-stat">❤️ ${tweet.likes}</div>
                    <div class="tweet-stat">🔄 ${tweet.retweets}</div>
                    <div class="tweet-stat">💬 ${tweet.replies}</div>
                    ${tweet.is_viral ? '<span class="viral-badge">🔥 VIRAL</span>' : ''}
                </div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = '<p style="color: red;">Error loading tweets</p>';
        throw error;
    }
}

// Generate ideas
async function generateIdeas() {
    const count = parseInt(document.getElementById('ideaCount').value) || 10;
    
    try {
        console.log(`💡 Generating ${count} ideas...`);
        const response = await fetch(`${API_BASE}/ideas/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ count })
        });
        
        const data = await response.json();
        hideGenerateModal();
        showSuccess(`Generated ${data.generated} new ideas!`);
        
        // Reload ideas
        loadIdeas();
    } catch (error) {
        console.error('Error generating ideas:', error);
        showError('Failed to generate ideas');
    }
}

// Post an idea
async function postIdea(ideaId, content) {
    try {
        const response = await fetch(`${API_BASE}/ideas/${ideaId}/post`, { method: 'POST' });
        
        if (response.ok) {
            showSuccess(`Posted: "${content.substring(0, 50)}..."`);
            loadIdeas();
        } else {
            showError('Failed to mark as posted');
        }
    } catch (error) {
        console.error('Error posting idea:', error);
        showError('Failed to post idea');
    }
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showSuccess('Copied to clipboard!');
    }).catch(() => {
        showError('Failed to copy');
    });
}

// Delete an idea
async function deleteIdea(ideaId, title) {
    if (confirm(`Delete "${title}"? This cannot be undone.`)) {
        try {
            const response = await fetch(`${API_BASE}/ideas/${ideaId}`, { method: 'DELETE' });
            
            if (response.ok) {
                showSuccess(`Deleted: "${title}"`);
                loadIdeas();
            } else {
                showError('Failed to delete idea');
            }
        } catch (error) {
            console.error('Error deleting idea:', error);
            showError('Failed to delete idea');
        }
    }
}

// Modal management
function showGenerateModal() {
    document.getElementById('generateModal').classList.add('active');
}

function hideGenerateModal() {
    document.getElementById('generateModal').classList.remove('active');
}

// Notification system
function showSuccess(message) {
    console.log('✅', message);
    alert('✅ ' + message);
}

function showError(message) {
    console.error('❌', message);
    alert('❌ ' + message);
}

// Auto-refresh every 30 seconds
setInterval(refreshDashboard, 30000);

console.log('🚀 Twitter Growth Engine Dashboard loaded');
