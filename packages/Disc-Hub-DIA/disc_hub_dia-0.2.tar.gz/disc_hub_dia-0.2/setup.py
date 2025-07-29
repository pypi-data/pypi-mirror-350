from setuptools import setup, find_packages

setup(
    name="Disc_Hub_DIA",
    version="0.2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["numpy","matplotlib","pandas",
                      "torch>=2.6.0","xgboost","scikit-learn"], #pip install torch==2.6.0+cu126 --extra-index-url https://download.pytorch.org/whl/cu126
    author="Yiwen Yu",
    description="A package for Disc Hub Data Integration Analysis",
)