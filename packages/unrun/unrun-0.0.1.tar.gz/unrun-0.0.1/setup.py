import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unrun",
    version="0.0.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/unrun",
    packages=setuptools.find_packages(where="packages"),
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
    ],
)
