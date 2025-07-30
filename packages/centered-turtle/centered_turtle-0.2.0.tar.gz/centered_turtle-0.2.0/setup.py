from setuptools import setup, find_packages

setup(
    name='centered-turtle',
    version='0.2.0',
    author='KilRoadWay',
    author_email='kilroadway09@gmail.com',
    description='A simple turtle-based drawing library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',  # GitHub 주소 등
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Education',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.10',
)