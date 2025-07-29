from setuptools import setup, find_packages
package_name = 'scnetwork'
version = '1.0.3'
from platform import system, machine
extras = []
if system().lower().strip() != 'darwin' or machine().lower().strip() != 'arm64': extras.append('torch-xla')
setup(
    name=package_name,
    version=version,
    author='SAPIENS TECHNOLOGY',
    packages=find_packages(),
    install_requires=['tqdm', 'requests', 'hurnet', 'semantic-comparison-network', 'psutil', 'ijson', 'tiktoken', 'torch', 'numpy']+extras,
    url='https://github.com/',
    license='Proprietary Software'
)
