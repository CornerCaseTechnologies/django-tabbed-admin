#######
Install
#######


.. code-block::  shell-session

    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py loaddata tabbed_admin_example/fixtures/test_data.json
    python manage.py loaddata tabbed_admin_example/fixtures/bands.json

Activate or deactivate grappelli or gipsy in the settings & urls
