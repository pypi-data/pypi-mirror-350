from setuptools import setup, find_packages
package_name = 'scnetwork'
version = '1.0.2'
setup(
    name=package_name,
    version=version,
    author='SAPIENS TECHNOLOGY',
    packages=find_packages(),
    install_requires=['tqdm', 'requests', 'hurnet', 'semantic-comparison-network', 'psutil', 'ijson', 'tiktoken', 'torch', 'torch-xla', 'numpy'],
    url='https://github.com/',
    license='Proprietary Software'
)
