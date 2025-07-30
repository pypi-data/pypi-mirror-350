class LazyImport(object):
    def __init__(self, module_name, module_class):
        # return from module_name import module_class
        # sample - from app01.package.pkg1 import Pkg1
        # class Name must be Capitalize(P)
        self.module_name = module_name
        self.module_class = module_class
        self.module = None

    def __getattr__(self, name):
        if self.module is None:
            self.module = __import__(self.module_name, fromlist=[self.module_class])
        return getattr(self.module, name)


from .response import Response
from importlib import import_module


def dynamicImport(module_name, names=False):
    try:
        module = import_module(module_name)
        if names:
            if type(names) == list and len(names) > 0:
                import_list = names
            elif type(names) == str:
                import_list = [names]

            error_list = []
            right_list = []
            for i in import_list:
                if hasattr(module, i):
                    right_list.append(i)
                else:
                    error_list.append(i)

            if len(error_list) > 0:
                return Response(
                    False, f"{error_list} not in the package:'{module_name}'!"
                )
            else:
                if len(right_list) > 1:
                    return __import__(module_name, fromlist=right_list)
                else:
                    return getattr(module, right_list[0])
        return module
    except Exception as e:
        return Response(False, str(e))
