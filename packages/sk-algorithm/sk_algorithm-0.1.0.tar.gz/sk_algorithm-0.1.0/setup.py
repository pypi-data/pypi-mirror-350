from setuptools import setup, find_packages

setup(
    name='sk-algorithm',
    version='0.1.0',
    author='Kathermytheen sk',
    author_email='kathermytheen143143@gmail.com',
    description='A helper library for ecryption and decryption to message',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    
)