import setuptools

with open("api_bricks_sec_api_rest_README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="api-bricks-sec-api-rest",
    version="1.0.2",
    author="Tomasz Przybysz",
    author_email="tprzybysz@coinapi.io",
    description="SDKs for API BRICKS SEC API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://docs.finfeedapi.com/sec-api/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)