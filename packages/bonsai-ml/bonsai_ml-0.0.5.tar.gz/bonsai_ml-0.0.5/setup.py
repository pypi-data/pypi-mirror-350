from setuptools import setup, find_packages


setup(
    name='bonsai_ml',
    version= '0.0.5',
    description='bonsai',
    author='MAPS',
    author_email='dongguk.maps@gmail.com',
    url='https://github.com/leecheolu/bonsai-ml.git',
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