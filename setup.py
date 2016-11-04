from __future__ import with_statement
import setuptools

requires = [
    "flake8 > 3.0.0",
]

setup_requires = [
    'pytest-runner',
]

tests_require = [
    'pytest',
]

def get_version(fname='flake8_webcheck.py'):
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


def get_long_description():
    descr = []
    for fname in ('README.md',):
        with open(fname) as f:
            descr.append(f.read())
    return '\n\n'.join(descr)



setuptools.setup(
    name='flake8_webcheck',
    version=get_version(),
    description="flake8 extension for web API static analysis",
    long_description=get_long_description(),
    keywords='flake8 static analysis',
    author='Joey Pereira',
    author_email='joey@pereira.io',
    url='https://github.com/xLegoz/flake8-webcheck',
    license="MIT",
    install_requires=requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    entry_points={
        'flake8.extension': [
            'H80 = flake8_webcheck:WebcheckPlugin',
        ],
    },
    classifiers=[
        "Framework :: Flake8",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
