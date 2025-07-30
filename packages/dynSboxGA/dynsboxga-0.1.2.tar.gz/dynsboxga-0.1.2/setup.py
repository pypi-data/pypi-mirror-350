from setuptools import setup, find_packages

setup(
    name='dynSboxGA',
    version='0.1.2',
    author="Mohammad Luqman, Salman Ali, Faisal Anwer",
    author_email="luqman.geeky@gmail.com, salmanali.amu@gmail.com, faisalanwer.cs@amu.ac.in",
    description='A Genetic Algorithm-based dynamic AES S-box generator',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mohdluqman/dynSboxGA",
    packages=find_packages(),
    license="MIT",
    install_requires=[
        'numpy',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'generate-sbox=dynamic_sbox.sbox:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
