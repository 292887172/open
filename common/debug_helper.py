from model.center.api import Api

__author__ = 'sunshine'


def get_debug_api():
    """
    获取需要测试的api
    :return:
    """
    api = Api.objects.filter()
    items = []
    for a in api:
        item = dict()
        item['api_url'] = a.api_url
        item['api_request_type'] = a.api_request_type.upper()
        item['api_params'] = a.api_params
        item['api_name'] = a.api_name
        item['api_doc_url'] = a.api_doc_url
        items.append(item)
    return items
