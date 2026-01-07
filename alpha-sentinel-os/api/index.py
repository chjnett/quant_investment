from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/health')
def health_check():
    return jsonify({"status": "ok", "service": "alpha-sentinel-api"})

# This is required for Vercel to pick up the app
app = app
