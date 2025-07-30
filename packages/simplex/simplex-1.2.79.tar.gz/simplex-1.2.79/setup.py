from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call
import sys

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        # Only install rebrowser-playwright if playwright version is being installed
        if any('playwright' in arg for arg in sys.argv):
            check_call(["rebrowser-playwright", "install"])

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # Only install rebrowser-playwright if playwright version is being installed
        if any('playwright' in arg for arg in sys.argv):
            check_call(["rebrowser-playwright", "install"])

setup(
    name="simplex",
    version="1.2.79",
    packages=find_packages(),
    package_data={
        "simplex": ["browser_agent/dom/*.js"],  # Include JS files in the dom directory
    },
    install_requires=[
        "colorama",
        "requests",
        "python-dotenv",
        "click",
    ],
    extras_require={
        'playwright': ['rebrowser-playwright>=1.0.0'],  # Full version with rebrowser-playwright
    },
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'simplex=simplex.cli:main',
        ],
    },
    author="Simplex Labs, Inc.",
    author_email="founders@simplex.sh",
    description="Official Python SDK for Simplex API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://simplex.sh",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.9",
) 