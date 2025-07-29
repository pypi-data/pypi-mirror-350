# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sbdh_ubl_data',
 'sbdh_ubl_data.sbdh',
 'sbdh_ubl_data.ubl',
 'sbdh_ubl_data.ubl.common',
 'sbdh_ubl_data.ubl.maindoc']

package_data = \
{'': ['*']}

install_requires = \
['xsdata>=25.4,<26.0']

setup_kwargs = {
    'name': 'sbdh-ubl-data',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Anders Lehn Reed',
    'author_email': 'anders.lehn.reed@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
