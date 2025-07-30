from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="ds20kdb-avt",
    version="1.1.15",
    author="Alan Taylor, Paolo Franchini",
    author_email="avt@hep.ph.liv.ac.uk",
    maintainer="Alan Taylor",
    maintainer_email="avt@hep.ph.liv.ac.uk",
    description="A cross-platform Python interface to the DarkSide-20k production database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="",
    url="https://gitlab.in2p3.fr/darkside/productiondb_software/",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "aiohttp",
        "importlib-metadata",
        "pandas",
        "python-dateutil>=2.9.0",
        "requests",
        "tkcalendar",
        "ttkwidgets",
        "paramiko",
        "polars-lts-cpu",
    ],
    entry_points={
        "console_scripts": [
            "create_credentials_file = ds20kdb.create_credentials_file:main",
            "submit_vtile = ds20kdb.submit_vtile:main",
            "ds20k_create_credentials_file = ds20kdb.create_credentials_file:main",
            "ds20k_gen_tray_files_gui = ds20kdb.gen_tray_files_gui:main",
            "ds20k_qrgen = ds20kdb.qrgen:main",
            "ds20k_scanner_auto = ds20kdb.scanner_auto:main",
            "ds20k_submit_cr_test_result = ds20kdb.vtile_test_submit_cr:main",
            "ds20k_submit_vtile = ds20kdb.submit_vtile:main",
            "ds20k_submit_vtile_json = ds20kdb.submit_vtile_json:main",
            "ds20k_veto_location_gui = ds20kdb.veto_location_gui:main",
            "ds20k_veto_location = ds20kdb.veto_location:main",
            "ds20k_wafer_location_gui = ds20kdb.wafer_location_gui:main",
            "ds20k_wafer_heat_map_from_vtile_qrcodes = ds20kdb.wafer_heat_map_from_vtile_qrcodes:main",
            "ds20k_wafer_map_from_db = ds20kdb.wafer_map_from_db:main",
        ]
    },
    # see https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Environment :: Console",
        "Environment :: X11 Applications",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
    ],
)
