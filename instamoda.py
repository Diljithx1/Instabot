# instamoda.py

import asyncio

_sessions = {}

async def login_instagram(username: str, password: str) -> bool:
    await asyncio.sleep(1)  # simulate login delay
    if username and password:
        _sessions[username] = {
            "logged_in": True,
            "followers": 100
        }
        return True
    return False

async def boost_followers(username: str) -> str:
    if username not in _sessions or not _sessions[username].get("logged_in"):
        return "❌ Not logged in."
    await asyncio.sleep(2)  # simulate API call
    _sessions[username]["followers"] += 50
    return f"✅ Boosted! {username} now has {_sessions[username]['followers']} followers."

async def check_status(username: str) -> str:
    user = _sessions.get(username)
    if not user:
        return "❌ No session found."
    return f"✅ Logged in as {username}\n📈 Followers: {user['followers']}"
