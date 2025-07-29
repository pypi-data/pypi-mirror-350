from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="tunnelmate",
    version="1.0.5",
    author="Parsa Lakzian (with Tara AI)",
    description="Full-featured SSH tunnel & Cloudflare DNS management library and CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["requests", "pyyaml"],
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'tunnelmate = ssh_tunneler.cli:main'
        ]
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
