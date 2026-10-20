from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB = "database.sqlite"

def query_db(query, args=(), one=False):
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query, args)
        rv = cur.fetchall()
        conn.commit()
        return (rv[0] if rv else None) if one else rv

# Initialize DB & default event
query_db("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, title TEXT, date TEXT, capacity INTEGER)")
query_db("CREATE TABLE IF NOT EXISTS registrations (id INTEGER PRIMARY KEY, event_id INTEGER, student_name TEXT, student_email TEXT, UNIQUE(event_id, student_email))")
if not query_db("SELECT * FROM events WHERE id = 1", one=True):
    query_db("INSERT INTO events VALUES (1, 'Backend Development Workshop', '2026-10-20', 50)")

@app.route('/api/v1/events/<int:id>', methods=['GET'])
def get_event(id):
    event = query_db("SELECT * FROM events WHERE id = ?", (id,), one=True)
    if not event: return jsonify({"error": "Not found"}), 404
    count = query_db("SELECT COUNT(*) as c FROM registrations WHERE event_id = ?", (id,), one=True)['c']
    return jsonify({**dict(event), "registeredCount": count, "availableSeats": event['capacity'] - count})

@app.route('/api/v1/events/<int:id>/register', methods=['POST'])
def register(id):
    data = request.json or {}
    name, email = data.get('name'), data.get('email')
    if not name or not email: return jsonify({"error": "Name & email required"}), 400
    
    event = query_db("SELECT * FROM events WHERE id = ?", (id,), one=True)
    if not event: return jsonify({"error": "Not found"}), 404
    
    count = query_db("SELECT COUNT(*) as c FROM registrations WHERE event_id = ?", (id,), one=True)['c']
    if count >= event['capacity']: return jsonify({"error": "Capacity full"}), 400

    try:
        query_db("INSERT INTO registrations (event_id, student_name, student_email) VALUES (?, ?, ?)", (id, name.strip(), email.strip().lower()))
        return jsonify({"message": "Registered successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already registered"}), 409

@app.route('/api/v1/events/<int:id>/registrations', methods=['GET'])
def get_regs(id):
    event = query_db("SELECT * FROM events WHERE id = ?", (id,), one=True)
    if not event: return jsonify({"error": "Not found"}), 404
    regs = query_db("SELECT id, student_name, student_email FROM registrations WHERE event_id = ?", (id,))
    return jsonify({**dict(event), "totalRegistered": len(regs), "registrations": [dict(r) for r in regs]})

# --- EASY BROWSER TEST ROUTE ---
@app.route('/test-browser')
def test_browser():
    try:
        query_db("INSERT INTO registrations (event_id, student_name, student_email) VALUES (?, ?, ?)", 
                 (1, "Test Student", "test@student.com"))
        return "<h1>Success!</h1><p>Test Student registered successfully! Go back and check your registrations page.</p>"
    except sqlite3.IntegrityError:
        return "<h1>Notice</h1><p>Test Student is already registered in the database!</p>"

if __name__ == '__main__':
    print("Server is running...")
    app.run(port=5000)
