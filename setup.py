import setuptools

setuptools.setup(
    name='everpay',
    version='0.3.0',
    packages=['everpay',],
    license='MIT',
    description = 'Python wrappers for everpay.io api',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author = 'xiaojay',
    author_email = 'xiaojay@gmail.com',
    install_requires=['requests', 'web3', 'python-jose', 'arweave-python-client', 'eth_account'],
    url = 'https://github.com/everFinance/everpay.py',
    download_url = 'https://github.com/everFinance/everpay.py/archive/refs/tags/v0.3.0.tar.gz',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
