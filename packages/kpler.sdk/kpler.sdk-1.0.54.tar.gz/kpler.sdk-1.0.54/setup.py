from setuptools import find_namespace_packages, setup


with open("README.md") as fh:
    long_description = fh.read()

setup(
    name="kpler.sdk",
    description="A Python wrapper around the Kpler client API",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/kpler/python-sdk",
    author="Kpler",
    author_email="engineering@kpler.com",
    license="Apache License, Version 2.0",
    packages=find_namespace_packages(
        where="src",
        include=["kpler*"],
    ),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=1.0.0,<=1.5.3",
        "requests>=2.20.0,<=2.31.0",
        "numpy<2",
    ],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "doc": [
            "Sphinx==5.0.0",
            "sphinx_rtd_theme==1.0.0",
            "sphinx-autodoc-typehints==1.12.0",
        ],
        "test": [
            "pytest==6.2.5",
            "python-dateutil==2.8.1",
            "pytest-rerunfailures==11.1.2",
            "black==18.9b0",
            "mypy-extensions==1.0.0",
            "mypy==1.8.0",
            "pre-commit==2.6.0",
            "pytest-cov==5.0.0",
        ],
        "publish": [
            "twine==4.0.2",
            "urllib3>=1.21.1,<2.2",
            "importlib-metadata<8.0.0"
        ],
    },
)
