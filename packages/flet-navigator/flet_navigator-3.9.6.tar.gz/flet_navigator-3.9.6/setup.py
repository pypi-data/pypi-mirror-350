from setuptools import setup, find_packages

setup(
    name="flet_navigator",
    version="3.9.6",
    author="Evan",
    description="⚡⚓ Minimalistic, fast, and effective navigation/routing library for Flet applications.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/xzripper/flet_navigator",
    download_url="https://github.com/xzripper/flet_navigator/archive/refs/tags/v3.9.6.tar.gz",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Development Status :: 6 - Mature"
    ],
    install_requires=[],
    python_requires=">=3.9",
)
