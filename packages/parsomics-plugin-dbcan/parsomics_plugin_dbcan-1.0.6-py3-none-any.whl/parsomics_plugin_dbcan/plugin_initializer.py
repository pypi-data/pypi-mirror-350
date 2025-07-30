from parsomics_core.plugin_utils import PluginInitializer

from parsomics_plugin_dbcan.populate import populate_dbcan

initializer = PluginInitializer(
    subject="dbcan",
    plugin_name="parsomics-plugin-dbcan",
    populate_func=populate_dbcan,
)
