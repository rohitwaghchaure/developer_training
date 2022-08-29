from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in developer_training/__init__.py
from developer_training import __version__ as version

setup(
	name="developer_training",
	version=version,
	description="Developer Training",
	author="Frappe",
	author_email="support@frappe.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
