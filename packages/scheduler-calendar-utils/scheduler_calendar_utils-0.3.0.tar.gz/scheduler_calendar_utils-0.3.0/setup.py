from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = cythonize([
    Extension(
        name="scheduler_calendar_utils.helpers",
        sources=["scheduler_calendar_utils/helpers.py"],
    )
], compiler_directives={"language_level": "3"})

setup(
    name="scheduler_calendar_utils",
    version="0.3.0",
    description="Utilities for database/firestore interaction and structured HTTP responses",
    author="Your Name",
    packages=["scheduler_calendar_utils"],
    ext_modules=extensions,
    install_requires=[
        "Flask>=3, <4",
        "SQLAlchemy>=2, <3",
        "Cython>=3, <4",
        "PyMySQL>=1, <2",
        "cloud-sql-python-connector>=1, <2",
        "google-cloud-firestore>=2, <3"
    ],
    zip_safe=False,
)