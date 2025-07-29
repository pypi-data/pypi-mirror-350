from setuptools import setup, find_packages

setup(
    name="grammatical-phrase-splitter",
    version="0.2.4",
    packages=find_packages(
        include=['grammatical_phrase_splitter', 'grammatical_phrase_splitter.*']
    ),
    install_requires=[
        "openai",       
        "spacy"        
    ],
    entry_points={
        'console_scripts': [
            'split-phrase=grammatical_phrase_splitter.grammatical_phrase_splitter:main',
        ],
    },
    include_package_data=True,
    description="A package to split sentences into grammatical segments using OpenAI API",
    author="Ziwei Gu",
    author_email="ziweigu@g.harvard.edu",
    url="https://github.com/ZiweiGu/GP-TSM", 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
