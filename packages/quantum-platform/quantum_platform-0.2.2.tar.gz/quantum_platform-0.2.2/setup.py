from setuptools import setup, find_packages

setup(
    name='quantum_platform',
    version='0.2.2',
    author='Your Name',
    author_email='you@example.com',
    description='量子力学教学仿真平台（Flet + PINN）',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flet>=0.7.0',
        'matplotlib',
        'scipy',
        'numpy',
        'plotly',
        'torch',
        'scikit-image'
    ],
    entry_points={
        'gui_scripts': [
            'quantum-platform=quantum_platform.app:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
