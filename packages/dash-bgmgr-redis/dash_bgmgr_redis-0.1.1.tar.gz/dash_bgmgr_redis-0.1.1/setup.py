from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="dash-bgmgr-redis",
    version="0.1.1",
    author="Razgriz Hsu",
    author_email="dev@raz.tw",
    description="Redis-based background callback manager for Dash applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RazgrizHsu/dash-bgmgr-redis",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ]
    },
    keywords="dash redis background callback manager",
    project_urls={
        "Bug Reports": "https://github.com/RazgrizHsu/dash-bgmgr-redis/issues",
        "Source": "https://github.com/RazgrizHsu/dash-bgmgr-redis",
    },
)
