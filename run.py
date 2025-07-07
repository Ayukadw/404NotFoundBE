from app import create_app
from dotenv import load_dotenv
import os

load_dotenv()

# Debug: cek folder static dan uploads
print("=== DEBUG STATIC FOLDER ===")
print("Current working directory:", os.getcwd())
print("Static folder exists:", os.path.exists("static"))
print("Uploads folder exists:", os.path.exists("static/uploads"))
if os.path.exists("static/uploads"):
    print("Files in uploads:", os.listdir("static/uploads"))
print("==========================")

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
