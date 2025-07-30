from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chatterbox-io",
    version="0.3.0",
    author="OverQuotaAI",
    author_email="support@chatter-box.io",
    description="Python client for ChatterBox - Integrate with Zoom, Teams, Google Meet for real-time transcripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OverQuotaAI/chatterbox-python",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.32.3",
        "python-socketio>=5.12.1",
        "pydantic>=2.11.1",
    ],
    extras_require={
        "dev": [
            "pytest>=8.3.5",
            "black>=25.1.0",
            "isort>=6.0.1",
            "flake8>=7.2.0",
        ],
    },
) 