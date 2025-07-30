from setuptools import setup, find_packages

setup(
    name="mkdocs-suppress-logs-plugin",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["mkdocs>=1.1"],
    entry_points={
        "mkdocs.plugins": [
            "suppress_logs = mkdocs_suppress_logs_plugin:SuppressLogsPlugin"
        ]
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="MkDocs plugin to suppress unwanted log messages using pattern matching.",
    long_description="Suppress MkDocs or plugin log messages using wildcard patterns like '{*}' for cleaner builds.",
    long_description_content_type="text/markdown",
    url="https://github.com/yourname/mkdocs-suppress-logs-plugin",
    classifiers=[
        "Framework :: MkDocs",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.7',
)
