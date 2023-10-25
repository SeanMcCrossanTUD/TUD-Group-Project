from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt', 'r') as req_file:
        return [line.strip() for line in req_file if line.strip() and not line.startswith('#')]

found_packages = find_packages(include=['dq_checks*', 'data_prep*', 'azure_package*', 'rds_sql_package*'])

setup(
    name='python_da',
    version='0.1',
    packages=found_packages,
    install_requires=read_requirements(),
    description='Profiles your data quality issues and cleans your data.',
    author='Sean McCrossan',
    author_email='mccrosss@tcd.ie', 
    url='https://github.com/SeanMcCrossanTUD/TUD-Group-Project/python_da',
    classifiers=[
        'Development Status :: MVP',
        'Intended Audience :: Data Scientist',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
)
