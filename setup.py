from setuptools import setup, find_packages

setup(
    name="Dency",
    version="2.0",
    packages=find_packages(),
    install_requires=["click", "requests", "packaging"],
    entry_points={"console_scripts": ["dependency-fetcher=dependency_fetcher.cli:main"]},
    author="PRIMUS",
    author_email="alokpal2803@gmail.com",
    description="feteches and generates requirements.txt",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/11PRIMUS/Dency.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10 ",
    extras_require={"dev": ["pytest", "black"]},
    include_package_data=True,
    zip_safe=False,
)