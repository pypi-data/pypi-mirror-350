from setuptools import setup, find_packages    
import codecs
import os

here = os.path.abspath(os.path.dirname("README.md"))

with codecs.open(os.path.join(here, "README.md")) as fh:
    long_description = fh.read()

here = os.path.abspath(os.path.dirname("requirement.txt"))

with codecs.open(os.path.join(here, "requirement.txt"), encoding="utf-8") as fh:
    required = fh.read().splitlines()


setup(
        name='gcoupler',
        version='1.2',
        description='Interactome Prediction using Gcoupler',
        long_description_content_type="text/markdown",
        long_description=long_description,
        url="https://github.com/the-ahuja-lab/Gcoupler",
        author="Sanjay Kumar Mohanty",
        author_email="sanjaym@iiitd.ac.in",
        py_modules=["Synthesizer","Authenticator","Generator","BioRanker"],
        package_dir={'':'src'},
        extras_require={
        "dev":required,
        },
        packages=find_packages(),
        classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        ],
)
