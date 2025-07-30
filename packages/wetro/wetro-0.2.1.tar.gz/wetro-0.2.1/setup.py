from setuptools import setup, find_packages

setup(
    name="wetro",
    version="0.2.1",
    packages=find_packages(),
    install_requires=["requests","pydantic","typing_extensions"],
    author="Wetrocloud Inc",
    author_email="bolu@wetrocloud.com",
    description="Wetrocloud's Official SDK",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://docs.wetrocloud.com/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)