from setuptools import setup, find_packages

setup(
    name='daraja_gateway',
    version='0.1.0',
    description='A Python library for integrating with Safaricom Daraja API using Flask',
    author='vincent mwangi kienje',
    author_email='vynoroidtechnologies@gmail.com',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'requests',
        'python-dotenv'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7',
)
