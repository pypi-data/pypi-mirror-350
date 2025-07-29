from setuptools import setup, find_packages
setup(
    name="thirteen_gpu",
    version="0.0.13",
    description="simple gpu scheduler",
    author="seil.na",
    author_email="seil.na@thirteen.ai",
    url="https://github.com/thirteen-ai/simple_gpu_scheduler",
    download_url="https://github.com/thirteen-ai/simple_gpu_scheduler/archive/master.zip",
    install_requires=["fastapi", "paramiko", "uvicorn"],
    packages=find_packages(exclude=[]),
    keywords=[],
    python_requires=">=3",
    entry_points={
        "console_scripts": [
            "submit = thirteen_gpu.submit:main",
            "delete = thirteen_gpu.delete:main",
        ]
    },
)
