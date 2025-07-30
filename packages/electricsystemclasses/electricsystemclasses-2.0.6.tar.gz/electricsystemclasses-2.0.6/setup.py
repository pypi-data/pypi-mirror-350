from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='electricsystemclasses',
    version='2.0.6',
    license='Server Side Public License (SSPL), Version 1.0',
    description='A collection of electric system components classes for simulation purposes',
    author='ropimen',
    author_email='rmmenichelli@gmail.com',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
