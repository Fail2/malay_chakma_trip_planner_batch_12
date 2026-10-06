from app import create_app, db
from flask import jsonify

app = create_app()

@app.route('/health', methods=['GET'])
def index():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="127.0.0.1", port=5000, debug=True)