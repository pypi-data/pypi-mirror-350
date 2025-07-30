from pathlib import Path
import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="streamlit-fill-in-blanks",
    version="0.1.0",
    author="Felix Hammer",
    author_email="fhammer@uos.de",
    description="Streamlit component for fill-in-the-blanks exercises",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ffhammer/streamlit-fill-in-blanks",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.8",
    install_requires=[
        "streamlit >= 1.0",
    ],
)
