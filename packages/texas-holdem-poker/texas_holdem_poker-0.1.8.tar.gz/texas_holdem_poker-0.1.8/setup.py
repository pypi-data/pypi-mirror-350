from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='texas_holdem_poker',
    version='0.1.8',  # 版本号
    description="a command-line-interacted texas holdem poker game, also include a real-time winning-rate calculator",
    long_description=long_description,
    author='ray.ping',
    author_email='342099577@qq.com',
    url='',
    install_requires=[],
    license='MIT',
    packages=find_packages()
)
