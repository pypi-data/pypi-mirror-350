from setuptools import setup, find_packages

setup(
    name="authflow-sdk",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    author="AuthFlow",
    author_email="support@authflow.com",
    description="Official AuthFlow SDK for Python",
    keywords="auth, authentication, authflow, oauth, sdk",
    url="https://authflow.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)