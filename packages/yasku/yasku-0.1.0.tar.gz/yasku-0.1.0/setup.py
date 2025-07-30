from setuptools import setup, find_packages

setup(
    name="yasku",
    version="0.1.0",
    description="Yet Another Science Keppy Upy - Keep up to date with science fields via PubMed and Discord.",
    author="Albert Lahat",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pyyaml",
        "tqdm"
    ],
    entry_points={
        'console_scripts': [
            'yasku = yasku.main:main',
            'yasku_config = yasku.config:main'
        ]
    },
    python_requires='>=3.7',
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
