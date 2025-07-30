from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="streamlit-hierarchy-chart",
    version="0.0.2",
    author="Winston Ssentongo",
    author_email="winstondavid96@gmail.com",
    description="Streamlit component that allows you to create Hierarchy charts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(exclude=["scripts*","example.py","test.py","test.ipynb"]),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=[
        "streamlit >= 0.63",
    ],
)
