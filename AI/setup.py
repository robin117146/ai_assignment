from setuptools import setup, find_packages

setup(
    name="IntelligentTutoringSystem",
    version="1.0.0",
    description="An Intelligent Tutoring System for Chemistry, featuring adaptive AI-based learning on topics like the periodic table, chemical bonding, and reactions.",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/your-username/IntelligentTutoringSystem",  # Replace with your GitHub repo URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask==2.1.3",
        "openai==0.27.7"
    ],
    entry_points={
        "console_scripts": [
            "its=app:app.run",  # This assumes the app.py contains the main Flask app
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
