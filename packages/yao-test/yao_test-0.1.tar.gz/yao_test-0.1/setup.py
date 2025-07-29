from setuptools import setup, find_packages

setup(
    name='yao_test',  # 包名
    version='0.1',  # 版本号
    packages=find_packages(),  # 自动查找包
    install_requires=[  # 依赖项
        'pandas',
    ],
    author='Yaohoohi',  # 作者
    author_email='yaohoohi@qq.com',  # 作者邮箱
    description='one test',  # 描述
    long_description=open('README.md').read(),  # 长描述
    long_description_content_type='text/markdown',  # 长描述格式
    url='https://github.com/yourusername/my_package',  # 项目地址
    license='MIT',  # 许可证
)
