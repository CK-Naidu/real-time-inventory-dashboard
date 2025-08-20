# app.py (Temporary "Hello World" version)
import os
from flask import Flask

app = Flask(_name_)

@app.route("/")
def hello_world():
    # Get the port number from the environment variable
    port = os.environ.get("PORT", 8080)
    return f"Hello World! The application is running successfully on port {port}."

if _name_ == "_main_":
    # Get the port number from the environment variable, default to 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
