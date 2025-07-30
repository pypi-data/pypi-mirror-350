from .constant import Constant
from .response import Response
from django.apps import apps
from copy import deepcopy
from django.db.models import Q  # 不要拿掉
from jsonpath import jsonpath
from django.core.paginator import Paginator


class HandleData(Constant):
    def get_(self, table_name, conditions={}, page_size=None, current_page=None, sort=[]):
        # table_name = kwargs.get("table_name")
        # condition = {} if not kwargs.get("condition")
        name_type = "db_table" if not "." in table_name else "verbose_name"

        if len(list(conditions.keys())) == 0:
            conditions = {"data": [{}]}

        if "data" not in list(conditions.keys()):
            conditions = {"data": [conditions]}

        condition = strConditions(formatConditions(conditions))

        for model in apps.get_models():
            if model._meta.app_label == self.app_name:
                if model._meta.__getattribute__(name_type) == table_name:
                    models = model.objects.filter(eval(condition))
                    qs = models.all().values()
                    if len(sort) > 0:
                        qs = qs.order_by(*sort)
                    if page_size == None:
                        return Response(data=formatJson(list(qs)))
                    else:
                        # 创建Paginator对象并指定每页显示的记录数量
                        paginator = Paginator(list(qs), per_page=page_size)
                        page = paginator.get_page(current_page)

                        return Response(
                            data=formatJson(list(page.object_list)),
                            page={
                                "total_count": paginator.count,
                                "num_pages": paginator.num_pages,
                                "current_page": page.number,
                            },
                        )

        return Response(False, "table is not found!", [])

    # {
    #   "action":"insert",
    #   "table_name":"TBL_USER",
    #   "data":[
    #     { user_name:"d1"},
    #     { user_name:"d2"},
    #     { user_name:"d3"}
    #   ]
    # }
    def handle_(self, table_name, obj):
        action = obj.get("action")
        data = list(obj.get("data"))

        name_type = "db_table" if not "." in table_name else "verbose_name"
        for model in apps.get_models():
            if model._meta.app_label == self.app_name and model._meta.__getattribute__(name_type) == table_name:
                list_data = []
                if action == "insert":
                    for item in data:
                        if "id" in item:
                            del item["id"]
                        result = model.objects.create(**item)
                        list_data.append(to_dict(result))
                    return Response(data=formatJson(list_data))
                elif action == "delete":
                    for item in data:
                        item = strConditions(formatConditions(item, [], "node"))
                        result = model.objects.filter(eval(item)).delete()
                    return Response(data=formatJson(list_data))
                elif action == "modify":
                    for item in data:
                        id = item.get("id")
                        clone_item = deepcopy(item)
                        del clone_item["id"]
                        model.objects.filter(id=id).update(**clone_item)
                        result = model.objects.get(id=id)
                        list_data.append(to_dict(result))
                    return Response(data=formatJson(list_data))
                else:
                    return Response(False, "no action", [])

        # handleData(para)
        return Response(False, "table is not found!", [])


def to_dict(self, fields=None, exclude=None):
    from django.db.models.fields import DateTimeField
    from django.db.models.fields.related import ManyToManyField

    data = {}
    for f in self._meta.concrete_fields + self._meta.many_to_many:
        value = f.value_from_object(self)

        if fields and f.name not in fields:
            continue

        if exclude and f.name in exclude:
            continue

        if isinstance(f, ManyToManyField):
            value = [i.id for i in value] if self.pk else None

        # if isinstance(f, DateTimeField):
        #     value = value.strftime("%Y-%m-%d %H:%M:%S") if value else None

        data[f.name] = value

    return data


def addCreateModifyDate(obj, type="ymd"):
    import datetime

    # import django.utils.timezone as timezone

    # print(datetime.datetime.now())
    # print(datetime.datetime.now().strftime("%d-%b-%y %I:%M:%S.%f %p +8:00"))
    # print(datetime.datetime.utcnow())
    # print(timezone.now())

    action = obj.get("action")
    data = obj.get("data")

    for item in data:
        if action == "insert":
            item["create_date"] = (
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if type == "ymd"
                else datetime.datetime.now().strftime("%d-%b-%y %I:%M:%S.%f %p +8:00")
            )
        elif action == "modify":
            item["modify_date"] = (
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if type == "ymd"
                else datetime.datetime.now().strftime("%d-%b-%y %I:%M:%S.%f %p +8:00")
            )
    return obj


"""
jsonStr, formatList=["$.data[*]", "$.data2[*]"], model="jsonpath"
{
    "data": [
                {"id": 4},
                {"id": {"type": "__range", "value": "(4,6)"}}
            ],
    "data2": [
                {"id": 1},
                {"id": {"type": "__range", "value": "(2,3)"}}
            ]
}
"""

"""
jsonStr, formatList=["name", "id"], model="node"
{
    "id": {"type": "__range", "value": "(4,6)"},
    "name": "Component 1",
    "status": {"type": "__isnull", "value": false }
}
"""


class BeautyCondition:
    pass


def formatC(jsonStr):
    c = {}
    for k, v in jsonStr.items():
        c[k] = {"type": "__in", "value": v} if type(v) == list else v
    return {"data": [c]}


def formatConditions(jsonStr, formatList=["$.data[*]"], model="jsonpath"):
    condition_list = []
    if model == "node":
        if formatList == ["$.data[*]"] or len(formatList) == 0:
            formatList = list(jsonStr.keys())
        condition = {}
        for k, v in jsonStr.items():
            if k in formatList:
                if type(v) == (dict or object):
                    if v.get("type") == "__range":
                        value = eval(v.get("value"))
                    else:
                        value = v.get("value")

                    condition[k + v.get("type")] = value
                else:
                    condition[k] = v
        condition_list.append(condition)
    elif model == "jsonpath":
        for i in formatList:
            for j in jsonpath(jsonStr, i):
                condition = {}
                for k, v in j.items():
                    if type(v) == (dict or object):
                        if v.get("type") == "__range":
                            value = eval(v.get("value"))
                        else:
                            value = v.get("value")

                        condition[k + v.get("type")] = value
                    else:
                        condition[k] = v
                condition_list.append(condition)
    return condition_list


def strConditions(conditions):
    return " | ".join(map(str, [f"Q(**{i})" for i in conditions]))


def formatJson(data: list):
    import pandas as pd

    if len(data) > 0:
        df = pd.DataFrame(data)
        for col in df.columns:
            try:
                df.loc[:, col] = df.apply(lambda x: eval(x[col]), axis=1)
            except Exception as e:
                pass
        return df.to_dict("records")
    else:
        return data
