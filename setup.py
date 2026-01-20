from setuptools import setup, find_packages

setup(
    name="pc-mlra",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'Flask==2.3.3',
        'Flask-CORS==4.0.0',
        'gunicorn==21.2.0',
        'gspread==5.11.2',
        'google-auth==2.23.3',
        'google-auth-oauthlib==1.2.0',
        'oauth2client==4.1.3',
    ],
)
