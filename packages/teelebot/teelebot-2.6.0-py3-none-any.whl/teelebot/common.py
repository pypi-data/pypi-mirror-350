'''
@creation date: 2023-05-13
@last modification: 2024-02-29
'''

__cloud_api_server__ = "https://api.telegram.org/"
__common_pkg_prefix__ = "~~"
__inline_mode_prefix__ = "?:"

__metadata_templates__ = {
    "1.0": {
        "Metadata-version": "1.0",
        "Plugin-name": "",
        "Version": "",
        "Summary": "",
        "Home-page": "",
        "Author": "",
        "Author-email": "",
        "License": "",
        "Keywords": "",
        "Requires-teelebot": "",
        "Requires-dist": "",
        "Source": ""
    },
    "1.1": {
        "Metadata-version": "1.1",
        "Plugin-name": "",
        "Command": "",
        "Buffer-permissions": "False:False",
        "Version": "",
        "Summary": "",
        "Home-page": "",
        "Author": "",
        "Author-email": "",
        "License": "",
        "Keywords": "",
        "Requires-teelebot": "",
        "Requires-dist": "",
        "Source": ""
    }
}
__metadata_version_in_use__ = max(__metadata_templates__.keys())

__config_template__ = {
    "[config]": "",
    "key": "",
    "root_id": "",
    "plugin_dir": "",
    "pool_size": "40",
    "buffer_size": "16",
    "debug": "False",
    "hide_info": "False",
    "proxy": "",
    "local_api_server": "False",
    "drop_pending_updates": "False",
    "updates_chat_member": "False",
    "webhook": "False",
    "self_signed": "False",
    "cert_key": "",
    "cert_pub": "",
    "load_cert": "False",
    "server_address": "",
    "server_port": "",
    "local_address": "",
    "local_port": "",
    "secret_token": ""
}

__plugin_init_func_name__ = "Init"

__plugin_control_plugin_name__ = "PluginCTL"
__plugin_control_plugin_command__ = "/pluginctl"


