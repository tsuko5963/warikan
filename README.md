## install&setting
sudo apt install python3-pip python3-venv git  
git clone https://github.com/tsuko5963/warikan.git  
cd warikan  
python3 -m venv myvenv  
. myvenv/bin/activate  
python3 -m pip install -r requirements.txt  
python3 manage.py migrate  
python3 manage.py createsuperuser  
## modify mysite/settings.py  
DEBUG = False  
STATIC_ROOT = BASE_DIR / 'static'
## copy static dir
python3 manage.py collectstatic
## run
python3 manage.py runserver 0.0.0.0:8000  
