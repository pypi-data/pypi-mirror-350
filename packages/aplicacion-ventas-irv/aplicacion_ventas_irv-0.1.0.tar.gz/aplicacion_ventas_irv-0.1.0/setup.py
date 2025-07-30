from setuptools import setup, find_packages

setup(
    name='aplicacion_ventas_irv',
    version='0.1.0',
    author='Irving Rodríguez Vargas',
    author_email='irvingr@hotmail.com',
    description='Paquete para gestionar ventas, precios, impuestos y descuentos',
    long_description = open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tu_usuario/aplicacion_ventas',#CAMBIA ESTO POR TU URL DE GITHUB
    packages = find_packages(),
    install_requires = [],
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', #CAMBIA ESTO SEGUN SEA NECESARIO
        'Operating System :: OS Independent',
    ],
    python_requires = '>=3.7'
)