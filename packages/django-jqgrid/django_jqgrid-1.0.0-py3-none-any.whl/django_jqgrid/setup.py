import os
from setuptools import setup, find_packages

# Read README for long description
README = ''
readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
if os.path.exists(readme_path):
    with open(readme_path, encoding='utf-8', errors='ignore') as readme:
        README = readme.read()
else:
    README = """
# Django JQGrid

A Django package for easy integration of jqGrid with automatic configuration, bulk actions, and advanced features.

## Features

- Auto-discovery and configuration of Django models
- Built-in support for CRUD operations
- Advanced filtering, searching, and sorting
- Bulk actions support
- Import/Export functionality
- Multi-database support
- Responsive grid layouts
- Customizable templates and styling

## Installation

```bash
pip install django-jqgrid
```

## Quick Start

1. Add 'django_jqgrid' to your INSTALLED_APPS
2. Include the URLconf in your project urls.py
3. Run `python manage.py migrate` to create the django_jqgrid models
4. Use the JQGridMixin in your views or the {% jqgrid %} template tag

For full documentation, visit the project repository.
"""

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-jqgrid',
    version='1.0.0',
    packages=['django_jqgrid'],
    package_dir={'django_jqgrid': '.'},
    include_package_data=True,
    license='MIT License',
    description='A Django package for easy integration of jqGrid with automatic configuration, comprehensive CRUD operations, and advanced features.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/coder-aniket/django-jqgrid',
    author='coder-aniket',
    author_email='coder.aniketp@gmail.com',
    keywords=['django', 'jqgrid', 'grid', 'data-table', 'crud', 'admin', 'interface', 'jquery', 'bootstrap'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces',
    ],
    python_requires='>=3.8',
    install_requires=[
        'Django>=3.0',
        'djangorestframework>=3.12',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-django>=4.0',
            'pytest-cov>=2.0',
            'flake8>=3.8',
            'black>=20.8b1',
            'isort>=5.0',
            'mypy>=0.900',
            'django-stubs>=1.9.0',
            'djangorestframework-stubs>=1.4.0',
            'sphinx>=4.0',
            'sphinx-rtd-theme>=1.0',
        ],
        'test': [
            'pytest>=6.0',
            'pytest-django>=4.0',
            'pytest-cov>=2.0',
            'factory-boy>=3.2',
            'faker>=8.0',
        ],
        'docs': [
            'sphinx>=4.0',
            'sphinx-rtd-theme>=1.0',
            'sphinx-autodoc-typehints>=1.12',
        ],
    },
    project_urls={
        'Documentation': 'https://django-jqgrid.readthedocs.io',
        'Source': 'https://github.com/coder-aniket/django-jqgrid',
        'Issues': 'https://github.com/coder-aniket/django-jqgrid/issues',
        'Changelog': 'https://github.com/coder-aniket/django-jqgrid/blob/main/CHANGELOG.md',
    },
)