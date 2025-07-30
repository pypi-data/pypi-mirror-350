from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
		name="wiim",
		version="0.0.2a17",
		author="Linkplay",
		author_email="tao.jiang@linkplay.com",
		description="A small package to work with wiim",
		url="https://github.com/WiimHome/python-wiim",
		package_dir={"": "src"},
		packages=find_packages(where="src"),
		include_package_data=True,
		classifiers=[
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
		]
	)
