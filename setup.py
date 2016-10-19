import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='dshield',
    version='0.2',
    py_modules=['dshield'],
    include_package_data=True,
    install_requires=[
        'requests'
    ],
    license='BSD',
    description='A Pythonic interface to the Internet Storm Center / DShield API.',
    long_description=README,
    url='https://github.com/rshipp/python-dshield/',
    author='Ryan Shipp',
    author_email='python@rshipp.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Internet',
    ],
)
