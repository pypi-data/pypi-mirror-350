from setuptools import setup, find_packages

setup(
    name="font_to_py",
    version="0.44.1",
    packages=find_packages(),
    install_requires=[
        "freetype-py>=2.4.0",
    ],
    entry_points={
        'console_scripts': [
            'font_to_py=font_to_py.font_to_py:main',
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
