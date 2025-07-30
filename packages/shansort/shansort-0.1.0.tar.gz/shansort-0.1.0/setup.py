from setuptools import setup, Extension

ext_modules = [
    Extension(
        "shansort.shan_sort",  # module name exposed to Python
        sources=["shansort/shan_sort.c"],
    ),
]

setup(
    name="shansort",
    version="0.1.0",
    description="Stable ShanSort radix sort module implemented in C",
    author="Your Name",
    author_email="your.email@example.com",
    license="MIT",
    ext_modules=ext_modules,
    packages=["shansort"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
