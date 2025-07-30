from setuptools import setup, find_packages

setup(
   name='investfiap-package-denise-vitoriano',
   version='0.1',
   packages=find_packages(),
   install_requires=[],
   author='Denise Vitoriano',
   author_email='denisevitoriano@gmail.com',
   description='Uma biblioteca para cálculos de investimentos.',
   url='https://github.com/denisevitoriano/investfiap',
   classifiers=[
       'Programming Language :: Python :: 3',
       'License :: OSI Approved :: MIT License',
       'Operating System :: OS Independent',
   ],
   python_requires='>=3.6',
)