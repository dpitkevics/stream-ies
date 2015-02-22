from distutils.core import setup

setup(
    name='stream-ies',
    version='0.01',
    packages=['lib'],
    url='',
    license='',
    author='Daniels',
    author_email='',
    description='',
    install_requires=[
        'libtorrent',
        'hachoir_core',
        'hachoir_parser',
        'hachoir_metadata', 'PySide', 'ui_quitter', 'PIL'
    ]
)
