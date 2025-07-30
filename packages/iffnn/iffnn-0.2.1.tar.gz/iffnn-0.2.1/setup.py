from setuptools import setup, find_packages

setup(
    name='iffnn',
    version='0.2.1',
    author='Miles Q. Li',
    author_email='miles.qi.li@mail.mcgill.ca',
    description='Interpretable Feedforward Neural Network Library based on Li et al.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MilesQLi/iffnn',
    project_urls={
        'Documentation': 'https://github.com/MilesQLi/iffnn#readme',
        'Source': 'https://github.com/MilesQLi/iffnn',
        'Bug Tracker': 'https://github.com/MilesQLi/iffnn/issues',
    },
    packages=find_packages(exclude=['tests*', 'examples*']),
    install_requires=[
        'torch>=1.7.0',
        'tqdm>=4.50.0',
    ],
    extras_require={
        'dev': ['pytest', 'flake8'],
        'examples': ['scikit-learn>=0.24.0'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='interpretable neural networks explainability PyTorch AI',
    python_requires='>=3.7',
)
