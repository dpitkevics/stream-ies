from distutils.core import setup

setup(
    name='stream-ies',
    version='0.01',
    packages=['', 'lib', 'adapters', 'widgets', 'windows'],
    url='',
    license='',
    author='Daniels',
    author_email='',
    description='',
    install_requires=[
        'libtorrent',
        'hachoir_core',
        'hachoir_parser',
        'hachoir_metadata',
        'PySide',
        'ui_quitter',
        'Pillow',
        'requests',
        'pyfscache',
        'beautifulsoup4',
        'phonon'
    ],
    data_files=[
        ('phonon_backend', [
            'C:\Python27\Lib\site-packages\PyQt4\plugins\phonon_backend\phonon_ds94.dll'
        ])
    ]
)
