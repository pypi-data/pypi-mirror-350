from setuptools import setup

setup(
    name="python-gestpay",
    version="2.1.0",
    description="Gestpay WSs2s and WsCryptDecrypt SOAP Client",
    url="https://github.com/metadonors/python-gestpay",
    author="Metadonors",
    author_email="services@metadonors.it",
    license="MIT",
    packages=["pygestpay"],
    install_requires=[
        "zeep",
    ],
    zip_safe=False,
)
