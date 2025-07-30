# setup.py

import setuptools
import os

# --- Get the long description from the README file ---
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# --- Get the version (a common way is from a __version__.py file) ---
# For now, let's define it directly, but consider moving it to pybrainorg/__init__.py
# or pybrainorg/version.py and reading it from there.
# Example if it were in pybrainorg/__init__.py:
# version_info = {}
# with open(os.path.join("pybrainorg", "__init__.py")) as fp: # Adjust 'pybrainorg' if your package name differs
#     exec(fp.read(), version_info)
# current_version = version_info['__version__']
current_version = "0.1.0" # Initial development version

# --- List the dependencies ---
# It's good to specify minimum versions if you know of incompatibilities.
# You can read from a requirements.txt or list them here.
install_requires = [
    "brian2>=2.5",      # Core simulation engine
    "numpy>=1.20",      # Numerical array manipulation
    "matplotlib>=3.4",  # For plots and visualizations
    "scipy>=1.7",       # Scientific functions (often a Brian2 dependency)
    "networkx>=2.6",    # For graph analysis and visualization (in analysis/visualization)
    # Add other RUNTIME dependencies here
]

# --- Optional dependencies (for development, testing, documentation) ---
extras_require = {
    "dev": [
        "pytest>=6.0",
        "flake8>=3.9",
        "black>=21.0b0",
        "ipykernel", # For running example notebooks
        "jupyterlab",
    ],
    "docs": [
        "sphinx>=4.0",
        "sphinx-rtd-theme>=1.0",
        "nbsphinx>=0.8",
        "ipykernel", # nbsphinx needs this to execute notebooks
    ],
    "test": [
        "pytest>=6.0",
    ]
}
extras_require["all"] = sum(extras_require.values(), [])


setuptools.setup(
    name="pybrainorg",  # Package name as it will appear on PyPI
    version=current_version,
    author="Luciano Silva / Bioquaintum Research & Development", # Replace
    author_email="luciano.silva@bioquaintum.io", # Replace
    description="A Python Brain Organoid Simulator using Brian2.",
    long_description=long_description,
    long_description_content_type="text/markdown", # Content type of the README
    url="https://github.com/bioquaintum/pybrainorg",  # URL of your GitHub repository (Replace)
    project_urls={ # Additional useful URLs
        "Bug Tracker": "https://github.com/bioquaintum/pybrainorg/issues",
        "Documentation": "https://pybrainorg.readthedocs.io/", # If you host on ReadTheDocs
        "Source Code": "https://github.com/your_username/pybrainorg",
    },
    packages=setuptools.find_packages(
        where='.', # Look for packages from the current directory
        exclude=['tests*', 'examples*'] # Exclude tests and examples directories
    ),
    # If your code was in a 'src/pybrainorg' directory:
    # package_dir={'': 'src'},
    # packages=setuptools.find_packages(where='src', exclude=("tests*", "examples*")),

    classifiers=[ # Classifiers help users find your project
        "Development Status :: 3 - Alpha",  # Development stage
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",  # Replace with your chosen license
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: English",
    ],
    python_requires='>=3.7',  # Minimum supported Python version
    install_requires=install_requires,
    extras_require=extras_require,
    # If you have non-code package data that needs to be included:
    # include_package_data=True,
    # package_data={
    #     'pybrainorg': ['data_files/*.json'], # Example
    # },
    # If you have command-line executable scripts:
    # entry_points={
    #     'console_scripts': [
    #         'pybrainorg_cli=pybrainorg.cli:main_function', # Example
    #     ],
    # },
    keywords="brain organoid simulation brian2 neuroscience computational-neuroscience",
)
