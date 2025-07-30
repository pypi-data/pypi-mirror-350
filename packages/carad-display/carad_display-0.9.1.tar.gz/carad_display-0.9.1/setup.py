import os
from setuptools import find_packages, setup
from setuptools.command.install import install


this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()


setup(
    name="carad-display",
    version="0.9.1",
    author_email='amgudym@mail.ru',
    description='A package for diplay of CARAD project, requires run on linux',
    packages=find_packages(),
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'carad-display = carad_display.main:main',
        ],
    },
    package_data={
        'carad_display': ['videos/*.mp4'],
    },
    python_requires='>=3.11',
)
