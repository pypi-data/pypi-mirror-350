from typing import Optional

from pydantic.v1 import BaseSettings

from fastpluggy.core.repository.app_settings import database_settings_source


class BaseDatabaseSettings(BaseSettings):
    class Config:
        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings
        ):
            return (
                init_settings,  # 1. Explicitly passed settings
                env_settings,   # 2. Environment variables
                file_secret_settings,  # 3. Secrets from files
                database_settings_source,  # 4. Custom database source
            )

class FastPluggyConfig(BaseDatabaseSettings):
    app_name : Optional[str] = 'FastPluggy'

    # admin config
    admin_enabled:Optional[bool] = True
    fp_admin_base_url : Optional[str] = '/admin'
    plugin_list_url : Optional[str] = 'https://registry.fastpluggy.xyz/plugins.json'

    show_empty_menu_entries: Optional[bool] = True
    install_module_requirement_at_start:Optional[bool] = True
    check_all_plugin_updates_at_start:Optional[bool] = False

    session_secret_key:str = "your-secret-key"

