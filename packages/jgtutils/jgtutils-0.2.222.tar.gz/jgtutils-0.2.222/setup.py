import re

from setuptools import find_packages, setup


def read_version():
    with open("jgtutils/__init__.py") as f:
        content=f.read()
        version_match = re.search(r"version=['\"]([^'\"]*)['\"]", content)
        return version_match.group(1)

version = read_version()

setup(
    name='jgtutils',
    version=version,
    packages=find_packages(),
    #install_requires=INSTALL_REQUIRES,
    description='A utility package common to other JGT projects.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Guillaume Isabelle',
    author_email='jgi@jgwill.com',
    url='https://github.com/jgwill/jgtutils',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],    
    # entry_points={
    #     'console_scripts': ['jgtutr=jgtutils.cli_tlid_range:main'],
    # },
    keywords='utilities',
    project_urls={
        'Bug Reports': 'https://github.com/jgwill/jgtutils/issues',
        'Source': 'https://github.com/jgwill/jgtutils',
    },
)
