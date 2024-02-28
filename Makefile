default: bin/django-admin
	./manage.py runserver

bin/django-admin:
	python3 -m venv --prompt 'softwarecommons' .
	./bin/pip install --upgrade -r requirements.txt

clean:
	rm -rf bin lib include pyvenv.cfg
