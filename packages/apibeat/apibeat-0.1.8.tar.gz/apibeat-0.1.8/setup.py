from setuptools import setup, find_packages

setup(
    name="apibeat",
    version="0.1.8",
    author="Vijay Rajpoot",
    author_email="demonking15543@gmail.com",
    description="Benchmarking tool to compare REST and GraphQL API performance",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/demonking15543/api-performance-monitor",
    packages=find_packages(),
    install_requires=["requests"],
    include_package_data=True,
   entry_points={
        "console_scripts": [
            "apibeat=apibeat.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
        keywords=["api", "benchmark", "graphql", "rest", "latency", "performance", "cli"],

)