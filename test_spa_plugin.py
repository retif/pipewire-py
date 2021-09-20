from test_spa_plugin import ffi
from test_spa_plugin import lib

@ffi.def_extern()
def spa_handle_factory_enum(factory, index):
    print(factory)
    print(index)
    return 0
