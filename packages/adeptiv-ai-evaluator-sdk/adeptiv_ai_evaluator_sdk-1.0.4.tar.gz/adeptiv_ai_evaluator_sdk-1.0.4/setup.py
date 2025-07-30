from setuptools import setup, find_packages

setup(
    name="adeptiv-ai-evaluator-sdk",
    version="1.0.4",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "boto3>=1.26.0",
        "botocore>=1.29.0",
        "asyncio>=3.4.3",
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "aws": [
            "boto3>=1.26.0",
            "botocore>=1.29.0",
            "aioboto3>=11.0.0",
        ]
    },
    author="Adeptiv-AI Evaluation Team",
    author_email="support@adeptiv-ai.com",
    description="Async client SDK for submitting model outputs to Adeptiv-AI evaluation service via AWS",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/adeptiv-ai/evaluator-sdk",
    project_urls={
        "Bug Tracker": "https://github.com/adeptiv-ai/evaluator-sdk/issues",
        "Documentation": "https://docs.adeptiv-ai.com/sdk",
        "Source Code": "https://github.com/adeptiv-ai/evaluator-sdk",
        "Homepage": "https://adeptiv-ai.com",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO",
    ],
    keywords=[
        "adeptiv-ai",
        "evaluation",
        "model-evaluation", 
        "ai",
        "machine-learning",
        "async",
        "aws",
        "sqs",
        "lambda"
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "adeptiv-ai-eval=adeptiv_ai_evaluator.cli:main",
        ],
    },
    package_data={
        "adeptiv_ai_evaluator": ["py.typed"],
    },
    include_package_data=True,
    zip_safe=False,
)