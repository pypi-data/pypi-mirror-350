from setuptools import setup, find_packages

setup(
    name="p2p-terminal-chat",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "cryptography==42.0.2",
        "netifaces==0.11.0",
        "colorama==0.4.6"
    ],
    entry_points={
        'console_scripts': [
            'p2pchat=p2p_chat:main',
        ],
    },
    author="Alfonso Hernandez",
    author_email="your.email@example.com",
    description="A P2P terminal chat application with friend system",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/p2p-terminal-chat",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 