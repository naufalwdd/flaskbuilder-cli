from setuptools import setup, find_packages

setup(
    name='flaskbuilder',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'flaskbuilder=flaskbuilder.__main__:main',
        ],
    },
    install_requires=[
        'click',
    ],
)