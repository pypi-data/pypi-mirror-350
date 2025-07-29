from setuptools import setup, find_packages

setup(
    name='udp-file-transfer',
    version='0.0.1',
    author='Guangye Bai',
    author_email='2253637@tongji.edu.cn',
    description='An academic experiment package',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://pypi.org/project/udp-file-transfer/',
    packages=find_packages(),
    license='MIT',
    keywords=['udp', 'transfer', 'experiment', 'typosquatting', 'security'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
    ],
    python_requires='>=3.6',
    install_requires=[]
)
