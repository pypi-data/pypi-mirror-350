class Constant:
    #################App para
    app_name = ""

    def get_verbose_name(table_name, app_name=None):
        if app_name is None:
            app_name = Constant.app_name
        return app_name + "." + table_name
