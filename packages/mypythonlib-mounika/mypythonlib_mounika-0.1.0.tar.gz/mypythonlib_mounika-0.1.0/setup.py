from setuptools import find_packages, setup

setup(
    name='mypythonlib_mounika',  # Package name (must be unique if uploading to PyPI)
    version='0.1.0',
    packages=find_packages(include=['mypythonlib']),
    description='My first Python library',
    author='Your Name',
    install_requires=[],  # Add dependencies here if you have any
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
