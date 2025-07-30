from setuptools import setup, find_packages

setup(
    name='svo-chunker',
    version='0.1.0',
    description='Semantic text chunking based on SVO triplets and vector proximity',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/maverikod/vvz-svo-chunker',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'langdetect',
        'spacy',
        'stanza',
        'natasha',
        'numpy',
        'scipy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: Russian',
        'Natural Language :: English',
    ],
    python_requires='>=3.7',
) 