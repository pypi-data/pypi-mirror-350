from setuptools import setup, find_packages

setup(
    name="ufm-config-diff",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "paramiko",
        "colorama",
        "beautifulsoup4",
    ],
    entry_points={
        "console_scripts": [
            "ufm-config-diff=ufm_config_diff.config_diff:main",
        ],
    },
    author="NVIDIA",
    author_email="support@nvidia.com",
    description="Advanced UFM configuration comparison tool with interactive HTML reports, table sorting/filtering, and email notifications",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Mellanox/ufm-config-diff",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Networking",
        "Topic :: Software Development :: Testing",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
    keywords="ufm nvidia mellanox infiniband docker configuration comparison networking",
    project_urls={
        "Bug Reports": "https://github.com/Mellanox/ufm-config-diff/issues",
        "Source": "https://github.com/Mellanox/ufm-config-diff",
        "Documentation": "https://github.com/Mellanox/ufm-config-diff/blob/master/README.md",
    },
) 