
from setuptools import setup
from gepics import get_version


with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().splitlines()

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()


setup(
    name='gepics',
    version=get_version(),
    url="https://github.com/michel4j/gepics",
    license='MIT',
    author='Michel Fodje',
    author_email='michel4j@gmail.com',
    description='Python GObject Wrapper for EPICS Process Variables',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='epics gobject development',
    py_modules=['gepics'],
    install_requires=requirements,
    classifiers=[
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
