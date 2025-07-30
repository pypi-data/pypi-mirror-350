from setuptools import setup, find_packages

setup(
    name="font_to_py",
    version="0.42",
    packages=find_packages(),
    install_requires=[
        "freetype-py>=2.13",
    ],
    entry_points={
        'console_scripts': [
            'font_to_py=font_to_py.main:main',
        ],
    },
    author="Peter Hinch",
    author_email="peter@ehinch.me.uk",
    description="Tool to convert standard font files to Python source",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/peterhinch/micropython-font-to-py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
