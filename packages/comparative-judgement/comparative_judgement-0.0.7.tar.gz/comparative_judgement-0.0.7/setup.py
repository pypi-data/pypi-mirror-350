from setuptools import setup, find_packages

VERSION = '0.0.7'
DESCRIPTION = 'A package for conducting Comparative Judgement'
LONG_DESCRIPTION = open('README.md').read()

# Setting up
setup(
    name = "comparative_judgement",
    version = VERSION,
    author = "Andy Gray",
    description = DESCRIPTION,
    long_description_content_type = "text/markdown",
    long_description = LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'ray'],
    keywords=['python', 'comparative', 'judgement', 'Bayesian', 'BTM'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)