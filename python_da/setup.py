from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt', 'r') as req_file:
        return [line.strip() for line in req_file if line and not line.startswith('#')]

found_packages = find_packages(include=['dq_checks*', 'data_prep*', 'azure_package*'])
print("Found packages:", found_packages)
setup(
    name='python_da',
    version='0.1',
    packages=found_packages,
    install_requires=read_requirements(),
)
