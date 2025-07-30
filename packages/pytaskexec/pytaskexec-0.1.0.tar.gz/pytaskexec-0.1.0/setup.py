from setuptools import setup, find_packages

setup(
    name="pytaskexec",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'concurrent-futures;python_version<"3.2"',  # Only needed for Python < 3.2
    ],
    author="anandan-bs",
    author_email="",  # You'll need to add your email
    description="A lightweight task execution system for concurrent operations in Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/anandan-bs/pytaskexec",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords=["task", "concurrent", "async", "threading", "executor"],
    project_urls={
        "Source": "https://github.com/anandan-bs/pytaskexec",
        "Bug Reports": "https://github.com/anandan-bs/pytaskexec/issues",
    },
)
