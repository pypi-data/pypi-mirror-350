from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
 
setup(
    name='apigle',
    version='1.0.1',
    description='Official Python client for Apigle.com API',
    long_description=long_description,
    long_description_content_type="text/markdown",  # Bu önemli!
    url="https://github.com/boztek/apigle-python",
    author='Boztek LTD',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    python_requires='>=3.7',
)
