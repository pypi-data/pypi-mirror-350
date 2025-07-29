import setuptools

PACKAGE_NAME = "google-contact-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name="google-contact-local",
    version="0.0.62",  # https://pypi.org/project/google-contact-local
    author="Circles",
    author_email="valeria.e@circ.zone",
    description="PyPI Package for Circles google-contact-local Python",
    long_description="PyPI Package for Circles google-contact-local Python",
    long_description_content_type="text/markdown",
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f"{package_dir}/src"},
    package_data={package_dir: ["*.py"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "google-account-local>=0.0.11",
        "pycountry",
        "tzdata>=2024.1",
        "api-management-local>=0.0.63",
        "contact-email-address-local>=0.0.8",
        "contact-group-local>=0.0.30",
        "contact-local>=0.0.42",
        "contact-location-local>=0.0.14",
        "contact-notes-local>=0.0.33",
        "contact-persons-local>=0.0.8",
        "contact-phone-local>=0.0.12",
        "contact-profile-local>=0.0.7",
        "contact-user-external-local>=0.0.1",
        "database-mysql-local>=0.1.1",
        "importer-local>=0.0.54",
        "internet-domain-local>=0.0.8",
        "location-local>=0.0.104",
        "logger-local>=0.0.135",
        "organization-profile-local>=0.0.4",
        "organizations-local>=0.0.14",
        "python-sdk-remote>=0.0.93",
        "url-remote>=0.0.91",
        "user-context-remote>=0.0.75",
        "user-external-local>=0.0.42",
    ],
)
