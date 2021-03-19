from setuptools import setup

setup(name='frilouz',
      version='0.0.2',
      py_modules=['frilouz'],
      description='Python AST parser adapter with partial error recovery',
      long_description='''
An adaptor for AST parser like `ast.parse` and `gast.parse` which is capable of
recovering from syntax error and provide a list of syntax errors met
during parsing.''',
      author='serge-sans-paille',
      author_email='serge.guelton@telecom-bretagne.eu',
      url='https://github.com/serge-sans-paille/frilouz/',
      license="BSD-3-Clause",
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Natural Language :: English',
                   'Programming Language :: Python :: 3',
                   ],
      )
