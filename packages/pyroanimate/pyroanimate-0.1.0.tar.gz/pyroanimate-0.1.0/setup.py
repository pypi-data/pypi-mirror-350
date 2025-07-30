from setuptools import setup, find_packages

setup(
    name="Pyroanimate",
    version="0.1.0",
    description="A simple animation library for Pyrogram bots",
    author="dap3842",
    author_email="afistal@mail.ru",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "pyrogram>=2.0.0"
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)