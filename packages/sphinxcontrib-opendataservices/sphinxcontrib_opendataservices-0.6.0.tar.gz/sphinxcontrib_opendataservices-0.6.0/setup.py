from setuptools import setup

setup(
    name='sphinxcontrib-opendataservices',
    version='0.6.0',
    author='Open Data Services',
    author_email='code@opendataservices.coop',
    packages=['sphinxcontrib'],
    url='https://github.com/OpenDataServices/sphinxcontrib-opendataservices',
    python_requires=">=3.9.0",
    install_requires=[
        'docutils',
        'jsonpointer',
        'myst-parser>=0.18.0',
        'sphinx',
        'sphinxcontrib-opendataservices-jsonschema>=0.5.0',
    ],
    extras_require={
        'test': [
            'coveralls',
            'flake8',
            'isort',
            'lxml',
            'pytest',
            'pytest-cov',
        ],
        'docs': [
            'sphinx',
            'odsc-default-sphinx-theme',
        ]
    },
    namespace_packages=['sphinxcontrib'],
    classifiers=[
        'License :: OSI Approved :: MIT License'
    ],
)
