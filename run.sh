# Activate the virtual environment
source venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Set environment variables for Flask
export FLASK_APP=run.py
export FLASK_ENV=development

# Start the Flask application
python -m flask run --port 5000