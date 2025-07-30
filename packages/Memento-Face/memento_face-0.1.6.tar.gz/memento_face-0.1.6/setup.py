from setuptools import setup, find_packages

setup(
    name="Memento-Face",
    version="0.1.6",
    author="RazielMoesch",
    author_email="therazielmoesch@gmail.com",
    description="Easy to use Face Recognition and Detection models.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RazielMoesch/MementoML",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "Memento.models": ["FaceDetectionWeights.pth", "FaceRecognitionWeights.pth"],
    },
    install_requires=[
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "opencv-python",
        "Pillow",
        "matplotlib",
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)