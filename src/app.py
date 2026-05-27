import os
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__, static_folder='.', static_url_path='')

# Manual CORS header addition to support all origins (including file:// protocol)
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    return response

@app.route('/')
def index():
    return app.send_static_file('index.html')

# Support serving static files under /src/ prefix (e.g. /src/index.html)
@app.route('/src/<path:filename>')
def serve_src(filename):
    return app.send_static_file(filename)

@app.route('/search')
def search():
    query = request.args.get('name', '').strip()
    if not query:
        return jsonify([])

    # Locate database
    db_path = "/home/nemo/find-lec/LecProfile/lecturer.db"
    if not os.path.exists(db_path):
        db_path = "lecturer.db"

    try:
        db = sqlite3.connect(db_path)
        csr = db.cursor()
        
        # Search query matching case-insensitively using SQLite LIKE
        csr.execute("SELECT name, phone_number FROM Lecturers WHERE name LIKE ?", (f"%{query}%",))
        results = csr.fetchall()
        db.close()

        # Format rows cleanly
        data = [{"name": row[0], "phone": row[1] if row[1] else ""} for row in results]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
