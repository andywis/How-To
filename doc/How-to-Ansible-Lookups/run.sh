
# Load my Python3 virtual env
. ~/venv/py3/bin/activate

pycodestyle lookup_plugins/cats.py && pylint lookup_plugins/cats.py
pycodestyle lookup_plugins/dogs.py && pylint lookup_plugins/dogs.py

ansible-playbook playbook.yml
