"""
AI Chat Users in Python
----------------------

Links
`````

* `development version <https://bitbucket.org/entinco/eic-ai-prototypes/src/main/lib-aichatusers-python>`

"""

from setuptools import find_packages
from setuptools import setup

try:
    readme = open('readme.md').read()
except:
    readme = __doc__

setup(
    name='eic_aichat_users',
    version='1.0.39',
    url='https://bitbucket.org/entinco/eic-ai-prototypes/src/master/lib-aichatusers-python',
    license='Commercial',
    author='Enterprise Innovation Consulting LLC',
    author_email='seroukhov@entinco.com',
    description='AI Chat Users in Python',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['config', 'data', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'pip-services4-commons>=0.0.0',
        'pip-services4-components>=0.0.0',
        'pip-services4-config>=0.0.0',
        'pip-services4-data>=0.0.0',
        'pip-services4-http>=0.0.0',
        'pip-services4-mongodb>=0.0.0',
        'pip-services4-persistence>=0.0.0',
        'pip-services4-prometheus>=0.0.0',
        'pip-services4-rpc>=0.0.0',
        'pip-services4-swagger>=0.0.0'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
