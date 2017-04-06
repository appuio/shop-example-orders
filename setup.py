from setuptools import setup

setup(
    name='shop-example-orders',
    packages=['orders'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy'
    ]
)
