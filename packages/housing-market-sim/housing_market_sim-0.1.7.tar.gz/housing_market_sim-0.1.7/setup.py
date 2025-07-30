from setuptools import setup, find_packages

setup(
    name="housing_market_sim",  # 包名，上传 PyPI 的正式名称
    version="0.1.7",  # 请根据需要递增版本号
    description="基于ABM的住房过滤动态仿真模拟系统",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    author='ZhangZuo LiuXiaoge',
    author_email='lxg5880@163.com',
    url="https://github.com/yourusername/housing_market_sim",  # 可选
    packages=find_packages(),
    include_package_data=True,  # ✅ 确保 MANIFEST.in 生效
    package_data={
        "housing_market_sim": ["assets/*.png"],  # ✅ 打包图标资源
    },
    install_requires=[
        "streamlit>=1.25.0",  # 主 UI 框架
        "matplotlib>=3.7.0",  # 图表绘制
        "numpy>=1.23.0",  # 数值计算
        "mesa>=1.2.1,<2.2",  # ✅ 避免装到 3.0+
        "openai>=1.3.5",  # GPT 模型调用（你用的是新 API）
        "pandas>=1.5.3",  # （可选）数据结构操作，适用于 future 扩展
        "scipy>=1.10.0",  # 如果后续你引入优化/分布函数等
        "requests>=2.31.0",  # 如果 future 扩展要做联网请求
        "tqdm>=4.64.1",  # 如果用于进度条（建议性依赖）
    ],
    entry_points={
        "console_scripts": [
            "housing_market_sim = housing_market_sim.app:main"  # ✅ 命令行入口：app.py 中必须定义 main()
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
    python_requires='>=3.8',
)
