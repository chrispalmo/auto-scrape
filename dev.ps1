./venv/scripts/activate.ps1
$env:FLASK_APP="run.py"
$env:FLASK_DEBUG=1
flask run
