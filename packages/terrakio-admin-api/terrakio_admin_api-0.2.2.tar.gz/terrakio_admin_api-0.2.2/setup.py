from setuptools import setup

setup(
    name="terrakio_admin_api",
    version="0.2.2",
    author="Yupeng Chao",
    author_email="yupeng@haizea.com.au",
    description="Admin API client for Terrakio services",
    url="https://github.com/HaizeaAnalytics/terrakio-python-api",
    packages=["terrakio_admin_api"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.7",
    install_requires=[
        "terrakio-core>=0.1.0",
    ],
    metadata_version='2.2'
) 