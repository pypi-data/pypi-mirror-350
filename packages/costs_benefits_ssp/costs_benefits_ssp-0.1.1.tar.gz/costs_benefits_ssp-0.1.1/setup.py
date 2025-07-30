from setuptools import find_packages, setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="costs_benefits_ssp",
    version="0.1.1",
    author="Hermilo Cortés",
    author_email="hermilocg@tec.mx",
    description="Costs and Benefits package",
    include_package_data = True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/milocortes/costs_benefits_ssp.git",
    install_requires=[
        "SQLAlchemy>=2.0.0",
        "openpyxl>=3.1.0",
        "pandas>=2.0.0"
    ],
    packages=find_packages(exclude=("tests",)),
    package_data={
        'costs_benefits_ssp': ['database/backup/cb_data.db']
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "dev" : ["pytest>=7.0", "twine>=4.0.2"]
    },
    python_requires='>=3.11',
    tests_require=['pytest'],
)
