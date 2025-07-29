from setuptools import setup, find_packages

setup(
    name="django_post_api",  # 包名
    version="1.1.0",  # 版本号
    author="songhaoi",  # 作者
    author_email="songhao2020@hotmail.com",  # 作者邮箱
    description="Django Post API",  # 简短描述
    long_description=open("README.md").read(),  # 从 README.md 读取长描述
    long_description_content_type="text/markdown",  # 长描述格式
    url="https://gitee.com/songhaoi/django-api",  # 项目主页
    packages=find_packages(),  # 自动查找所有包和子包
    include_package_data=True,  # 包含非 Python 文件
    install_requires=[  # 依赖列表
        "Django>=4.2",
        "requests>=2.32.3"
    ],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',  # Python 版本要求
)
