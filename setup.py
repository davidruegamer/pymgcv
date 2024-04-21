from setuptools import setup, find_packages

setup(
    name="pymgcv",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "rpy2",
        "pandas"
    ],
    # Optional
    author="David Ruegamer",
    author_email="david.ruegamer@stat.uni-muenchen.de",
    description="A collection of translated functions from the mgcv R package.",
    license="GPL-3",
    url="github.com/davidruegamer/pymgcv",
)

