import setuptools
with open("README.md",encoding='utf-8') as fh:
    long_description = fh.read()
setuptools.setup(
    name="pylibswathi",
    version=0.1,
    author="Swathi Dattha Lakshmi Pasupuleti",
    author_email="swathipasupuleti02@gmail.com",
    description="A Python library for data analysis and visualization using pandas, numpy, matplotlib, and seaborn.",
    long_description=long_description, 
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pandas>=1.0',
        'numpy>=1.18',
        'matplotlib>=3.0',
        'seaborn>=0.10'
    ],
)