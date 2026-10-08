set -e
 
cd "$(dirname "$0")"
 
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

venv/bin/python -m pip install -r requirements.txt
venv/bin/python -m pytest ./tests/test_service.py -v
exec venv/bin/python run.py