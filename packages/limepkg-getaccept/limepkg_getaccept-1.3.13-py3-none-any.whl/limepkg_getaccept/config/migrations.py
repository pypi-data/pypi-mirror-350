import lime_admin.plugins


class Migration1(lime_admin.plugins.ConfigMigration):
    """describe the schema changes"""

    @property
    def version(self):
        return 2  # the new version, after running the upgrade

    def upgrade(self, config):
        if config.get("person"):
            for item in config.get("person").get("personSettings"):
                if item.get("phone"):
                    item["mobile"] = item["phone"]
                    del item["phone"]
        if config.get("coworker") and config.get("coworker").get("phone"):
            config["coworker"]["mobile"] = config["coworker"]["phone"]
            del config["coworker"]["phone"]

        return config

    def downgrade(self, config):
        return config
