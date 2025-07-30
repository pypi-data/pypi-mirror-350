from setuptools import setup, find_packages

setup(
    name="microsynphylo",
    version="0.0.2",
    description="GUI for Phylogenetic Inference of Genes in Microsyntenic Blocks",
    author="YJake Leyhr",
    packages=find_packages(),
    install_requires=[
        "PyQt5",
        "toytree",
        "toyplot",
        "pandas",
        "numpy",
        "scipy",
        "biopython",
        "Bio"
    ],
    entry_points={
        "console_scripts": [
            "microsynphylo=microsynphylo.microsynphylo:main"
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
