from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bieniciscraper',
    version='1.0.3',
    description='scrape housing listings on bien\'ici from any bien\'ici search url 💛',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='sasha bouloudnine',
    author_email='sasha.bouloudnine@lobstr.io',
    packages=find_packages(),
    install_requires=[
        'requests',
        'retry',
    ],
    entry_points={
        'console_scripts': [
            'bieniciscraper = bieniciscraper.cli:main',
        ],
    },
)
