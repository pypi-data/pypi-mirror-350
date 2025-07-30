from setuptools import setup, find_packages
import os

def get_version():
    version_file = os.path.join('issnresolver', 'version.py')
    with open(version_file, 'r') as f:
        exec(f.read())
    return locals()['__version__']

setup(
    name='issnresolver',
    version=get_version(),

    # Editable fields:
    description='Fast async ISSN ↔ ISSN-L resolver using the ISSN Portal API',
    long_description = open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',

    author='Akmal Setiawan',
    author_email='your@email.com',
    url='https://github.com/acepocalypse/issnresolver',
    project_urls={
        'Source': 'https://github.com/acepocalypse/issnresolver',
        'Tracker': 'https://github.com/acepocalypse/issnresolver/issues',
        'Documentation': 'https://github.com/acepocalypse/issnresolver#readme',
    },

    license='MIT',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'aiohttp>=3.8',
        'pandas>=1.3',
        'tqdm>=4.0',
    ],
    extras_require={
        "notebook": ["nest_asyncio"]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ],
)