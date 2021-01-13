class Sender:
    """
    Makes a http request with server
    Request can be GET or POST
    """
    from requests import get, post
    
    def __init__(self, address):
        self.addr = address
        self.resp = None

        return

    def send(self, **kwargs):
        """
        Make GET or POST request with dictionary data
        By default, makes a GET request
        """

        data = kwargs.get('data')
        if data is None:
            # 'No data to send!!!'
            return

        # self.post or self.get produces error
        # Use class name instead
        if kwargs.get('request') == 'post':
            self.resp = Sender.post(self.addr, data=data)
        else:
            self.resp = Sender.get(self.addr, params=data)

        return

    def get_resp_status(self):
        """
        Returns the last request Status Code
        None if previous request was unsuccessful
        """
        if self.resp is not None:
            return self.resp.status_code

        return None

    def get_resp_text(self):
        """
        Returns the last request content
        None if previous request was unsuccessful
        """
        if self.resp is not None:
            return self.resp.text
        
        return None
    
