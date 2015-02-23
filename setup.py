from setuptools import setup

setup(
    name='stream-ies',
    version='0.01',
    packages=['', 'lib', 'adapters', 'widgets', 'windows', 'cache', 'temp', 'resources'],
    url='',
    license='',
    author='Daniels',
    author_email='',
    description='',
    install_requires=[
        #'libtorrent',
        'hachoir_core',
        'hachoir_parser',
        'hachoir_metadata',
        'PySide',
        'Pillow',
        'requests',
        'pyfscache',
        'beautifulsoup4',
        'phonon'
    ],
    data_files=[
        ('phonon_backend', [
            'C:\Python27\Lib\site-packages\PySide\plugins\phonon_backend\phonon_ds94.dll'
        ])
    ]
)
