from setuptools import setup, find_packages

setup(
    name="p2p_messenger",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'cryptography==42.0.2',
        'pycryptodome==3.20.0',
        'psutil',
    ],
    entry_points={
        'console_scripts': [
            'p2p_messenger=node:main',
        ],
    },
    author="Alfonso Hernandez",
    description="A decentralized P2P messaging app",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tu-usuario/p2p_messenger",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={
        'p2p_messenger': ['*.py'],
    },
    include_package_data=True,
) 