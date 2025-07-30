from setuptools import setup, find_packages

setup(
    name="hume_api",
    version="0.2.6",
    description="Simple client for Hume API with audio support",
    author="shiventi",
    packages=find_packages(),
    install_requires=[
        "websocket-client",
        "pyaudio",
        "requests"
    ],
    python_requires=">=3.7",
    url="https://github.com/shiventi",
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
