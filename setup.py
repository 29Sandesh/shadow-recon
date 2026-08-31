from setuptools import setup, find_packages

setup(
    name="shadow-recon",
    version="1.0.0",
    description="Instant B2B Company & Domain Intelligence OSINT Scanner",
    author="Sandesh Agrawal",
    author_email="contact@sandeshagrawal.tech",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "dnspython>=2.6.0",
        "beautifulsoup4>=4.12.0"
    ],
    entry_points={
        "console_scripts": [
            "shadow-recon=shadow_recon.cli:main",
            "shadowrecon=shadow_recon.cli:main",
            "recon=shadow_recon.cli:main",
        ]
    },
    python_requires=">=3.9",
)
