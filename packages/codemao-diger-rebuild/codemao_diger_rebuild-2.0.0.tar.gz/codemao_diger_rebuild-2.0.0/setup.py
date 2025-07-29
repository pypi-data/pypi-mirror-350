#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'codemao-diger-rebuild',
        version = '2.0.0',
        description = '',
        long_description = 'codemao-diger-rebuild',
        long_description_content_type = None,
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        keywords = '',

        author = '',
        author_email = '',
        maintainer = '',
        maintainer_email = '',

        license = 'MIT License',

        url = 'https://github.com/Rov-Waff/codemao-diger-rebuild',
        project_urls = {},

        scripts = [],
        packages = [
            'codemao_diger.DBMapper',
            'codemao_diger.requester',
            'codemao_diger.requester.entity'
        ],
        namespace_packages = [],
        py_modules = ['codemao_diger.DBGenerator'],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = ['requests>=2.32'],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
