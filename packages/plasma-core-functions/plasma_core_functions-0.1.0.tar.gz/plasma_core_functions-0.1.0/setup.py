from setuptools import setup, find_packages

setup(
    name='plasma_core_functions',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pytest>=8.3.5',
        'boto3>=1.38.21',
        'pandas>=2.2.3',
        'intrinio-sdk>=6.37.0',
        'requests>=2.32.3',
        'python-dateutil>=2.9.0',
        'botocore>=1.38.21',
    ],
    description='Consolidated core functions for PLASMA projects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your_github_username/PLASMA-Core-Functions', # Replace with your repo URL
    author='Your Name', # Replace with your name
    author_email='your.email@example.com', # Replace with your email
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', # Or your chosen license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
