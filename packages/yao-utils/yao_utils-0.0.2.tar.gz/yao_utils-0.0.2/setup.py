from setuptools import setup, find_packages

setup(
    name='yao_utils',  # 包名
    version='0.0.2',  # 版本号
    packages=find_packages(),  # 自动查找包
    install_requires=[  # 依赖项
        'uuid',
    ],
    author='Yaohoohi',  # 作者
    author_email='yaohoohi@qq.com',  # 作者邮箱
    description='我的工具包',  # 描述
    long_description=open('README.md',encoding="utf-8").read(),  # 长描述
    long_description_content_type='text/markdown',  # 长描述格式
    license='MIT',  # 许可证
)

#python setup.py sdist bdist_wheel
#twine upload dist/*