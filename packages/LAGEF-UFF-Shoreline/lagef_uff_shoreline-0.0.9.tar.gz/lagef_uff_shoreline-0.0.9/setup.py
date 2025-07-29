from setuptools import setup

with open('README.md','r') as arq:
    readme = arq.read()

setup(name='LAGEF-UFF-Shoreline',
    version='0.0.9',
    license='MIT License',
    author='Pablo Simoes',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email=['pablosergio.simoes@gmail.com','pablosimoes@id.uff.br'],
    keywords=['lagef uff','linha de costa','shoreline','google earth engine'],
    description=u'Scripts para análise de linha de costa - Lagef UFF - projeto IVC',
    packages=['LAGEF_UFF'],
    install_requires=['pandas','geemap','numpy','earthengine-api','scikit-image','matplotlib'],)







