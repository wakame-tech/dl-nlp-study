""" logger handler to notify to line """

class LineHandler(StreamHandler):
    """
    学習状況を LINE Push Message API で通知する
    """
    
    def __init__(self, token, ch):
        """
        Parameters
        ----------
        token: str
            アクセストークン
        ch: str
            チャンネルID
        """
        
        StreamHandler.__init__(self)
        self.token = token
        self.ch = ch

    def emit(self, record: LogRecord):
        text = self.format(record)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        message = {
            'to': self.ch,
            'messages': [{
                'type': 'text',
                'text': text
            }]
        }
        requests.post(
            url='https://api.line.me/v2/bot/message/push',
            headers=headers,
            data=json.dumps(message).encode('utf-8'),
        )