import os

ENV = os.getenv('PAW_ENV')

if ENV == 'develop':
    from .develop import *

elif ENV == 'product':
    from .product import *

else:
    from .local import *
