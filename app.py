from flask import Flask, request, jsonify, redirect
from shortner.url_shortener import URLShortener
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Instantiate the URLShortener
shortener = URLShortener(base_url="http://localhost:5001/")

@app.route('/shorten', methods=['POST'])
def shorten():
    """Endpoint to shorten a URL."""
    data = request.json
    long_url = data.get("long_url")
    ttl = data.get("ttl", None)

    try:
        if ttl:
            ttl = int(ttl)
        short_url = shortener.shorten_url(long_url, ttl)
        return jsonify({"short_url": short_url}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/<short_url_key>', methods=['GET'])
def redirect_to_long_url(short_url_key):
    """Endpoint to handle redirection."""
    long_url = shortener.redirect(short_url_key)
    if long_url:
        return redirect(long_url, code=302)
    return jsonify({"error": "URL not found or expired"}), 404

@app.route('/stats/<short_url_key>', methods=['GET'])
def stats(short_url_key):
    """Endpoint to fetch statistics for a short URL."""
    stats = shortener.get_stats(short_url_key)
    if stats:
        return jsonify(stats), 200
    return jsonify({"error": "Stats not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, port= 5001)
