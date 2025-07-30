import pandas as pd
from django.conf import settings
from rich import print
from rich.console import Console
from .runOracle import RunOracle

console = Console()

DATABASES = settings.DATABASES
DATABASES_APPS_MAPPING = settings.DATABASES_APPS_MAPPING


class DatabaseAppsRouter:
    def db_for_read(self, model, **hints):
        app_label = (
            model._meta.app_label
            if not "." in (a := model._meta.verbose_name)
            else a.split(".")[0]
        )
        if app_label in DATABASES_APPS_MAPPING:
            return DATABASES_APPS_MAPPING[app_label]
        return None

    def db_for_write(self, model, **hints):
        app_label = (
            model._meta.app_label
            if not "." in (a := model._meta.verbose_name)
            else a.split(".")[0]
        )
        if app_label in DATABASES_APPS_MAPPING:
            return DATABASES_APPS_MAPPING[app_label]
        return None

    def allow_relation(self, obj1, obj2, **hints):
        obj1_app_label = (
            obj1._meta.app_label
            if not "." in (a := obj1._meta.verbose_name)
            else a.split(".")[0]
        )
        obj2_app_label = (
            obj2._meta.app_label
            if not "." in (a := obj2._meta.verbose_name)
            else a.split(".")[0]
        )
        db_obj1 = DATABASES_APPS_MAPPING.get(obj1_app_label)
        db_obj2 = DATABASES_APPS_MAPPING.get(obj2_app_label)
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            else:
                return False
        return None

    def db_for_migrate(self, db, app_label, model_name=None, **hints):
        if db in DATABASES_APPS_MAPPING.values():
            return DATABASES_APPS_MAPPING.get(app_label) == db
        elif app_label in DATABASES_APPS_MAPPING:
            return False
        return None


class DBConfig:
    def __init__(self, tns_config, sqlStr):
        self.tns_config = tns_config
        self.sqlStr = sqlStr
        self.initDBConfig()
        pass

    def updateDBs(self, data):
        db_list = (
            pd.DataFrame(data)
            .groupby(["ENGINE_NAME", "ENGINE_CONTENT"])
            .apply(lambda x: x.to_dict("records"))
            .to_frame("MAPPING")
            .reset_index(drop=False)
            .to_dict("records")
        )

        if db_list:
            # print("=" * 100)
            console.rule()
            for i_index, i in enumerate(db_list):
                # update DATABASES
                DATABASES[i.get("ENGINE_NAME")] = eval(i.get("ENGINE_CONTENT"))
                print(
                    i_index,
                    " [bold blue]DATABASES Add [bold green]Success",
                    "=======> ",
                    '"' + str(i.get("ENGINE_NAME")) + '"',
                    ":",
                    i.get("ENGINE_CONTENT"),
                )
                if i["MAPPING"]:
                    for n_index, n in enumerate(i["MAPPING"]):
                        DATABASES_APPS_MAPPING[n.get("VERBOSE_ENGINE_NAME")] = i.get(
                            "ENGINE_NAME"
                        )
                        print(
                            "      ",
                            n_index,
                            "[bold blue]Mapping Add [bold green]Success",
                            "===> ",
                            '"' + str(n.get("VERBOSE_ENGINE_NAME")) + '"',
                            ":",
                            '"' + str(i.get("ENGINE_NAME")) + '"',
                        )
                        # print("=" * 100)
                        console.rule()
            if not DATABASES.get("default"):
                DATABASES["default"] = {}
                DATABASES_APPS_MAPPING["default"] = "default"
        else:
            # print("=" * 10)
            console.rule()
            print("no database list found - by dbconfig")
            # print("=" * 10)
            console.rule()
        pass

    def initDBConfig(self):
        data = RunOracle(self.tns_config).runSql(self.sqlStr)

        if data:
            self.updateDBs(data)

        else:
            # print("=" * 80)
            console.rule()
            print("=====> no project detail found - by dbconfig")
            # print("=" * 80)
            console.rule()
