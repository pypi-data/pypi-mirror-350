# setup.py

from setuptools import find_packages, setup

from maitai_common.version import version

setup(
    name="maitai-python",
    version=version,
    packages=find_packages(
        exclude=(
            "maitai_back",
            "maitai_back.*",
            "apps",
            "apps.*",
            "maitai_gen",
            "maitai_gen.*",
            "maitai_models",
            "maitai_models.*",
        ),
        include=(
            "maitai.*",
            "maitai",
            "maitai_common",
            "maitai_common.*",
        ),
    ),
    install_requires=[
        "openai>=1.34.0",
        "httpx[http2]",
        "websocket-client",
        "pyhumps",
        "pydantic>=2.0.0",
        "groq",
    ],
    # Optional metadata
    author="Maitai",
    author_email="support@trymaitai.ai",
    description="Maitai SDK for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://docs.trymaitai.ai",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
