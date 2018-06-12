from setuptools import setup, find_packages


setup(
    name='inverted_index',
    version='0.1',
    url='https://github.com/crolfe/inverted-index-py',
    author='Colin Rolfe',
    license='MIT',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    install_requires=[
      'Flask==0.12.2',
    ]
)
