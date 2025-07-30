from setuptools import setup, find_packages

setup(
    name="mpalp",  # 패키지 이름 (pip install 시 사용될 이름)
    version="0.1.4",    # 버전
    packages=find_packages(),  # textbasic 폴더 내 모든 패키지 포함
    include_package_data=True,  # 이 설정을 통해 패키지 내 데이터 파일을 포함시킬 수 있음
    package_data={
    },
    install_requires=[ # 패키지 설치 시 같이 설치되도록 설정
        "torch==2.7.0",
        "torchaudio==2.7.0",
        "torchvision==0.22.0",
        "pandas==2.2.3",
        "psutil==7.0.0",
        "tqdm==4.67.1"
    ],
    # install_requires=[
	#    "pandas>=1.3.0,<2.0.0",  # 버전 범위 설정 방법
	# ],
    author="Kimyh",
    author_email="kim_yh663927@naver.com",
    description="Multi-Purpose AI Learning Package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/Kim-YoonHyun/my_package",  # 깃허브 주소 등
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",  # 최소 지원할 파이썬 버전
)