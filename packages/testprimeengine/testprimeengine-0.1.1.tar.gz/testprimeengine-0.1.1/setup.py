from setuptools import setup, find_packages

setup(
    name="testprimeengine",                 # your package name
    version="0.1.1",                        # matches the __version__ below
    author="Lee Bond",
    author_email="leebo@example.com",
    description="PrimeEngineAI TestPrimeEngine package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),               # finds all packages under repo
    python_requires='>=3.7',
    install_requires=[]                     # add runtime deps here, if any
)
