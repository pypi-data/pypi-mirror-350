import os
import re
import shutil
import sys

from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 9)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================

This version of Ardhi Framework requires Python {}.{}, but you're trying
to install it on Python {}.{}.

This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:

    $ python -m pip install --upgrade pip setuptools
    $ python -m pip install ardhi-framework

This will install the latest version of Ardhi Framework which works on
your version of Python. If you can't upgrade your pip (or Python), request
an older version of Ardhi Framework:

    $ python -m pip install "ardhi-framework<3.10"
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)


def read(f):
    with open(f, encoding='utf-8') as file:
        return file.read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('ardhi_framework')


if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    if os.system("twine check dist/*"):
        print("twine check failed. Packages might be outdated.")
        print("Try using `pip install -U twine wheel`.\nExiting.")
        sys.exit()
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('ardhi_framework.egg-info')
    sys.exit()


setup(
    name='ardhi_framework',
    version=version,
    url='https://www.ardhisasa.go.ke/',
    license='MIT',
    description='Ardhi Framework for land transactions.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Vincent Kioko',
    author_email='kiokovincent12@gmail.com',  # SEE NOTE BELOW (*)
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django>=3.2",
        "djangorestframework>=3.0",
        "PyJWT"
    ],
    dependencies=[
        "Django>=3.2,<5.0",
        "djangorestframework>=3.12,<4.0",
        "PyJWT"
    ],
    python_requires=">=3.9",
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Framework :: Django :: 5.1',
        'Framework :: Django :: 5.2',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
    ],
    project_urls={
        'Funding': 'https://wearefreeopen/',
        'Source': 'https://gitlab.com/ardhisasa/ardhi-framework',
        'Changelog': 'https://no-changelog-yet.com',
    },
)
