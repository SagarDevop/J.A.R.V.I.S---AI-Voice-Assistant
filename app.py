from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-jarvis', methods=['GET'])
def run_jarvis():
    try:
        # Run Jarvis in a separate subprocess so it doesn't block Flask
        subprocess.Popen(["python", "jarvis.py"])
        return jsonify({"message": "Jarvis started successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return "Jarvis API is running."

if __name__ == "__main__":
    app.run(debug=True)
