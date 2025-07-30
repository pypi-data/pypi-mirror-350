from parsomics_core.plugin_utils import PluginInitializer

from parsomics_plugin_clean.populate import populate_clean

initializer = PluginInitializer(
    subject="clean",
    plugin_name="parsomics-plugin-clean",
    populate_func=populate_clean,
)
