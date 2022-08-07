import setuptools

with open("README.md", "r", encoding="utf-8") as file_handle:
    long_description = file_handle.read()

setuptools.setup(
    name="plantstar-shared",
    version="0.1.23",
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
        "Django>=4.0.4",
        "msgpack>=1.0.4",
        "psycopg2>=2.9.3",
        "python-dateutil>=2.8.2",
        "pytz>=2022.1",
        "requests>=2.27.1",
    ]
)
