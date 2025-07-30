from setuptools import setup, find_packages

setup(
    name="smaj_kyber",
    version="0.1.3",
    author="Yinka John Adegoke",
    description="Kyber KEM wrapper using ctypes and platform-specific dynamic libraries",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "smaj_kyber": [
            "lib/*.dylib",  # macOS
            "lib/*.dll",    # Windows
            "lib/*.so",     # Linux
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="MIT",
)
