class Base():
    def __init__(self, client):
        self.client = client
        self.base_url = client.base_url
        self.short_url = client.short_url

        self.settings = client.settings

    def _make_request(
            self,
            endpoint,
            payload=None,
            params=None,
            method='post',
            files=None
    ):
        url = f'{self.base_url}/{endpoint}'

        if method.lower() == 'get':
            return self.client.session.get(url, params=params, verify=False)
        else:
            return self.client.session.post(
                url, json=payload, params=params, files=files, verify=False
            )
