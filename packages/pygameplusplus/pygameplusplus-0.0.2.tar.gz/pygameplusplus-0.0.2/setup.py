from setuptools import setup, find_packages

setup(
    name="pygameplusplus",
    version="0.0.2",
    author="Annes",
    description="Better pygame",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pygameplusplus",
    packages=find_packages(),
    install_requires=["pygame", "cairosvg"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
