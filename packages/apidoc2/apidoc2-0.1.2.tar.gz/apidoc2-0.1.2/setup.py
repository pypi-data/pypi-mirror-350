from setuptools import setup

setup(
    name='apidoc2',
    version='0.1.2',
    description='从Java项目批量提取ApiDoc注解并生成API文档的工具',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='meng.lv',
    author_email='meng.lv@howbuy.com',
    url='https://gitlab-code.howbuy.pa/ftx/apidoc-ext',
    py_modules=['apidoc2'],
    python_requires='>=3.6',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'apidoc2=apidoc2:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
    package_data={},
) 