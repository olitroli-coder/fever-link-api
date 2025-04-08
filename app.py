from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
SERP_API_KEY = os.environ.get("SERPAPI_KEY")

@app.route('/find-event-link', methods=['GET'])
def find_event_link():
    plan_group = request.args.get('plan_group')
    city = request.args.get('city')

    if not plan_group or not city:
        return jsonify({"error": "Missing plan_group or city"}), 400

    search_query = f"{plan_group} {city} Fever site:feverup.com"
    serp_url = "https://serpapi.com/search"

    params = {
        "q": search_query,
        "cca18112d936cf3e5a1c0c96859318441b99b4bccf17ac7031f75b8a102069a9": SERP_API_KEY,
        "engine": "google",
    }

    response = requests.get(serp_url, params=params)
    data = response.json()

    for result in data.get("organic_results", []):
        link = result.get("link")
        if link and "feverup.com" in link:
            return jsonify({
                "link": link,
                "event": f"{plan_group} – {city}",
                "status": "success"
            })

    return jsonify({"status": "not_found"}), 404

if __name__ == '__main__':
    app.run()
