from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="bncode",
    version="0.0.1",
    author="boon4681",
    author_email="boon4681dev@gmail.com",
    description="BNcode",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/boon4681/bncode.git",
    license="MIT",
    packages=find_packages(where="bncode"),
    package_dir={"": "bncode"},
    install_requires=[
        'numpy','opencv-python'
    ],
    tests_require=[
        'coverage', 'wheel', 'pytest', 'requests_mock'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)