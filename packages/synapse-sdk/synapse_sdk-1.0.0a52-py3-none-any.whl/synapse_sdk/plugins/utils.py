import json
from pathlib import Path

from synapse_sdk.i18n import gettext as _
from synapse_sdk.plugins.categories.registry import _REGISTERED_ACTIONS, register_actions
from synapse_sdk.plugins.enums import PluginCategory
from synapse_sdk.plugins.exceptions import ActionError
from synapse_sdk.utils.file import get_dict_from_file


def get_action(action, params_data, *args, **kwargs):
    if isinstance(params_data, str):
        try:
            params = json.loads(params_data)
        except json.JSONDecodeError:
            params = get_dict_from_file(params_data)
    else:
        params = params_data

    config_data = kwargs.pop('config', False)
    if config_data:
        if isinstance(config_data, str):
            config = read_plugin_config(plugin_path=config_data)
        else:
            config = config_data
    else:
        config = read_plugin_config()
    category = config['category']
    return get_action_class(category, action)(params, config, *args, **kwargs)


def get_action_class(category, action):
    register_actions()
    return _REGISTERED_ACTIONS[category][action]


def get_available_actions(category):
    register_actions()
    return list(_REGISTERED_ACTIONS[category].keys())


def get_plugin_categories():
    return [plugin_category.value for plugin_category in PluginCategory]


def read_plugin_config(plugin_path=None):
    config_file_name = 'config.yaml'
    if plugin_path:
        config_path = Path(plugin_path) / config_file_name
    else:
        config_path = config_file_name
    return get_dict_from_file(config_path)


def read_requirements(file_path):
    file_path = Path(file_path)
    if not file_path.exists():
        return None

    requirements = []
    for line in file_path.read_text().splitlines():
        stripped_line = line.strip()
        if stripped_line and not stripped_line.startswith('#'):
            requirements.append(stripped_line)
    return requirements


def run_plugin(
    action,
    params,
    plugin_config=None,
    plugin_path=None,
    modules=None,
    requirements=None,
    envs=None,
    debug=False,
    **kwargs,
):
    from synapse_sdk.plugins.models import PluginRelease

    if not envs:
        envs = {}

    if debug:
        if plugin_path and plugin_path.startswith('http'):
            if not plugin_config:
                raise ActionError({'config': _('"plugin_path"가 url인 경우에는 "config"가 필수입니다.')})
            plugin_release = PluginRelease(config=plugin_config)
        else:
            plugin_release = PluginRelease(plugin_path=plugin_path)
            plugin_config = plugin_release.config

        if action not in plugin_release.actions:
            raise ActionError({'action': _('해당 액션은 존재하지 않습니다.')})

        if plugin_path:
            envs['SYNAPSE_DEBUG_PLUGIN_PATH'] = plugin_path

        if modules:
            envs['SYNAPSE_DEBUG_MODULES'] = ','.join(modules)

    else:
        if plugin_config is None:
            raise ActionError({'config': _('플러그인 설정은 필수입니다.')})

    action = get_action(
        action,
        params,
        config=plugin_config,
        requirements=requirements,
        envs=envs,
        debug=debug,
        **kwargs,
    )
    return action.run_action()
