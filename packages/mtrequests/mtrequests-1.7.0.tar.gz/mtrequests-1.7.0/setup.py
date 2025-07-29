from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='mtrequests',
    version='1.7.0',
    author='dail45',
    description='threading for requests',
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    url="https://github.com/dail45/mtrequests",
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='requests threading',
    python_requires='>=3.6',
    requires=[
        "requests"
    ],
    install_requires=[
        "requests"
    ]
)
