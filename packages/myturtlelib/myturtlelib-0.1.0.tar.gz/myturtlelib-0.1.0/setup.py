from setuptools import setup, find_packages

setup(
    name='myturtlelib',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple turtle-based drawing library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/myturtlelib',  # GitHub 주소 등
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Education',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.10',
)