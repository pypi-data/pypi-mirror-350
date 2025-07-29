from setuptools import setup, find_packages, find_namespace_packages
import os

requirements = [line.strip()
          for line in open('requirements.txt').readlines()
          if line.strip() and not line.startswith('#')]

readme = open('README.md').read()
history = open('HISTORY.md').read()
version = '0.3.0'
name= 'terrajinja-sbp-datadog'
package_path= name.replace('-', '.')

# only the cli has an entry point
entry_points=None
if name=='terrajinja-cli':
    entry_points={
      'console_scripts': [
        'tjcli = terrajinja.cli:main',
      ]
    }

setup(
    name=name,
    version=version,
    description='''Terrajinja extension for automation using cdktf''',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    url='https://gitlab/terrajinja',
    author='Terrajinja Team',
    author_email='int-terrajinja@schubergphilis.com',
    license='MIT',
    include_package_data=True,
    install_requires=requirements,
    packages=find_namespace_packages(where='src/', include=[package_path]),
    package_dir={'': 'src'},
    classifiers=[
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Natural Language :: English',
      'Programming Language :: Python :: 3.11',
    ],
    entry_points=entry_points,
)
