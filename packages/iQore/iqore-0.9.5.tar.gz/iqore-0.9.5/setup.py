from setuptools import setup, find_packages

setup(
    name='iQore',
    version='0.9.5',
    description='Quantum-Classical SDK by iQore (Private)',
    author='iQore Inc.',
    author_email='team@iqore.com',
    url='https://iqore.com',
    packages=find_packages(include=['iQore', 'iQore.*']),
    include_package_data=True,
    package_data={
        '': ['pyarmor_runtime_006585/*'],
    },
    install_requires=[],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
)

