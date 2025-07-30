from setuptools import setup, find_packages

setup(
    name='DS365ai',                      # Package name
    version='0.1.0',                      # Start with 0.1.0
    packages=find_packages(),            # Auto-detect packages
    description='A Python package for DS365ai',  # Short description
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='DS365ai',
    author_email='',
    url='',  # Optional
    classifiers=[                         # Optional - helps PyPI categorize
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',             # Required Python version
)
