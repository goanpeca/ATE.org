from setuptools import setup, find_packages


with open("requirements.txt") as f:
    install_requirements = f.read().splitlines()
    print(install_requirements)

setup(
        name="APP",
        version="1.0",
        packages=find_packages(),
        python_requires='>=3.7',
        install_requires=install_requirements
)
