from setuptools import setup, find_packages

setup(
    name='global_service',
    version='0.1.0',
    description='Global logging and service utilities for Python projects',
    author='Rohit Jagatp',
    author_email='rohit.jagatp@lighthouseindia.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'python-dotenv',
        'cx_Oracle',  
    ],
    python_requires='>=3.6',
    url='https://github.com/yourusername/global_service',  # optional
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)