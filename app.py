from flask import Flask, request
import requests

app = Flask(__name__)

APP_ID = "1534118494925816"
APP_SECRET = "4b744e4907fef8bec9ce73c5ef32ace8"
FB_APP_ID = "1044559058253358"
FB_APP_SECRET = "5038a2341b2ebe7db4d6a8af463925d2"

@app.route("/")
def callback():
    code = request.args.get("code")
    if not code:
        return "No code received."

    # Step 1: Exchange code for short-lived token
    res = requests.post("https://api.instagram.com/oauth/access_token", data={
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": request.base_url,
        "code": code
    })
    data = res.json()

    if "error_type" in data:
        return f"Step 1 error: {data}"

    short_token = data.get("access_token")
    user_id = data.get("user_id")

    # Step 2: Exchange for long-lived token
    res2 = requests.get("https://graph.instagram.com/access_token", params={
        "grant_type": "ig_exchange_token",
        "client_secret": APP_SECRET,
        "access_token": short_token
    })
    data2 = res2.json()

    if "error" in data2:
        return f"Step 2 error: {data2}<br>Short token was: {short_token}"

    long_token = data2.get("access_token")
    expires = data2.get("expires_in")

    return f"""
    <h1>Success!</h1>
    <p><b>User ID:</b> {user_id}</p>
    <p><b>Long-lived token (valid for {int(expires or 0) // 86400} days):</b></p>
    <p style='word-break:break-all;background:#f0f0f0;padding:10px'>{long_token}</p>
    """

if __name__ == "__main__":
    app.run()
