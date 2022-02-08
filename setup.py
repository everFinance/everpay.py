import setuptools

setuptools.setup(
    name='everpay',
    version='0.1.0',
    packages=['everpay',],
    license='MIT',
    description = 'Python wrappers for everpay.io api',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author = 'xiaojay',
    author_email = 'xiaojay@gmail.com',
    install_requires=['requests', 'web3.py', 'python-jose'],
    url = 'https://github.com/everFinance/everpay.py',
    download_url = 'https://github.com/everFinance/everpay.py/archive/refs/tags/v0.1.0.tar.gz',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    )
