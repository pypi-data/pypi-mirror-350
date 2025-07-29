from setuptools import setup, find_packages

setup(
    name='mshack',
    version='0.1.1',
    description='Export music score sheets to PDF',
    author='Casey Johnson',
    author_email='sharus.programmer@gmail.com',
    url='https://github.com/CaseyJohnson-RS/MSHack',
    install_requires=[
        'requests',   # Зависимости
        'selenium',
        'svglib',
        'pillow',
        'reportlab'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)