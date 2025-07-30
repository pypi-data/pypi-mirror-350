import setuptools
import subprocess
import os

ROOT = os.path.dirname(__file__)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def get_version():
    try:
        tags = subprocess.check_output(["git", "tag"]).decode("utf-8").strip()
        tags = tags.split()
        vault_tags = [i for i in tags if 'vault' in i]
        vault_tags.sort()
        version = (
            vault_tags[-1].split('vault_')[1] if len(vault_tags) > 0 else "0.0.5"
        )
        return version
    except Exception as e:
        print(f"Failed to get version due to: {e}")
        return "0.0.5"

def get_requires():
    """Parse requirements from requirements.txt"""
    try:
        install_reqs = []
        if os.path.exists('requirements.txt'):
            with open('requirements.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        install_reqs.append(line)
        return install_reqs
    except Exception as e:
        print(f"Failed to parse requirements: {e}")
        return []

setuptools.setup(
    name="vault-sdk-gyan",
    version=get_version(),
    author="K Sridhar",
    author_email="sridhar@concentric.ai",
    description="Concentric Vault Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/concentricai/apputils",
    project_urls={
        "Source": "https://bitbucket.org/concentricai/apputils/src/main/vaultsdk/pythonSdk/",
        "Bug Tracker": "https://concentricai.atlassian.net/jira/software/c/projects/SW/boards/2/backlog",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=get_requires(),
    include_package_data=True,
    zip_safe=False,
)
