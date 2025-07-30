from setuptools import setup

version=0.11400000000000002

setup(name='genai_utils', 
      version=str(version), 
      description='Very simple quick way to deploy Django Webservices',
      url='https://github.com/meyers007/genai_utils.git',
      author='Wan Bae, Seattle University',
      author_email='baew@seattleu.edu',
      license='Apache License 2.0',
      packages = ['genai_utils'],
      package_data={'genai_utils':['*']},
      zip_safe=False,
      install_requires=['torch'],
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',
            
          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          #'Topic :: Jupyter Prettification :: Utilities ',
      
          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: Apache Software License',
      
          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          #'Programming Language :: Python :: 2',
          #'Programming Language :: Python :: 2.6',
          #'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12'
      ],
)
