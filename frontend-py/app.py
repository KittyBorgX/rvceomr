"""
RVCE OMR Grading System - Python Flask Frontend
1:1 port of the Next.js TypeScript frontend
"""

import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, jsonify, request, Response, send_file
import requests
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

# Configuration
API_BASE_URL = os.environ.get("API_URL", "http://localhost:8000/api")


# API Client Class
class ApiClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()

    def upload_batch(self, files, batch_name=None):
        """Upload batch of OMR images"""
        url = f"{self.base_url}/omr/upload"

        files_data = []
        for file in files:
            files_data.append(
                ("files", (file.filename, file.stream, file.content_type))
            )

        data = {}
        if batch_name:
            data["batchName"] = batch_name

        response = self.session.post(url, files=files_data, data=data)
        response.raise_for_status()
        return response.json()

    def upload_excel(self, files, batch_name=None):
        """Upload Excel answer key"""
        url = f"{self.base_url}/omr/uploadexcel"

        files_data = []
        for file in files:
            files_data.append(
                ("files", (file.filename, file.stream, file.content_type))
            )

        data = {}
        if batch_name:
            data["batchName"] = batch_name

        response = self.session.post(url, files=files_data, data=data)
        response.raise_for_status()
        return response.json()

    def get_batch_status(self, batch_id):
        """Get batch processing status"""
        url = f"{self.base_url}/omr/status/{batch_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_batch_results(self, batch_id):
        """Get batch results"""
        url = f"{self.base_url}/omr/results/{batch_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def download_results(self, batch_id):
        """Download results as CSV"""
        url = f"{self.base_url}/omr/download/{batch_id}"
        response = self.session.get(url, stream=True)
        response.raise_for_status()
        return response.content

    def download_all_results(self):
        """Download all results as master CSV"""
        url = f"{self.base_url}/omr/download-all"
        response = self.session.get(url, stream=True)
        response.raise_for_status()
        return response.content

    def get_dashboard_stats(self):
        """Get dashboard statistics"""
        url = f"{self.base_url}/omr/dashboard"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()


# Initialize API client
api_client = ApiClient()


# Template context processors
@app.context_processor
def inject_globals():
    return {"current_year": datetime.now().year, "app_name": "RVCE OMR Grading System"}


# Routes
@app.route("/")
def index():
    """Dashboard page"""
    return render_template("index.html")


@app.route("/upload")
def upload_page():
    """Upload page"""
    return render_template("upload.html")


@app.route("/upload/answers")
def upload_answers_page():
    """Upload answers page - redirects to upload with tab"""
    return render_template("upload.html", initial_tab="excel")


@app.route("/processing/<batch_id>")
def processing_page(batch_id):
    """Processing status page"""
    return render_template("processing.html", batch_id=batch_id)


@app.route("/results/<batch_id>")
def results_page(batch_id):
    """Results page"""
    return render_template("results.html", batch_id=batch_id)


# API Routes (proxies to backend)
@app.route("/api/stats/dashboard")
def api_dashboard_stats():
    """Get dashboard stats"""
    try:
        stats = api_client.get_dashboard_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/omr/upload", methods=["POST"])
def api_upload_batch():
    """Upload OMR batch"""
    try:
        files = request.files.getlist("files")
        batch_name = request.form.get("batchName")

        if not files:
            return jsonify({"error": "No files provided"}), 400

        result = api_client.upload_batch(files, batch_name)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/answers/upload", methods=["POST"])
def api_upload_excel():
    """Upload Excel answer key"""
    try:
        files = request.files.getlist("files")
        batch_name = request.form.get("batchName")

        if not files:
            return jsonify({"error": "No files provided"}), 400

        result = api_client.upload_excel(files, batch_name)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/omr/status/<batch_id>")
def api_batch_status(batch_id):
    """Get batch status"""
    try:
        status = api_client.get_batch_status(batch_id)
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/omr/results/<batch_id>")
def api_batch_results(batch_id):
    """Get batch results"""
    try:
        results = api_client.get_batch_results(batch_id)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/omr/results/<batch_id>/download")
def api_download_results(batch_id):
    """Download results CSV"""
    try:
        content = api_client.download_results(batch_id)
        return Response(
            content,
            mimetype="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=Results_{batch_id}.csv"
            },
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/omr/download-all")
def api_download_all_results():
    """Download all results as master CSV"""
    try:
        content = api_client.download_all_results()
        return Response(
            content,
            mimetype="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=Results_All_Batches.csv"
            },
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template(
        "error.html", error_code=404, error_message="Page not found"
    ), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template(
        "error.html", error_code=500, error_message="Internal server error"
    ), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
