from setuptools import setup, find_packages

setup(
    name="microsynphylo",
    version="0.0.3",
    description="GUI for Phylogenetic Inference of Genes in Microsyntenic Blocks",
    author="Jake Leyhr",
    package_dir={"": "src"},  # 👈 tells setuptools to look in src/
    packages=find_packages(where="src"),  # 👈 search for packages inside src/
    install_requires=[
        "PyQt5",
        "toytree",
        "toyplot",
        "pandas",
        "numpy>=1.16.5,<1.23.0",
        "scipy",
        "biopython",
    ],

    entry_points={
        "console_scripts": [
            "microsynphylo=microsynphylo.microsynphylo:main"
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
