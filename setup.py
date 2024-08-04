from setuptools import setup, find_packages

setup(
    name='simple-agents',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'chromadb>=0.5.0',
    ],
    author='Aman Raza',
    author_email='',
    description='A simple package for function calling package',
    long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    url='https://github.com/electro199/simple-agents',  # URL to the project repository
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
