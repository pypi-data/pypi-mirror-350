from setuptools import setup, find_packages

setup(
    name='neuronum',
    version='1.6.0',
    author='Neuronum Cybernetics',
    author_email='welcome@neuronum.net',
    description='Interact with the Neuronum Network to build & automate interconnected networks of soft- and hardware components',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://neuronum.net",
    project_urls={
        "GitHub": "https://github.com/neuronumcybernetics/neuronum",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests', 
        'websocket-client',
        'click',
        'questionary',
        'python-dotenv',
    ],
    entry_points={
        "console_scripts": [
            "neuronum=cli.main:cli"
        ]
    },
    python_requires='>=3.6', 
)
