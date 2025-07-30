from .valid_json_versions import valid_json_versions


# TODO Shall we merge it with the machine-learning-unified-json?
class UnifiedJson:
    def __init__(self, data: dict, json_version: str):
        if json_version not in valid_json_versions:
            raise Exception(
                f"version {json_version} is not in valid_json_versions {valid_json_versions}, "
                f"please make sure you run sql2code."
            )
        self.json_version = json_version
        self.data = data

    def get_unified_json(self):
        return {"version": self.json_version, "data": self.data}

    def get_data(self):
        return self.data

    def get_json_version(self):
        return self.json_version

    def __str__(self):
        return self.get_unified_json()

    def __repr__(self):
        return self.__str__()
