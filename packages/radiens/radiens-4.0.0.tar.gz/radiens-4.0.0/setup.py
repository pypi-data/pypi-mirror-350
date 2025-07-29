from setuptools import find_packages, setup

metadata = {}
with open('radiens/version.py', 'r') as f:
    exec(f.read(), None, metadata)

with open('README.md', 'r') as f:
    long_description = f.read()
long_description += '\n\n'
with open('CHANGELOG.md', 'r') as f:
    long_description += f.read()

with open('requirements.txt', 'r') as f:
    _reqs = f.read().split('\n')
    install_requires = [r for r in _reqs if r]

setup(name='radiens',
      version=metadata['__version__'],
      description='provides python API to RADIENS analytics platform',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='NeuroNexus',
      author_email='dkipke@neuronexus.com',
      license='MIT',
      license_files=('LICENSE',),
      url='http://neuronexus.github.io',
      classifiers=[
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.10',
          'License :: OSI Approved :: MIT License',
      ],
      packages=find_packages(exclude=('radiens_obs', 'tests')),
      include_package_data=True,
      python_requires=">=3.10",
      install_requires=install_requires,
      entry_points={
          'console_scripts': ['radiens=radiens.cli.main:cli',
                              ]},

      )
