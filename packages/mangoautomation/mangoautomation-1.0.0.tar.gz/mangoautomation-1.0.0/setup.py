from setuptools import setup, find_packages

__version__ = '1.0.0'

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='mangoautomation',
    version=__version__,
    description='测试工具',
    long_description=long_description,
    package_data={ },
    author='毛鹏',
    author_email='729164035@qq.com',
    url='https://gitee.com/mao-peng/testkit',
    packages=find_packages(),
    install_requires=[
        'setuptools==68.2.0',
        'pydantic==2.9.2',
        'playwright==1.43.0',
        'uiautomation==2.0.20',
        'uiautomator2==3.2.5',
        'mangotools==1.0.1',
        'adbutils~=2.8.9',

    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ]
)

"""


python -m pip install --upgrade setuptools wheel
python -m pip install --upgrade twine

python setup.py check
python setup.py sdist bdist_wheel
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

"""
