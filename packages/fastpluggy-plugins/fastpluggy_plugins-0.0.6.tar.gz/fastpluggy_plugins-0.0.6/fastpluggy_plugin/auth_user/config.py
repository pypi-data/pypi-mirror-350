from fastpluggy.core.config import BaseDatabaseSettings


class AuthUserConfig(BaseDatabaseSettings):
    default_admin_username:str ='admin'
    default_admin_password:str ='admin'
   # role_for_fp_admin:str ='super_admin'