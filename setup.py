import setuptools

with open("README.md", "r", encoding="utf-8") as file_handle:
    long_description = file_handle.read()

setuptools.setup(
    name="plantstar-shared",
    # MAJOR_MILESTONE_VERSION.MINOR_MILESTONE_VERSION.MAJOR_VERSION.MINOR_VERSION.HOTFIX_VERSION.SUBVERSION
    # The main version should stay as v2.0.3.0.x until we have passed that in the plantstar_apu/plantstar_dcm projects
    version="2.0.3.0.2.36",
    author="SYSCON International",
    author_email="dev@syscon-intl.com",
    description="Shared code used in plantstar_apu and plantstar_dcm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SYSCON-International/plantstar_shared",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        # Make sure to update the requirements.txt to match any changes made to this section
        "Django>=4.2.0",
        "msgpack>=1.0.4",
        "psycopg2>=2.9.9",
        "python-dateutil>=2.8.2",
        "pytz>=2023.4",
        "requests>=2.31.0",
    ]
)
