from setuptools import setup, find_packages

setup(
    name="TwoPy",
    version="1.0.4",
    author="starfal8k",
    include_package_data=True,
    install_requires=[
        'argparse',
        'cryptography'
    ],
    description="Python project builder with encryption capability.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://example.com/twopy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
