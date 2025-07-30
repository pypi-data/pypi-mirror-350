from setuptools import setup, find_packages

setup(
    name='housing-market-sim',
    version='0.1.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit>=1.0",
        "mesa",
        "openai",
        "matplotlib",
        "numpy"
    ],
    entry_points={
        'console_scripts': [
            'housing-market-sim = housing_market_sim.app:main'
        ],
    },
    author='ZhangZuo LiuXiaoge',
    author_email='lxg5880@163.com',
    description='基于ABM的住房过滤动态仿真模拟系统',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/your_account/housing-market-sim',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
    python_requires='>=3.7'
)