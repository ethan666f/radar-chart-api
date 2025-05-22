from flask import Flask, request, send_file, jsonify
import matplotlib.pyplot as plt
import numpy as np
import io
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Radar Chart API is running!"

@app.route('/radar', methods=['POST'])
def radar_chart():
    data = request.json

    raw_scores = data.get("scores")
    labels = data.get("labels")

    # Handle scores from string or list
    if isinstance(raw_scores, str):
        try:
            scores = [int(x.strip()) for x in raw_scores.split(',')]
        except ValueError:
            return jsonify({"error": "Scores must be integers."}), 400
    elif isinstance(raw_scores, list):
        scores = raw_scores
    else:
        return jsonify({"error": "Invalid scores format."}), 400

    if len(scores) != 8:
        return jsonify({"error": f"Exactly 8 scores are required, received {len(scores)}."}), 400

    if not labels or len(labels) != 8:
        labels = [f"Q{i+1}" for i in range(8)]

    # Radar chart math
    angles = np.linspace(0, 2 * np.pi, len(scores), endpoint=False).tolist()
    scores += scores[:1]  # Close the loop
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, scores, color='blue', linewidth=2)
    ax.fill(angles, scores, color='blue', alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title("Questionnaire Radar Chart", size=14, y=1.1)
    plt.tight_layout()

    # Save to memory buffer
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    plt.close()
    img_bytes.seek(0)

    return send_file(img_bytes, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

