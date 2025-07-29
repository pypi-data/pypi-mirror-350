from setuptools import setup, find_packages

setup(
    name="abstract-framehub-client",
    version="0.1.5",
    packages=find_packages(),
    install_requires=[
        "grpcio",
        "protobuf"
    ],
    author="ThéoMottet",
    description="Client Python for AbstractFrameHub Server",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/stackngo-client/abstract-framehub-client-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.7',
)