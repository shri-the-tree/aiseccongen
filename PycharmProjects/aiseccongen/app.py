from flask import Flask, render_template, request, jsonify, redirect, url_for
from agents.crew_setup import AISecurityCrew
from config import CONTENT_CONFIG, OUTPUT_DIR
import os
import threading
from datetime import datetime

app = Flask(__name__)

# Global variable to track generation status
generation_status = {
    "in_progress": False,
    "current_topic": "",
    "result": None,
    "error": None
}


@app.route('/')
def index():
    """Main page with topic selection and generation form."""
    return render_template('index.html', topics=CONTENT_CONFIG['topics'])


@app.route('/generate', methods=['POST'])
def generate_content():
    """Start content generation process."""
    global generation_status

    if generation_status["in_progress"]:
        return jsonify({"error": "Generation already in progress"}), 400

    topic = request.form.get('topic')
    custom_topic = request.form.get('custom_topic')
    word_count = int(request.form.get('word_count', 1000))

    # Use custom topic if provided
    final_topic = custom_topic if custom_topic else topic

    if not final_topic:
        return jsonify({"error": "Please select or enter a topic"}), 400

    # Reset status
    generation_status.update({
        "in_progress": True,
        "current_topic": final_topic,
        "result": None,
        "error": None
    })

    # Start generation in background thread
    thread = threading.Thread(
        target=background_generate,
        args=(final_topic, word_count)
    )
    thread.daemon = True
    thread.start()

    return redirect(url_for('status'))


def background_generate(topic, word_count):
    """Background function to generate content."""
    global generation_status

    try:
        crew = AISecurityCrew()
        result = crew.generate_content(topic, word_count)
        generation_status["result"] = result
    except Exception as e:
        generation_status["error"] = str(e)
    finally:
        generation_status["in_progress"] = False


@app.route('/status')
def status():
    """Show generation status and results."""
    return render_template('status.html', status=generation_status)


@app.route('/api/status')
def api_status():
    """API endpoint to check generation status."""
    return jsonify(generation_status)


@app.route('/view/<filename>')
def view_content(filename):
    """View generated content."""
    try:
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return render_template('content.html', content=content, filename=filename)
    except FileNotFoundError:
        return "Content not found", 404


@app.route('/api/generated')
def list_generated():
    """List all generated content files."""
    try:
        files = []
        if os.path.exists(OUTPUT_DIR):
            for filename in os.listdir(OUTPUT_DIR):
                if filename.endswith('.md'):
                    filepath = os.path.join(OUTPUT_DIR, filename)
                    stat = os.stat(filepath)
                    files.append({
                        "filename": filename,
                        "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M"),
                        "size": stat.st_size
                    })
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)