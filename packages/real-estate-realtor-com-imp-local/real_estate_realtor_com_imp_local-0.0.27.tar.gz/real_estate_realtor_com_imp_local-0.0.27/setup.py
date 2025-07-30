import setuptools

PACKAGE_NAME = "real-estate-realtor-com-imp-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version="0.0.27",  # https://pypi.org/project/real-estate-realtor-com-imp-local/
    author="Circles",
    author_email="info@circles.ai",
    description="PyPI Package for Real estate python package",
    long_description="This is a package for sharing common realtor functions used in different repositories",
    long_description_content_type="text/markdown",
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f"{package_dir}/src"},
    package_data={package_dir: ["*.py"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "importer-local>=0.0.33",
        "logger-local>=0.0.55",
        "database-mysql-local>=0.0.290",
        "location-local>=0.0.23",
        "entity-type-local>=0.0.12",
        "selenium",
    ],
)
