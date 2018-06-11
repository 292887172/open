# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import os
import sys
import datetime

import django
from django.core.paginator import Paginator
from ebcloudstore.client import EbStore
import requests

from base.convert import date2ymdhms
from conf.commonconf import CLOUD_TOKEN
from conf.docconfig import DOC_TPL_PATH
from util.jsonutil import MyEncoder


sys.path.append(os.path.join(os.path.dirname('.'), '..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'open.settings'
django.setup()
from model.center.doc import Doc
from model.center.doc_menu import DocMenu
from model.center.api import Api
from model.center.device_menu import DeviceMenu

def save_device_menu(menu_data):
    device_menu = DeviceMenu.objects.all()
    store_device = EbStore(CLOUD_TOKEN)
    file_name_device = "menu-{0}.js".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    store_device.upload(json.dumps(device_menu,cls=MyEncoder).encode("utf-8"),file_name_device,"application/javascript")
    DeviceMenu.objects.all().delete()
    try:
        for menu in menu_data:

            # 保存一级菜单
            DeviceMenu(device_menu_id=menu["id"], menu_name=menu["title"], menu_url=menu["url"],
                       device_key=menu["ordernum"],device_type=menu["sort"],create_time=datetime.datetime.now(),update_time=datetime.datetime.now()).save()
        pass
        return True
    except Exception as e:
        print(str(e))
        logging.getLogger("").info(str(e))
        return False


def execute_menu(menu_arr):
    """
    处理菜单数据：
    1、先删除数据库之前的全部数据（删除前保存一份到云存储中）
    2、从上往下逐个保存
    :param menu_arr:
    :return:
    """
    doc_menu = DocMenu.objects.all()
    store = EbStore(CLOUD_TOKEN)
    file_name = "menu-{0}.js".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    store.upload(json.dumps(doc_menu, cls=MyEncoder).encode("utf-8"), file_name, "application/javascript")
    DocMenu.objects.all().delete()

    try:
        for menu in menu_arr:
            if len(menu["nodes"]) == 0:
                dm_is_parent = 0
            else:
                dm_is_parent = 1
            # 保存一级菜单
            DocMenu(dm_id=menu["id"], dm_name=menu["title"], dm_is_parent=dm_is_parent, dm_url=menu["url"], dm_depth=1,
                    dm_order_num=menu["ordernum"], dm_parent_id=0).save()
            # 保存二级菜单
            for i in menu["nodes"]:
                DocMenu(dm_id=i["id"], dm_name=i["title"], dm_is_parent=0, dm_url=i["url"], dm_depth=2,
                        dm_order_num=i["ordernum"], dm_parent_id=menu["id"]).save()
                pass
            pass
        pass
        return True
    except Exception as e:
        print(str(e))
        logging.getLogger("").info(str(e))
        return False


def create_doc_menu(dm_name,
                    dm_doc_id,
                    dm_is_parent,
                    dm_url,
                    dm_order_num,
                    dm_depth,
                    dm_parent_id,
                    dm_class):
    """
    新建菜单项
    :param dm_name:
    :param dm_doc_id:
    :param dm_is_parent:
    :param dm_url:
    :param dm_order_num:
    :param dm_parent_id:
    :param dm_class:
    :return:
    """

    doc_foriegnkey = Doc.objects.filter(doc_id=dm_doc_id)

    try:
        create_line = DocMenu.objects.get_or_create(dm_name=dm_name,
                                                    dm_doc_id=doc_foriegnkey,
                                                    dm_is_parent=dm_is_parent,
                                                    dm_url=dm_url,
                                                    dm_order_num=dm_order_num,
                                                    dm_depth=dm_depth,
                                                    dm_parent_id=dm_parent_id,
                                                    dm_class=dm_class
                                                    )
        return True
    except Exception as e:
        logging.getLogger('').error(e)
        return False


def update_doc_menu(dm_id, dm_doc_name, dm_doc_id, dm_is_parent, dm_url, dm_order_num, dm_depth, dm_parent_id,
                    dm_class):
    """
    更新菜单项信息

    :param dm_id:
    :param dm_doc_name:
    :param dm_doc_id:
    :param dm_is_parent:
    :param dm_url:
    :param dm_order_num:
    :param dm_depth:
    :param dm_parent_id:
    :param dm_class:
    :return:
    """
    try:
        update_line = DocMenu.objects.filter(dm_id=dm_id).update(
            dm_doc_id=Doc.objects.get_or_create(dm_doc_id),
            dm_doc_name=dm_doc_name,
            dm_is_parent=dm_is_parent,
            dm_url=dm_url,
            dm_order_num=dm_order_num,
            dm_depth=dm_depth,
            dm_parent_id=dm_parent_id,
            dm_class=dm_class
        )
        if update_line > 0:
            return True
        else:
            return False

    except Exception as e:
        logging.getLogger("").error(e)
        return False


def create_sub_menu(parent_dm_id, dm_name, dm_doc_id, dm_url, dm_order_num, dm_class
                    ):
    """
    创建子菜单
    :param parent_dm_id:
    :param dm_name:
    :param dm_doc_id:
    :param dm_url:
    :param dm_order_num:
    :param dm_class:
    :return:
    """

    create_doc_menu(
        dm_name=dm_name, dm_doc_id=dm_doc_id, dm_is_parent=0, dm_url=dm_url, dm_order_num=dm_order_num, dm_depth=0,
        dm_parent_id=parent_dm_id, dm_class=dm_class
    )


def fetch_menu_info(dm_id):
    info = {
        'pMenu': [],
        'sMenu': [],
    }
    pMenu = info['pMenu']
    sMenu = info['sMenu']

    try:
        dm = DocMenu.objects.filter(dm_id=dm_id).get()
        if dm.dm_is_parent == 0 and dm.dm_parent_id != 0:
            pass


    except Exception as e:
        logging.getLogger('').error(e)
        return False


def fetch_all_menu():
    try:
        select_line = DocMenu.objects.values()

        s_len = len(select_line)
        if s_len > 0:
            result = [entry for entry in select_line]
            return result
        # return select_line
        else:
            return "no doc menu"

    except Exception as e:
        logging.getLogger('').error(e)
        return False


class DocBll:
    """
    文档操作类
    """

    def __init__(self):
        self.list = []

    @staticmethod
    def add_api_doc(api_id):
        """
        添加api文档(不存在则添加)
        :return:
        """
        # 判断是否已经在ebt_doc中存在了
        api = Api.objects.get(api_id=int(api_id))
        ret = Doc.objects.get_or_create(api_id=api)
        return ret

    @staticmethod
    def add_doc(doc_type, doc_name):
        # 添加普通文档和内部文档
        doc = Doc(doc_type=int(doc_type), doc_name=doc_name)
        doc.save()
        return doc
        pass

    @staticmethod
    def get_api_doc(api):
        """
        根据接口参数生成默认文档
        :param api_id:
        :return:
        """
        ret = ""
        if api:
            tpl = open(os.path.join(DOC_TPL_PATH, "api.md"), 'r', encoding='utf-8').read()
            tpl = tpl.replace("{{api_name}}", api.api_name)
            tpl = tpl.replace("{{api_url}}", api.api_url)
            tpl = tpl.replace("{{api_request_type}}", api.api_request_type)
            tpl = tpl.replace("{{api_params}}", api.api_params)
            tpl = tpl.replace("{{api_classify}}", api.api_classify)
            tpl = tpl.replace("{{api_function}}", api.api_function)
            tpl = tpl.replace("{{api_level}}", str(api.api_level))
            tpl = tpl.replace("{{api_group}}", str(api.api_group))
            tpl = tpl.replace("{{api_invoke_total}}", str(api.api_invoke_total))
            tpl = tpl.replace("{{api_return}}", "")  # api.api_return
            tpl = tpl.replace("{{api_describe}}", api.api_describe)
            ret = tpl
        return ret

    @staticmethod
    def add(api_id, doc_type, doc_markdown, doc_html):
        """
        添加文档
        :param api_id:
        :param doc_markdown:
        :param doc_html:
        :param doc_type:
        :return:
        """
        try:
            if api_id == '':
                api = None
            else:

                api = Api.objects.get(api_id=api_id)

            doc_id = Doc.objects.order_by('doc_id').reverse()[0].doc_id + 1
            try:
                # doc = Doc.objects.get_or_create(doc_id)
                doc = Doc.objects.create(doc_id=doc_id, api_id=api, doc_markdown=doc_markdown, doc_html=doc_html,
                                         doc_type=doc_type)
                doc.save()
                return True
            except Exception as e:
                logging.getLogger('').error(e)
                print(1, e)
                return False

        except Exception as e2:
            logging.getLogger('').error(e2)
            print(2, e2)
            return False

    @staticmethod
    def delete(*doc_id):
        """
        删除文档
        :param doc_id:
        :return:
        """
        for num in doc_id:
            try:
                Doc.objects.filter(doc_id=num).delete()
                return True
            except Exception as e:
                logging.getLogger('').error(e)
                return False

    def search(*doc_id):
        """
        查询文档
        :param doc_id:
        :return:
        """
        data = []
        for num in doc_id:
            try:
                doc = Doc.objects.get(doc_id=num)
                d = dict(
                    api_id=doc.api_id.api_id, doc_markdown=doc.doc_markdown, doc_html=doc.doc_html,
                    doc_type=doc.doc_type, doc_create_date=doc.doc_create_date, doc_update_date=doc.doc_update_date
                )
                data.append(d)
            except Exception as e:
                logging.getLogger('').error(e)
                return False

        return data

    @staticmethod
    def fetch(page, limit, order_by_names):
        """
        获取所有文档
        :param page:
        :param limit:
        :return:
        """
        try:
            pager = Paginator(Doc.objects.all().order_by(order_by_names), int(limit))
            doc_set = pager.page(int(page))
            total_count = pager.count
            data = []

            for doc in doc_set:
                try:
                    api = doc.api_id
                    api_name = api.api_name
                except Exception as e:
                    logging.getLogger('').error(e)
                    api_name = ''
                d = dict(
                    doc_id=doc.doc_id,
                    api_name=api_name,
                    doc_name=doc.doc_name,
                    doc_markdown=doc.doc_markdown,
                    doc_html=doc.doc_html,
                    doc_type=doc.doc_type,
                    doc_create_date=date2ymdhms(doc.doc_create_date),
                    doc_update_date=date2ymdhms(doc.doc_update_date)
                )

                data.append(d)
            result = dict(
                totalCount=total_count,
                items=data
            )

            return result
        except Exception as e:
            logging.getLogger('').error(e)
            return ""

    @staticmethod
    def update(doc_id, api_id, doc_markdown, doc_html, doc_type, doc_create_date, doc_update_date):
        """
        更新文档
        :param doc_id:
        :param api_id:
        :param doc_markdown:
        :param doc_html:
        :param doc_type:
        :param doc_create_date:
        :param doc_update_date:
        :return:
        """
        try:
            doc = Doc.objects.get_or_create(doc_id=doc_id)
            api = Api.objects.get(api_id=api_id)
            try:
                Doc.objects.filter(doc_id=doc_id).update(
                    api_id=api, doc_markdown=doc_markdown, doc_html=doc_html,
                    doc_type=doc_type, doc_create_date=doc_create_date, doc_update_date=doc_update_date
                )
                return True
            except Exception as e:
                logging.getLogger('').error(e)
                return False
        except Exception as e:
            logging.getLogger('').error(e)
            return False


def file_upload(file):
    url = 'http://dldir.56iq.net/api/upload/?type=response'
    files = {
        'file': file
    }
    headers = {
        'Referer': 'http://localhost'
    }

    try:
        r = requests.post(url, headers=headers, files=files)

    except Exception as e:
        logging.getLogger('').error(e)
    else:
        return r


if __name__ == "__main__":
    # a = DocBll.add_doc(1)
    # print(a,a.doc_id)
    pass