from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='vietnamese_address_parser',
    version='0.1.3',
    author='Dang Anh Dat',
    author_email='contact.anhdat@gmail.com',
    packages=find_packages(),
    package_data={
        'vietnamese_address_parser': ['tinh_qh_px_20_05_2025.json'],  # <--- IMPORTANT
    },
    install_requires=[
        # Add dependencies here
        "requests",
    ],
    entry_points={
        'console_scripts': [
            'vietnamese_address_parser = vietnamese_address_parser:hello', 
        ],
    },
    python_requires='>=3.9',
    long_description=description,
    long_description_content_type="text/markdown",
)