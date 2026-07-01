from flask import Flask, request
import requests

app = Flask(__name__)

APP_ID = "1534118494925816"
APP_SECRET = "4b744e4907fef8bec9ce73c5ef32ace8"

@app.route("/")
def callback():
    code = request.args.get("code")
    if not code:
        return "No code received."
    
    res = requests.post("https://api.instagram.com/oauth/access_token", data={
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": request.base_url,
        "code": code
    })
    
    data = res.json()
    token = data.get("access_token", "ERROR: " + str(data))
    return f"<h1>Your token:</h1><p style='word-break:break-all'>{token}</p>"

if __name__ == "__main__":
    app.run()
