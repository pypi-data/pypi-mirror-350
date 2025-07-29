from setuptools import setup, find_packages

setup(
    name='vietnamese_address_parser',
    version='v0.1.9',
    author='Dang Anh Dat',
    author_email='contact.anhdat@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    package_data={"vietnamese_address_parser": ["*.json"]},
    install_requires=[
        # Add dependencies here
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "vietnamese_address_parser=vietnamese_address_parser.cli:main",
        ],
    },
    python_requires='>=3.9',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
)