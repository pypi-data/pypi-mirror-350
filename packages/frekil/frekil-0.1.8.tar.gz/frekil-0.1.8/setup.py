"""
Setup script for the Frekil SDK
"""

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        packages=find_packages(include=["frekil", "frekil.*"]),
    )
