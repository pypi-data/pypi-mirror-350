# -*- coding: utf-8 -*-
# @Time    : 2025/5/23 上午11:17
# @Author  : 车小炮
import json
import os.path
import time

import loguru
import requests
from requests_toolbelt import MultipartEncoder


class Lark_Api:
    def __init__(self, app_id, app_secret):
        self.user_token_file_name = 'user_access_token.json'
        self.app_token_file_name = 'app_access_token.json'
        self.app_id = app_id
        self.app_secret = app_secret

    def lark_get_app_token(self, refresh_token=False):
        """
        获取app_token
        :param refresh_token: 是否刷新app_token
        :return:
        """
        if os.path.exists(self.app_token_file_name) and refresh_token == False:
            with open(self.app_token_file_name, 'r') as f:
                app_access_token = json.load(f)
                if app_access_token['write_time'] < time.time() - 7000:
                    loguru.logger.info('刷新app_token')
                    self.lark_get_app_token(refresh_token=True)
        else:
            loguru.logger.info('获取app_token')
            url = 'https://open.larksuite.com/open-apis/auth/v3/app_access_token/internal'
            data = {
                "app_id": self.app_id,
                "app_secret": self.app_secret
            }
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            response = requests.post(url, json=data, headers=headers)
            result = response.json()
            result['write_time'] = time.time()
            with open(self.app_token_file_name, 'w') as f:
                json.dump(result, f)
            app_access_token = result
        return app_access_token

    def lark_get_login_code(self):
        """
        打开授权url，点击url进行授权，成功后把网址的code输入到控制台
        :return:
        """
        login_url = f'https://open.larksuite.com/open-apis/authen/v1/authorize?app_id={self.app_id}&redirect_uri=https%3A%2F%2F127.0.0.1%2Fmock%2F%23%2Flogin&scope=drive:drive'
        print(login_url)
        authorization_code = input('输入登录授权码: ')
        return authorization_code

    def lark_get_user_token(self, token=True):
        '''
        先判断是否存在user_token的json文件，没有则先创建一个
        判断存在的文件msg是否为success，不是则重新获取
        token有效期为两小时，写入文件时增加写入时间，读取文件写入时间大于两小时则刷新token
        :return:
        '''
        if os.path.exists(self.user_token_file_name) and token == True:
            with open(self.user_token_file_name, 'r') as f:
                user_access_token = json.load(f)
                if user_access_token['message'] != 'success':
                    self.lark_get_user_token(token=False)
                if user_access_token['write_time'] < time.time() - 7000:
                    refresh_token = user_access_token['data']['refresh_token']
                    user_access_token = self.lark_get_user_refresh_token(refresh_token)
        else:
            authorization_code = self.lark_get_login_code()
            app_access_token = self.lark_get_app_token()['app_access_token']
            headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'Authorization': f'Bearer {app_access_token}',
            }
            url = 'https://open.larksuite.com/open-apis/authen/v1/oidc/access_token'
            data = {
                'grant_type': 'authorization_code',
                'code': authorization_code
            }
            response = requests.post(url, headers=headers, json=data)
            user_access_token = response.json()
            user_access_token['write_time'] = time.time()
            with open(self.user_token_file_name, 'w') as f:
                json.dump(user_access_token, f)
            loguru.logger.info('获取user_token', user_access_token)
        return user_access_token

    def lark_get_user_refresh_token(self, refresh_token):
        """
        user_access_token 的最大有效期是 2小时左右。
        当 user_access_token 过期时，可以调用refresh_token获取新的 user_access_token
        :param refresh_token:
        :return:
        """
        app_access_token = self.lark_get_app_token()['app_access_token']
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {app_access_token}',
        }
        url = 'https://open.larksuite.com/open-apis/authen/v1/oidc/refresh_access_token'
        data = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        result['write_time'] = time.time()
        with open(self.user_token_file_name, 'w') as f:
            json.dump(result, f)
        loguru.logger.info('刷新user_token', result)
        return result

    def lark_get_root_folder(self):
        """
        获取 "我的空间" 的元信息
        :return:
        """
        user_token = self.lark_get_user_token()['data']['access_token']
        url = 'https://open.larksuite.com/open-apis/drive/explorer/v2/root_folder/meta'
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {user_token}',
        }
        response = requests.get(url, headers=headers)
        result = response.json()
        print(result)
        return result

    def lark_create_folder(self, params):
        '''
        新建文件夹
        ---------
        @param name: 文件夹名称
        @param folder_token: 父文件夹token
        :return:
        '''
        user_token = self.lark_get_user_token()['data']['access_token']
        url = 'https://open.larksuite.com/open-apis/drive/v1/files/create_folder'
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {user_token}',
        }
        response = requests.get(url, headers=headers, params=params)
        result = response.json()
        print(result)
        return result

    def lark_get_file_list(self, params):
        '''
        获取文件列表
        params不指定文件夹token的话默认获取用户云空间下的清单
        ---------
        @param page_size: 分页大小
        @param page_token: 分页标记，第一次请求不填，表示从头开始遍历；分页查询结果还有更多项时会同时返回新的 page_token，下次遍历可采用该 page_token 获取查询结果
        @param folder_token: 文件夹的token（若不填写该参数或填写空字符串，则默认获取用户云空间下的清单，且不支持分页）
        :return:
        '''
        user_token = self.lark_get_user_token()['data']['access_token']
        url = 'https://open.larksuite.com/open-apis/drive/v1/files'
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {user_token}',
        }
        response = requests.get(url, headers=headers, params=params)
        result = response.json()
        print(result)
        return result

    def lark_upload_file(self, file_path, file_name, parent_node):
        """
        @param file_path: 文件路径
        @param file_name: 上传后的文件名
        @param parent_node: 文件夹token
        :return:
        """
        file_size = os.path.getsize(file_path)
        user_token = self.lark_get_user_token()['data']['access_token']
        url = 'https://open.larksuite.com/open-apis/drive/v1/files/upload_all'
        headers = {
            'Authorization': f'Bearer {user_token}',
        }
        form = {'file_name': file_name,
                'parent_type': 'explorer',
                'parent_node': parent_node,
                'size': str(file_size),
                'file': (open(file_path, 'rb'))}
        multi_form = MultipartEncoder(form)
        headers['Content-Type'] = multi_form.content_type
        requests.request("POST", url, headers=headers, data=multi_form)

    def lark_download_file(self, file_name, file_token):
        user_token = self.lark_get_user_token()['data']['access_token']
        url = f'https://open.larksuite.com/open-apis/drive/v1/files/{file_token}/download'
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {user_token}',
        }
        response = requests.get(url, headers=headers)
        with open(file_name, mode='wb') as f:
            f.write(response.content)

    def lark_permissions_list(self, data):
        """
        @data token: 文件的 token
        @data type: 文档类型 "doc" or "sheet" or "bitable" or "file"
        :return:
        """
        user_token = self.lark_get_user_token()['data']['access_token']
        url = f'https://open.larksuite.com/open-apis/drive/permission/member/list'
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {user_token}',
        }
        response = requests.post(url, headers=headers, data=data)
        result = response.json()
        print(result)
        return result

    def lark_add_permissions(self, file_token, params, data):
        """
        @params type: 文件类型，放于query参数中
            doc：文档
            sheet：电子表格
            file：云空间文件
            wiki：知识库节点（部分支持）
            bitable：多维表格
            docx：文档（暂不支持）
        @params need_notification: 是否通知对方（填bool值)可以不填，默认不通知

        @data member_type: 用户类型（主要用Lark邮箱）
            email: Lark邮箱
            openid: 开放平台ID
            openchat: 开放平台群组
            opendepartmentid:开放平台部门ID
            userid: 用户自定义ID
        @data member_id: 用户类型下的值
        @data perm: 需要更新的权限
            view: 可阅读
            edit: 可编辑
            full_access: 所有权限
        :return:
        """
        user_token = self.lark_get_user_token()['data']['access_token']
        url = f'https://open.larksuite.com/open-apis/drive/v1/permissions/{file_token}/members'
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {user_token}',
        }
        response = requests.post(url, headers=headers, params=params, data=data)
        result = response.json()
        print(result)
        return result


