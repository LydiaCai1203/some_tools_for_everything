import os

ENV = os.getenv('JD_ENV')

if ENV == 'PRODUCT':
    from .product import *
elif ENV == 'DEVELOP':
    from .develop import *
else:
    from .local import *