from setuptools import setup, find_packages

setup(
    name="Lavender-CcGAN",
    version="0.0.3",
    description="A pip package of model CcGAN.",
    long_description=open(
        "README.md").read(),
    long_description_content_type="text/markdown",
    author="Zeyu Xie",
    author_email="xie.zeyu20@gmail.com",
    url="https://github.com/Zeyu-Xie/Lavender-CcGAN",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
