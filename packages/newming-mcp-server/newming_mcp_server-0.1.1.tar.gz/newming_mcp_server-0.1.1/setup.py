from setuptools import setup, find_packages

setup(
    name="newming-mcp-server",
    version="1.0.0",
    description="Newming MCP Server for Claude Desktop (STDIO Mode)",
    author="Newming",
    packages=find_packages(),
    install_requires=[
        "fastmcp",
        "pandas",
        "requests"
    ],
    entry_points={
        'console_scripts': [
            'newming-mcp=main:main',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 