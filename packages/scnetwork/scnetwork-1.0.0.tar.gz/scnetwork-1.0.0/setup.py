from setuptools import setup, find_packages
package_name = 'scnetwork'
version = '1.0.0'
setup(
    name=package_name,
    version=version,
    author='SAPIENS TECHNOLOGY',
    packages=find_packages(),
    install_requires=[
        'torch-xla==2.7.0',
        'torch==2.4.1',
        'tiktoken==0.4.0',
        'numpy==1.25.2',
        'ijson==3.3.0',
        'psutil==7.0.0',
        'semantic-comparison-network==1.0.3',
        'hurnet==1.0.7',
        'requests==2.31.0',
        'tqdm==4.67.1'
    ],
    url='https://github.com/',
    license='Proprietary Software'
)
