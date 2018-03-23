# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns

doc_urlpatterns = patterns(
    'app.center.doc_views',
    # markdown编辑器
    url(r'^editormd$', 'editormd', name='editormd'),
    # markdown编辑器上传图片
    url(r'^editormd/doc_images/', 'doc_image_upload', name='doc_image_upload'),

    # 获取文档列表
    url(r'^admin/doc/data', 'api_doc_fetch'),

    # 添加文档
    url(r'^admin/doc/add$', 'api_create_doc'),
    url(r'^admin/doc/delete$', 'api_delete_doc', name='delete_doc'),
    # 读取文档
    url(r'^doc_show/(?P<doc_id>\d+)$', 'doc_show'),
    # 菜单管理
    url(r'^doc_menu$', 'doc_menu', name='doc_menu'),
)

admin_urlpatterns = patterns(
    'app.center.admin_views',
    url(r'^admin/$', 'admin_home', name='admin_center'),
    url(r'^admin/user/list/data$', 'account_list_data'),
    url(r'^admin/developer/list/data$', 'developer_list_data'),
    url(r'^admin/developer/check/data$', 'developer_checking_data'),
    url(r'^admin/developer/modal/detail', 'developer_detail_modal'),
    url(r'^admin/application/data$', 'application_checked_data'),
    url(r'^admin/application/all/data$', 'application_all_data'),
    url(r'^admin/application/check/data$', 'application_checking_data'),
    url(r'^admin/application/modal/detail$', 'application_detail_modal'),

    url(r'^admin/function/data$', 'function_checked_data'),
    url(r'^admin/function/all/data$', 'function_all_data'),
    url(r'^admin/function/check/data$', 'function_checking_data'),


    url(r'^admin/api/list/data$', 'api_list_data'),
    url(r'^admin/api/data$', 'api_data'),
    url(r'^admin/api/modal/detail$', 'api_detail_modal'),
    url(r'^modify_pwd_admin$', 'modify_pwd_admin', name='modify_pwd_admin'),
)

urlpatterns = patterns(
    'app.center.views',
    url(r'^$', "home", name="center"),
    url(r'^login$', "login", name='login'),
    url(r'^callback$', "callback", name='callback'),
    url(r'^login_sys$', "login_sys", name='login_sys'),
    url(r'^logout$', "logout", name='logout'),
    url(r'^register$', "register", name='register'),
    url(r'^register_confirm$', "register_confirm", name='register_confirm'),
    url(r'^register_success$', "register_success", name='register_success'),
    url(r"^send_sms$", "send_sms", name="send_sms"),
    url(r'^validate_code$', 'validate_code', name='validate_code'),
    url(r'^check_user_name$', 'check_user_name', name='check_user_name'),
    url(r'(?i)^me$', 'me', name='me'),
    url(r'^check_fac_uuid$', 'check_fac_uuid', name='check_fac_uuid'),
    url(r'^send_email_code$', 'send_email_code', name='send_email_code'),
    url(r'^checklist$', 'checklist', name='checklist'),
    url(r'^prolist$', 'prolist', name='prolist'),
    url(r'^active$', 'active', name='active'),
    url(r'^forget_pwd$', 'forget_pwd', name='forget_pwd'),
    url(r'^view_rule$', 'view_rule', name='view_rule'),
    url(r'^modify_pwd$', 'modify_pwd', name='modify_pwd'),

)

urlpatterns += doc_urlpatterns
urlpatterns += admin_urlpatterns
