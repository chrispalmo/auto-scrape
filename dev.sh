# export credentials
source ./set_secret_env_vars.sh

# flask configurations
export FLASK_APP="run.py"
export FLASK_DEBUG=1

flask run
