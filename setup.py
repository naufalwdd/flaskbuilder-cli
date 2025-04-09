from setuptools import setup, find_packages

setup(
    name='flaskbuilder',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['templates/**/*']  # menyertakan semua file dalam templates/
    },
    entry_points={
        'console_scripts': [
            'flaskbuilder=flaskbuilder.__main__:main',
        ],
    },
)
