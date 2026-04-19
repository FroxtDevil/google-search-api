from google_play_scraper import search, app
from flask import Flask, jsonify, request

app = Flask(__name__)

# Branding Information
DEVELOPER_INFO = {
    "developer": "Developer ROHIT",
    "channel": "https://t.me/Rohit_ob"
}

@app.route('/')
def home():
    return jsonify({
        "status": "API is running",
        "branding": DEVELOPER_INFO
    })

@app.route('/search', methods=['GET'])
def play_store_search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    try:
        results = search(query, num=10)
        formatted_results = []
        
        for app_info in results:
            formatted_results.append({
                "title": app_info.get("title"),
                "appId": app_info.get("appId"),
                "url": f"https://play.google.com/store/apps/details?id={app_info.get('appId')}",
                "icon": app_info.get("icon"),
                "developer": app_info.get("developer"),
                "price": app_info.get("price"),
                "score": app_info.get("score")
            })

        # Final Response with Search Count and Developer Credit
        return jsonify({
            "developer_contact": DEVELOPER_INFO,
            "total_results": len(formatted_results),
            "results": formatted_results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/app/<app_id>', methods=['GET'])
def get_app_details(app_id):
    try:
        app_details = app(app_id)
        detailed_info = {
            "developer_contact": DEVELOPER_INFO,
            "title": app_details.get("title"),
            "appId": app_details.get("appId"),
            "summary": app_details.get("description"),
            "reviews": app_details.get("reviews"),
            "screenshots": app_details.get("screenshots")
        }
        return jsonify(detailed_info)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch details: {str(e)}"}), 500

# Vercel ke liye handler
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(debug=True)