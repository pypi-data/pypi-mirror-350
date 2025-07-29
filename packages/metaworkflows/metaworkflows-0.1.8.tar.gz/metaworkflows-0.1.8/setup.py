from setuptools import setup, find_packages

setup(
    name='metaworkflows',
    version='0.1.8',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'PyYAML>=6.0',
        'pandas>=1.0.0',  # Base dependency for PythonEngine example
        'sqlalchemy>=1.4.0',  # Base dependency for DatabaseIO examples using PythonEngine
        'jsonschema==4.23.0'
    ],
    extras_require={
        'spark': ['pyspark>=3.0.0'],
        'postgres': ['psycopg2-binary>=2.9.0'],
        'gcp': ['google-cloud-storage>=2.0.0', 'google-cloud-secret-manager==2.23.0', 'pyarrow>=1.0.0'],
    },
    entry_points={
        'console_scripts': [
            'metaworkflows=metaworkflows.__main__:main',
        ],
    },
    author='tuanlxa, kiendt',
    author_email='atuabk58@mbbank.com.vn',
    description='A metadata-driven ETL framework',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers'
    ],
    python_requires='>=3.10',
)
