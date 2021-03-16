from setuptools import setup, find_packages
import os

version = '0.4.4.dev0'

tests_require = [
    'plone.app.testing>=4.2.5',
    'plone.app.robotframework']

setup(name='rer.cookieconsent',
      version=version,
      description='A cookies consent Plone solution; used for European Cookie Law by Emilia Romagna Region',  # noqa
      long_description=open('README.rst').read() + '\n' +
                       open(os.path.join('docs', 'HISTORY.rst')).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.2',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
      ],
      keywords='plone plonegov cookie-consent cookie-law cookie privacy',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.it',
      url='http://github.com/PloneGov-IT/rer.cookieconsent',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['rer'],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      install_requires=[
          'setuptools',
          'collective.jsconfiguration>=0.1.1',
          'collective.regjsonify>=0.2.0',
          'plone.api'
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
