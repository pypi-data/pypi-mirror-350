from setuptools import setup, find_packages

setup(
    name="bugzee-client",
    version="0.1.1",
    description="Bugzee Error Monitoring client libraries",
    author="Bugzee Team",
    author_email="support@bugzee.pro",
    url="https://bugzee.pro",
    py_modules=["bugzee_django", "bugzee_odoo"],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.py'],
    },
    install_requires=[
        "requests>=2.0.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.7",
) 