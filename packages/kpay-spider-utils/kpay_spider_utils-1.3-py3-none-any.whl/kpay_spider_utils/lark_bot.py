import requests


class LarkBot:
    """
    lark机器人
    """

    def __init__(self, webhook: str):
        """
        :param webhook: webhook，只需要URL后面webhook=后面的值
        """
        self.headers = {
            'Content-Type': 'application/json',
        }
        self.webhook = webhook

    def send_message(self, message: str, user: str = None):
        """
        :param message: 发送的消息
        :param user: 需要@的用户
        :return: 返回数据
        """
        data = {
            'msg_type': 'text',
            'content': {
                'text': str(message)
            },
        }
        post_url = f'https://open.larksuite.com/open-apis/bot/v2/hook/{self.webhook}'
        req = requests.post(post_url, headers=self.headers, json=data, timeout=20)
        return req.json()