from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bonsai_ml',
    version= '0.0.7',
    description='bonsai',
    long_description = long_description,
    long_description_content_type='text/markdown',
    author='MAPS',
    author_email='dongguk.maps@gmail.com',
    url='https://github.com/bonsai-tree-model/bonsai',
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "docplex",
        "psutil"
        ],
    packages=find_packages(exclude=[]),
    keywords=['Decision Tree','DT'],
    python_requires='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)