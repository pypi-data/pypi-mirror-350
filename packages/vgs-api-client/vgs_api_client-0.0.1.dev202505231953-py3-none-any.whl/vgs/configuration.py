from vgs_api_client import Configuration


class VGSConfiguration(Configuration):
    def __init__(
        self,
        vault_id=None,
        username=None,
        password=None,
        host="https://api.sandbox.verygoodvault.com",
        environment="sandbox",
        service_account_name=None,
        service_account_password=None,
        **kwargs,
    ):
        super(VGSConfiguration, self).__init__(username=username, password=password, host=host, **kwargs)
        self.vault_id = vault_id
        self.environment = environment
        self.service_account_name = service_account_name
        self.service_account_password = service_account_password


def config(*args, **kwargs):
    return VGSConfiguration(*args, **kwargs)
