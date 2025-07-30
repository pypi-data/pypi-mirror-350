from setuptools import setup, find_packages

setup(
    name="arkhelm-tml",
    version="0.0.3",
    author="Taireru LLC",
    author_email="tairerullc@gmail.com",
    description="Arkhelm Online Modding.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TaireruLLC/arkhelm_tml",
    packages=find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="MIT",
)
