#!/usr/bin/env python3
import os
from flask import Flask, send_from_directory, safe_join, make_response
from dotenv import load_dotenv

load_dotenv()

# Flutter build/web folder ko serve karne ke liye configuration
app = Flask(__name__, static_folder='build/web', static_url_path='')

# =====================================================================
# SAFE KEYS LOAD (Aapki 12 Special Keys)
# =====================================================================
SBR_GOOGLE_KEY_1 = os.getenv("SBR_GOOGLE_KEY_1")
GEMINI_API_KEY   = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY   = os.getenv("OPENAI_API_KEY")
CLOUD_API_KEY    = os.getenv("CLOUD_API_KEY")
NVIDIA_API_KEY   = os.getenv("NVIDIA_API_KEY")
WEATHER_API_KEY  = os.getenv("WEATHER_API_KEY")
AMBER_API_KEY    = os.getenv("AMBER_API_KEY")
ELEVENLABS_KEY   = os.getenv("ELEVENLABS_KEY")
LUMA_API_KEY     = os.getenv("LUMA_API_KEY")
GROQ_API_KEY     = os.getenv("GROQ_API_KEY")
NASA_API_KEY     = os.getenv("NASA_API_KEY")
AIRNOW_API_KEY   = os.getenv("AIRNOW_API_KEY")

# API Health Check Endpoint (Cloud Run ke liye zruri hai)
@app.route('/health', methods=['GET'])
def health_check():
    return {"status": "healthy", "system": "SBRBIOFORGE CENTRAL SYSTEM ACTIVE"}, 200

# Main Route: Jo seedhe Flutter App ko load karega
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Security Rule: Path traversal attack se bachne ke liye safe_join
    file_path = safe_join(app.static_folder, path)
    
    if path and os.path.isfile(file_path):
        response = make_response(send_from_directory(app.static_folder, path))
        # Static files (JS/CSS) ko browser me cache karne ke liye headers
        response.headers['Cache-Control'] = 'public, max-age=31536000'
    else:
        response = make_response(send_from_directory(app.static_folder, 'index.html'))
        # index.html ko cache nahi karenge taaki naya update turant dikhe
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'

    # Big Developer Security Headers
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
  
