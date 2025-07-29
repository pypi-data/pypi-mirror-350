import setuptools

PACAKGE_NAME = "sql-to-code-local"  # TODO sql2code-local?
package_dir = PACAKGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACAKGE_NAME,  # https://pypi.org/project/sql-to-code-local
    version='0.0.35',  # update each time
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles sql-to-code-local Local Python",
    long_description="PyPI Package for Circles sql-to-code-local Local Python",
    long_description_content_type='text/markdown',
    url="https://github.com/circles-zone/sql2code-local-python-package",

    # old
    # packages=[package_dir],
    # package_dir={package_dir: f'{package_dir}/src'},
    # package_data={package_dir: ['*.py']},

    # new
    packages=setuptools.find_packages(),

    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "logger-local>=0.0.71",  # https://pypi.org/project/logger-local/
        # TODO >= 0.1.1
        "database-mysql-local==0.0.459",  # https://pypi.org/project/database-infrastructure-local/
    ]
)
