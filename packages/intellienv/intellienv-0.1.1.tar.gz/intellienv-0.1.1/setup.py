from setuptools import setup, find_packages
import pathlib

readme_path = pathlib.Path(__file__).parent.resolve() / "README.md"
long_description = readme_path.read_text(encoding="utf-8")

setup(
    name="intellienv",
    version="0.1.1",
    description="A Python package for managing environment variables safely and conveniently",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Adithya Nair",
    author_email="66921216+AdiNairCS50@users.noreply.github.com",
    license="MIT",
    url="https://github.com/AdiNairCS50/intellienv",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'intellienv=intellienv.__main__:main',
        ],
    },
    keywords="environment, variables, configuration, dotenv, env, config",
    project_urls={
        "Bug Tracker": "https://github.com/AdiNairCS50/intellienv/issues",
        "Documentation": "https://github.com/AdiNairCS50/intellienv#readme",
        "Source Code": "https://github.com/AdiNairCS50/intellienv",
    },
)