import codecs

import setuptools

with codecs.open("README.rst", encoding='utf8') as fh:
    long_description = fh.read()
    
    
with open('version.txt', 'r') as f:
    current_version = f.read().strip()

# Split the current version into its components
version_parts = current_version.split('.')
major, minor, patch = map(int, version_parts)

# Increment the patch version
patch += 1

# Construct the new version string
new_version = f"{major}.{minor}.{patch}"

# Write the new version number back to the file
with open('version.txt', 'w') as f:
    f.write(new_version)

 

setuptools.setup(name='searchlogit',
                 version=new_version,
                 description='Extensions for a Python package for \
                              GPU-accelerated estimation of mixed logit models.',
                 long_description=long_description,
                 long_description_content_type="text/x-rst",
                 url='https://github.com/RyanJafefKelly/searchlogit',
                 author='Ryan Kelly, Prithvi Beeramoole, Zeke Ahern, Alban Pinz, Robert Burdett and Alexander Paz',
                 author_email='pritvi.beeramole@qut.edu.au, z.ahern@qut.edu.au',
                 license='MIT',
                 packages=['searchlogit'],
                 zip_safe=False,
                 python_requires='>=3.5',
                 install_requires=[
                     'numpy>=1.13.1',
                     'scipy>=1.0.0'
                 ])
