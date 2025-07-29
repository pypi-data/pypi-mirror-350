import setuptools

with open("README.md", "r", encoding="UTF-8") as f:
    description = f.read()

with open("LICENSE", "r") as f:
    license = f.read()

setuptools.setup(
    name="xplainable-client",
    version="1.2.6.post1",
    author="xplainable pty ltd",
    author_email="contact@xplainable.io",
    packages=["xplainable_client"],
    description="The client for persisting and deploying models to Xplainable cloud.",
    long_description=description,
    long_description_content_type="text/markdown",
    license=license,
    python_requires='>=3.10',
    install_requires=[
        "ipywidgets",
        "numpy>=1.26",
        "pandas>=1.5.2",
        "pyperclip",
        "Requests",
        "scikit_learn",
        "setuptools",
        "urllib3",
        "xplainable>=1.2.4"
    ]
)
