# setup.py
from setuptools import setup, find_packages

setup(
    name="photonkit",  # 🔄 changed from 'photonic'
    version="0.1.0",
    description="PhotonKit -- A mildly opinonated toolkit for managing your camera photo collection",
    author="Rahul Singh",
    license="MIT",
    packages=find_packages(include=["backup", "backup.*"]),
    entry_points={
        "console_scripts": [
            "photonkit = backup.photo_backup:main"  # 👈 CLI command will now be `photonkit`
        ]
    },
    install_requires=[],
    python_requires=">=3.8",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
)
