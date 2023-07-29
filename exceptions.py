class NotLinksException(Exception):
    default_message = """
    Ни на одной странице не получилось найти хотя бы одну ссылку на товар. 
    Это может быть связано с тем, что код страницы на `yoox.com` изменился
    """

    def __init__(self, message=default_message):
        self.message = message
        super().__init__(self.message)
