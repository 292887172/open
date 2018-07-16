# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from django.core.paginator import Paginator
from model.center.doc import Doc
from model.center.doc_menu import DocMenu

__author__ = 'nailuoGG'


class ActionForMenu:
    """
    菜单管理类
    增删查改
    """

    def __init__(self):
        self.list = []

    @staticmethod
    def add(doc_id, dm_name, dm_is_parent, dm_url, dm_class, dm_depth, dm_order_num, dm_parent_id):
        """
        添加菜单
        :param doc_id:
        :param dm_name:
        :param dm_is_parent:
        :param dm_url:
        :param dm_class:
        :param dm_depth:
        :param dm_ordernum:
        :param dm_parent_id:
        :return:
        """
        doc = None
        try:
            if doc_id == '':
                doc = None
            else:
                doc = Doc.objects.get(doc_id=doc_id) if not Doc.objects.filter(
                    doc_id=doc_id).exists() or doc_id == '' else None
        except Exception as e1:
            logging.getLogger("").error(e1)

        finally:
            try:
                doc_menu = DocMenu.objects.create(
                    doc_id=doc,
                    dm_name=dm_name,
                    dm_is_parent=dm_is_parent,
                    dm_url=dm_url,
                    dm_class=dm_class,
                    dm_depth=dm_depth,
                    dm_order_num=dm_order_num,
                    dm_parent_id=dm_parent_id
                )
                ret = doc_menu.dm_id
                doc_menu.save()
                return ret
            except Exception as e:
                logging.getLogger("").error(e)
                print(e)
                return ""

    @staticmethod
    def delete(*dm_id):
        """
        删除菜单
        :param dm_id:
        :return:
        """
        for x in dm_id:
            try:
                menu = DocMenu.objects.get(dm_id=x)
                try:
                    menu.delete()
                    return True
                except Exception as e1:
                    logging.getLogger("").error(e1)
                    return False
            except Exception as e:
                logging.getLogger('').error(e)
                return False

    @staticmethod
    def fetch(page, limit, order_by_names):
        try:
            pager = Paginator(DocMenu.objects.all().order_by(order_by_names), int(limit))
            menu_set = pager.page(int(page))
            total_count = pager.count

            data = []

            for menu in menu_set:
                doc_id = ''
                try:
                    doc_id = menu.doc_id.doc_id
                except Exception as e:
                    logging.getLogger('').error(e)
                finally:
                    dm_id = menu.dm_id
                    d = dict(
                        dm_id=dm_id,
                        doc_id=doc_id,
                        dm_name=menu.dm_name,
                        dm_is_parent=menu.dm_is_parent,
                        dm_class=menu.dm_class,
                        dm_url=menu.dm_url,
                        dm_depth=menu.dm_depth,
                        dm_ordernum=menu.dm_order_num,
                        dm_parent_id=menu.dm_parent_id

                    )
                    data.append(d)
            result = dict(
                totalCount=total_count,
                items=data
            )
            return result
        except Exception as e:
            logging.getLogger('').error(e)
            print(e)
            return []

    @staticmethod
    def update(dm_id, doc_id, dm_name, dm_is_parent, dm_url, dm_class, dm_depth, dm_ordernum, dm_parent_id):
        try:
            doc = Doc.objects.get(doc_id=doc_id)
            try:
                DocMenu.objects.filter(dm_id=dm_id).update(
                    doc_id=doc,
                    dm_name=dm_name,
                    dm_is_parent=dm_is_parent,
                    dm_url=dm_url,
                    dm_class=dm_class,
                    dm_depth=dm_depth,
                    dm_ordernum=dm_ordernum,
                    dm_parent_id=dm_parent_id

                )
                return True
            except Exception as e:
                logging.getLogger('').error(e)
                return False
        except Exception as e2:
            logging.getLogger('').error(e2)
            return False


STATUS_CODE = {
    "success": {
        "status" : 1,
        "message": "成功"
    },
    "error"  : {
        "status" : 0,
        "message": "失败"
    }
}
