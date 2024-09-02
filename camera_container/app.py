from flask import Flask, jsonify, abort, send_file
import os

app = Flask(__name__)

MOCK_DIR = './mock'

def get_json_file_path(month, day=None):
    if day:
        return os.path.join(MOCK_DIR, f'month_{month}', f'day_{day}.json')
    return os.path.join(MOCK_DIR, f'month_{month}.json')

@app.route('/month/<int:month>', methods=['GET'])
def get_month_data(month):
    if month < 1 or month > 12:
        abort(404, description="Month out of range")

    file_path = get_json_file_path(month)

    if not os.path.exists(file_path):
        abort(404, description="File not found")
    
    return send_file(file_path, mimetype='application/json')

@app.route('/month/<int:month>/day/<int:day>', methods=['GET'])
def get_day_data(month, day):
    if month < 1 or month > 12 or day < 1 or day > 31:
        abort(404, description="Month or day out of range")

    file_path = get_json_file_path(month, day)

    if not os.path.exists(file_path):
        abort(404, description="File not found")

    return send_file(file_path, mimetype='application/json')

@app.errorhandler(404)
def not_found(error):
    response = jsonify({
        "error": "Not Found",
        "message": error.description
    })
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True)
