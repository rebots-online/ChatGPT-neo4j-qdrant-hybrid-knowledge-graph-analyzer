from setuptools import setup, find_packages

setup(
    name="chat-knowledge-grapher",
    version="0.1.0",
    description="A system for analyzing chat conversations using vector embeddings and knowledge graphs",
    author="Robin L. M. Cheung",
    packages=find_packages(),
    install_requires=[
        line.strip()
        for line in open("requirements.txt")
        if line.strip() and not line.startswith("#")
    ],
    entry_points={
        "console_scripts": [
            "chat-analysis-server=mcp_modules.analysis.chat_analysis_server:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: General",
    ],
)