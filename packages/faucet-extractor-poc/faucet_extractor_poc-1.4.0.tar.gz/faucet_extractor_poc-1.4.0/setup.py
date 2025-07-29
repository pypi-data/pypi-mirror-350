from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

    setup(
        name="faucet-extractor-poc",
        version="1.4.0",
        author="Niagara Finance",
        author_email="niagarafinance@proton.me",
        description="Testnet faucet extractor (Proof of Concept)",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/niagarafinance/faucet-extractor-poc",
        keywords=["testnet", "faucet", "ethereum", "erc20", "web3"],
        package_dir={"": "src"},
        packages=find_packages(
            where="src", include=["faucet_extractor_poc", "faucet_extractor_poc.*"]
        ),
        package_data={"": ["*.py"]},
        include_package_data=True,
        install_requires=[
            "python-dotenv",
            "requests",
        ],
        entry_points={
            "console_scripts": [
                "faucet-extractor=faucet_extractor_poc.extract:main",
            ],
        },
        classifiers=[
            "License :: Other/Proprietary License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
        ],
        python_requires=">=3.10",
    )
