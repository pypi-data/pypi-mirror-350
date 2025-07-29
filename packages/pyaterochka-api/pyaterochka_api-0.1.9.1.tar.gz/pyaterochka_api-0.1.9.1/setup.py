from setuptools import setup, find_packages

setup(
    name='pyaterochka_api',
    version='0.1.9.1',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'camoufox[geoip]',
        'beartype',
        'fake-useragent',
        'tqdm'
    ],
    extras_require={
        'tests': [
            'pytest',
            'pytest-asyncio',
            'pytest-typed-schema-shot',
        ]
    },
    author='Miskler',
    description='A Python API client for Pyaterochka store catalog',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Open-Inflation/pyaterochka_api',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
        'Topic :: Utilities',
    ],
    python_requires='>=3.10',
)
