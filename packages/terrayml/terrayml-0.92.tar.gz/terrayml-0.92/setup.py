from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name="terrayml",
    version="0.92",
    author="Warren Ezra Bruce Jaudian",
    author_email="webpjaudian@gmail.com",
    packages=find_packages(),
    description="This is Terrayml.",
    long_description=description,
    long_description_content_type="text/markdown",
    license="MIT",
    py_modules=["terrayml"],
    install_requires=["awscli", "Click", "PyYAML", "python-dotenv"],
    entry_points="""
        [console_scripts]
        terrayml=terrayml.terrayml:cli
    """,
    package_data={
        "terrayml": [
            "terrayml/*",
            "file_templates/*",
            "mappings/*",
            "modules/*/*",
            "object_templates/*",
            ".env.example",
            "py.typed",
        ],
    },
)
