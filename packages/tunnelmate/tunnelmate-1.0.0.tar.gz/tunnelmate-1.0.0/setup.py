from setuptools import setup, find_packages

setup(
    name="tunnelmate",
    version="1.0.0",
    author="Parsa Lakzian (with Tara AI)",
    description="Full-featured SSH tunnel & Cloudflare DNS management library and CLI",
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
