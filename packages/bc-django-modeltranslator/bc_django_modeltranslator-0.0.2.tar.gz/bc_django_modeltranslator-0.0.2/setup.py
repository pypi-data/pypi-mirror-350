from setuptools import setup, find_packages

setup(
    name="bc_django_modeltranslator",
    version="0.0.2",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    description="A Django app for adding field-level translations to your models.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="max_luci4",
    author_email="max@gmail.com",
    url="https://github.com/chigan0/bc-model-translator.git",
    classifiers=[
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7"
)
