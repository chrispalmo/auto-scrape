./venv/scripts/activate.ps1
./set_secret_env_vars.ps1
$env:FLASK_APP="run.py"
$env:FLASK_DEBUG=1
flask run
