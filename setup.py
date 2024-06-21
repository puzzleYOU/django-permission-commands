from setuptools import find_packages, setup

setup(
    name="django-permission-commands",
    version="0.1.0",
    description="Django management commands for ruling groups and permissions based on django.contrib.auth",
    author="puzzleYOU GmbH",
    packages=find_packages("."),
    install_requires=["Django"],
    zip_safe=True,
)
