from setuptools import setup, find_packages
setup(
    name='tick_track',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'sanic==20.12.6',
        'pytz==2019.3',
        'peewee==3.13.1',
        'python-dotenv'
    ],

    author='Gabriel Menezes',
    description='This is an simple app to show you were did your time went',
    keywords='time track tracking activities task',
    python_requires='>=3.6.8',
)
