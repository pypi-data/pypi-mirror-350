from setuptools import setup, find_packages

setup(
    name='show-dt',
    version= '0.0.1',
    description='show decisiontree',
    # long_description = long_description,
    # long_description_content_type='text/markdown',
    author='MAPS',
    author_email='dongguk.maps@gmail.com',
    # url='',
    install_requires=[
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