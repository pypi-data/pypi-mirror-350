from netbox.plugins import PluginMenuButton, PluginMenuItem, PluginMenu

menu = PluginMenu(
    label="NetAuto F5",
    icon_class="mdi mdi-cloud-sync",
    groups=(
        ("Applications", (
            PluginMenuItem(
                link="plugins:netbox_netauto_plugin:flexapplication_list",
                link_text="Flex Applications",
                buttons=(
                    PluginMenuButton(
                        link="plugins:netbox_netauto_plugin:flexapplication_add",
                        title="Add",
                        icon_class="mdi mdi-plus-thick",
                    ),
                ),
            ),
            PluginMenuItem(
                link="plugins:netbox_netauto_plugin:l4application_list",
                link_text="L4 Applications",
                buttons=(
                    PluginMenuButton(
                        link="plugins:netbox_netauto_plugin:l4application_add",
                        title="Add",
                        icon_class="mdi mdi-plus-thick",
                    ),
                ),
            ),
            PluginMenuItem(
                link="plugins:netbox_netauto_plugin:mtlsapplication_list",
                link_text="mTLS Applications",
                buttons=(
                    PluginMenuButton(
                        link="plugins:netbox_netauto_plugin:mtlsapplication_add",
                        title="Add",
                        icon_class="mdi mdi-plus-thick",
                    ),
                ),
            ),
        )),
        ("Profiles", (
            PluginMenuItem(
                link="plugins:netbox_netauto_plugin:profile_list",
                link_text="Profiles",
                buttons=(
                    PluginMenuButton(
                        link="plugins:netbox_netauto_plugin:profile_add",
                        title="Add",
                        icon_class="mdi mdi-plus-thick",
                    ),
                ),
            ),
        )),
    ),
)