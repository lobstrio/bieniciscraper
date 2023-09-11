from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bieniciscraper',
    version='1.1.3',
    description='scrape housing listings on bien\'ici from any bien\'ici search url 💛',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/lobstrio/bieniciscraper',
    author='sasha bouloudnine',
    author_email='sasha.bouloudnine@lobstr.io',
    packages=find_packages(),
    py_modules=['main'],
    install_requires=[
        'requests',
        'retry',
    ],
    entry_points={
        'console_scripts': [
            'bieniciscraper = main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
