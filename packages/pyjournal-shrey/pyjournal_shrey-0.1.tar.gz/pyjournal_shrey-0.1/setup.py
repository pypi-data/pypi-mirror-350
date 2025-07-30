from setuptools import setup

setup(
    name='pyjournal-shrey',  
    version='0.1',
    py_modules=['journal'],  
    entry_points={
        'console_scripts': [
            'journal=journal:main',  
        ],
    },
    install_requires=[],
    author='Shrey Mehra',
    description='A simple command-line journal app with search, tagging, and markdown export.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
