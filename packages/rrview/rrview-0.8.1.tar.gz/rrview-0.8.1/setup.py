from setuptools import setup, find_packages

setup(
    name="rrview",  # 包名称，PyPI上的唯一标识
    author="Fakai Wang",
    author_email="fakaiwang@sjtu.edu.cn",
    description="Ruijin Radiology Viewer is designed for examining and analyzing 3D medical images, with specialized capabilities for multimodal scenarios.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="http://ruijin-imit.cn/software/rrview",
    
    # 自动发现所有包(包括子包)
    # packages=find_packages(include=["rrview", "rrview.*"]),
    # packages=find_packages(include=["src/rrview", "src/rrview.*"]),
    packages=find_packages(where="src"),
    package_dir={"": "src"},  # 关键配置
    package_data={
        "src/view": ["src/view*"],
    },
    # 指定Python版本要求
    python_requires=">=3.6",
    
    # 安装依赖
    install_requires=[
        "requests>=2.25.1",
        "SimpleITK>=2.2.1",
        "PySide6>=6.8.0",
        "numpy==1.25.0",
        "opencv_python_headless==4.8.0.76",
        "psutil==7.0.0",
        "PySide6==6.9.0",
        "Requests==2.32.3",
        "scipy==1.15.3",
        "setuptools==68.0.0",
        "SimpleITK==2.2.1",
        "scikit-image==0.25.2",
        "nibabel==5.3.2",
    ],
    
    # 可选依赖
    extras_require={
        "dev": ["pytest>=6.0", "black>=21.0"],
    },
    
    # # 创建命令行工具
    # entry_points={
    #     "console_scripts": [
    #         "rrview=rrview.main:main_gui",
    #     ],
    # },
    
    # 包含非Python文件(如图片、数据等)
    include_package_data=True,
    
    # 分类信息
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)