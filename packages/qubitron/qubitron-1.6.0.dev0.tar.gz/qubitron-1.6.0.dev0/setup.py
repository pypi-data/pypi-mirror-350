import runpy
from setuptools import setup, find_packages

# Get the version string from your version file
__version__ = runpy.run_path('qubitron-core/qubitron/_version.py')['__version__']
assert __version__, 'Version string cannot be empty'

name = 'qubitron'
description = (
    'A framework for creating, editing, and invoking '
    'Noisy Intermediate Scale Quantum (NISQ) circuits.'
)

# Read the long description from README
long_description = open('README.md', encoding='utf-8').read()

# Hardcoded install requirements — you must list your modules manually now
requirements = [
    "numpy>=1.22",
    "scipy",
    "sympy",
    "networkx",
    # Add more dependencies here as needed
]

setup(
    name=name,
    version=__version__,
    url='http://github.com/amyssnippet/qubitron',
    author='The Qubitron Developers',
    author_email='qubitron-dev@googlegroups.com',
    maintainer="Amol S",
    maintainer_email="your-email@example.com",
    python_requires='>=3.11.0',
    install_requires=requirements,
    license='Apache-2.0',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(where="qubitron-core"),
    package_dir={"": "qubitron-core"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Quantum Computing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
    keywords=[
        "quantum computing",
        "qubitron",
        "nisq",
        "quantum circuit simulator",
        "quantum programming",
        "simulation",
    ],
)
