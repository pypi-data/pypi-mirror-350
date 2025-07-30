from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='akshatprime',
  version='0.0.1',
  description='Identifying a prime number',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Akshat Gupta',
  author_email='akshatg@iitbhilai.ac.in',
  license='MIT', 
  classifiers=classifiers,
  keywords='prime', 
  packages=find_packages(),
  install_requires=[''] 
)
