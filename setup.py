from setuptools import find_packages, setup

setup(
    name='prioritydecorators',
    packages=find_packages(include=['prioritydecorators']),
    version='0.1.0',
    description='Library for adding/removing multiple decorators to a method with priorities',
    author='Maxim Gorbach',
    install_requires=['sortedcontainers==2.4.0'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.4.0'],
    license='MIT',
)