from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="unrun",
    version="0.2.0",
    author="Casper Huang",
    author_email="casper.w.huang@qq.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/howcasperwhat/unrun",
    packages=find_packages(where="packages"),
    package_dir={'': 'packages'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'unrun=unrun.cli:main',
        ],
    },
    install_requires=[
        'PyYAML',
        'rich',
    ],
    extras_require={
        "dev": [
            "pytest",
            "flake8",
            "twine",
            "wheel"
        ],
    },
)
