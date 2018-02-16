from setuptools import setup, find_packages

setup(name='abanalysis',
      version='1.2.2',
      packages=find_packages(), # include all packages under abanalysis
      # package_dir={'':'abanalysis'},   # tell distutils packages are under abanalysis
      description='Calculates Lift and Impact for AB Testing.',
      url='https://github.com/sarbadal/ab_analysis.git',
      author='Sarbadal Pal',
      author_email='sarbadal@gmail.com',
      license='Novus',
      # packages=['abanalysis'],
      package_data={'': ['Cluster_Data.txt','Sales_Data.txt','Cluster_Date.txt']},
      install_requires=['pandas', 'numpy', 'sklearn', 'datetime', 'scipy'], #external packages as dependencies
      include_package_data=True,
      zip_safe=False)