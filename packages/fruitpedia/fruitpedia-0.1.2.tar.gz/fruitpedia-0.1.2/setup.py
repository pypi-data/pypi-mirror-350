from setuptools import setup, find_packages

setup(
    name='fruitpedia',
    version='0.1.2',
    author='Ningappa Kanavi',
    description='A Python library with information on 100 fruits and CLI support',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fruitpedia",
    packages=find_packages(),        # automatically find packages
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'fruitpedia=fruitpedia.cli:main',
        ],
    },
    install_requires=[],             # add dependencies here if any
)
