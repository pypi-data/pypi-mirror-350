from setuptools import setup, find_packages
from moapy.version import moapy_version, env

def readme():
    with open('README_en.md', encoding='utf-8') as f:
        return f.read()

def parse_pipfile(filename):
    import toml
    """Load requirements from a Pipfile."""
    with open(filename, 'r') as pipfile:
        pipfile_data = toml.load(pipfile)

    requirements = {
        'full': []
    }
    for package, details in pipfile_data.get('packages', {}).items():
        if isinstance(details, dict):
            requirements['full'].append(f"{package}")
            # requirements['full'].append(f"{details['git']}#egg={package}")
        elif '*' not in details:
            requirements['full'].append(f"{package}=={details}")
        else:
            # Handle the case where details are just a version string
            requirements['full'].append(f"{package}")

    return requirements

def get_environment_version(base_version, env):
    # if env == 'ST':
    #     return f"{base_version}-st"
    # elif env == 'PR':
    #     return f"{base_version}-pr"
    return base_version

print("Resolved version:", get_environment_version(moapy_version, env))

setup(
    name='moapy',
    version=get_environment_version(moapy_version, env),
    packages=find_packages(),
    include_package_data=True,
    description='Midas Open API for Python',
    long_description=readme(),
    long_description_content_type='text/markdown',
    license='MIT',
    author='bschoi',
    url='https://github.com/MIDASIT-Co-Ltd/engineers-api-python',
    install_requires=['mdutils', "numpy", "matplotlib"],
    extras_require=parse_pipfile('Pipfile'),
)