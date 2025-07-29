from setuptools import setup, find_packages

setup(
    name='mi-paquete',
    version='0.1.0',
    description='Descripción corta de tu paquete',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tu Nombre',
    author_email='tu@email.com',
    license='MIT',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.8',
    include_package_data=True,
)