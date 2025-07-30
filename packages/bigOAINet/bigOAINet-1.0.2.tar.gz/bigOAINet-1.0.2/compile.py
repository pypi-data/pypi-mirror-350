from setuptools import setup, find_packages

# 如果是在虚拟环境中，必须先激活对应的环境，再执行下面的命令，否则无效
# python compile.py develop
setup(
    name="bigOAINet",
    version="1.0.0",
    description="bigO AI Network",
    author="jerry1979",
    author_email="6018421@qq.com",
    url="http://www.xtbeiyi.com/",
    packages=find_packages(),
)
