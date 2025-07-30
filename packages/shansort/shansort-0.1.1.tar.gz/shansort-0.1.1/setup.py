from setuptools import setup, Extension

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

ext_modules = [
    Extension(
        "shansort.shan_sort",
        sources=["shansort/shan_sort.c"],
    ),
]

setup(
    name="shansort",
    version="0.1.1",
    description="Shan Sort Algo",
    long_description=long_description,            # <-- add this
    long_description_content_type="text/markdown",  # <-- and this
    author="Bhavani Shanker",
    author_email="bhavanishanker9@proton.me",
    license="MIT",
    ext_modules=ext_modules,
    packages=["shansort"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: C",
    ],
    python_requires='>=3.6',
)


