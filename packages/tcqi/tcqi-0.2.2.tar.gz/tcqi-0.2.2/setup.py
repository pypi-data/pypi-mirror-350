from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name='tcqi',
    version='0.2.2',
    author="Sebastián Christen",
    author_email="schristen@itec.cat",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(),
    install_requires=[
        'numpy>=2.2.0',
        'pandas>=2.2.3',
        'plotly>=6.1.0',
        'tabulate>=0.9.0'
    ],
    description="Intended to facilitate the modification of TCQi files",
    long_description=description,
    long_description_content_type="text/markdown",
    license="CC-BY-NC-ND"
)