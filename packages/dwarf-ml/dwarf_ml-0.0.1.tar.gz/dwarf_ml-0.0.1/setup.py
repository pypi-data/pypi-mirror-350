from setuptools import setup, find_packages

# with open('README.md', encoding='utf-8') as f:
#     long_description = f.read()

setup(
    name='dwarf_ml',
    version= '0.0.1',
    description='DWARF',
    # long_description = long_description,
    # long_description_content_type='text/markdown',
    author='MAPS',
    author_email='dongguk.maps@gmail.com',
    # url='https://github.com/leecheolu/bonsai-ml.git',
    install_requires=[
        "pandas",
        ],
    packages=find_packages(exclude=[]),
    keywords=['Decision Tree','DT'],
    python_requires='>=3.7',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)