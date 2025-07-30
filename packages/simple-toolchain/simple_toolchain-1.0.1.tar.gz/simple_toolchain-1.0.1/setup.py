from setuptools import setup

setup(
    name='simple-toolchain',
    version='1.0.0',
    description='A simple command line utility to manage scripts and web apps',
    py_modules=['tc'],
    entry_points={
        'console_scripts': [
            'tc=tc:main',
        ],
    },
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)