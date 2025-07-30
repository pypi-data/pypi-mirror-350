from setuptools import setup

setup(

    name = "zModule",
    version = "1.0.6",
    description = "Just some Modules.",
    author = "zisia13",
    github = "zisia13",
    author_email = "nothing@nothing.com",
    packages = ["zModules",
                "zModules.zBanner",
                "zModules.zOs",
                "zModules.zCryptography",
                "zModules.zDatabase",
                "zModules.zCtk",
                "zModules.zNetwork"
               ],
    install_requires = [],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)