from setuptools import setup, find_packages

setup(
    name='PyECCIntegrity',
    version='0.1.0',
    author="Mohammad Luqman, Salman Ali, Faisal Anwer",
    author_email="luqman.geeky@gmail.com, salmanali.amu@gmail.com, faisalanwer.cs@amu.ac.in",
    description='ECC-based Integrity Verification using ECDSA and SHA-256',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mohdluqman/PyECCIntegrity",
    packages=find_packages(),
    license="MIT",
    install_requires=[
        'cryptography',
    ],
    entry_points={
        'console_scripts': [
            'verify-integrity=ecc_integrity.integrity:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
