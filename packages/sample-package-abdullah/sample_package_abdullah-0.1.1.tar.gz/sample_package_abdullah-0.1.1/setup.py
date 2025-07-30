from setuptools import setup, find_packages


setup(
    
    name='sample_package_abdullah',
    description='A sample Python package',
    author='Abdullah Al Baki',
    author_email='abdullahalbaki009@gmail.com',
    version='0.1.1', 
    
    packages=find_packages(include=['sample_package', 'sample_package.*']),
    install_requires=[
        'requests>=2.25.1',  # Example dependency
    ]
)

# version >> (major, minor, patch)
    # major: Incremented for big changes, like breaking changes or significant new features.
    # minor: Incremented for smaller changes, like new features that are backward-compatible.
    # patch: Incremented for bug fixes or minor changes that do not affect the program.


# pip install -e .                   # for current dir editable install


# Distribution
# Create source and wheel distribution
# python setup.py sdist bdist_wheel 

# twine upload dist/*
# 
# twine upload -r testpypi dist/*
