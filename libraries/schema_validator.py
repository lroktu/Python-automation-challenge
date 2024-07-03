
import jsonschema

from libraries.enums.topics import Topics
import logging
class schema_validator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.schema = {
            "type": "object",
            "properties": {
                "search-phrase": {
                    "type": "string"
                },
                "till-months-passed": {
                    "type": "integer",
                    "maximum": 6
                }
            },
            "required": ["search-phrase", "till-months-passed"]
        }

        
    def validate(self, data):
        try:
            jsonschema.validate(data, self.schema)
            if (data["till-months-passed"] == 0):
                data["till-months-passed"] = 1
            if (len(data["topics"]) == 0):
                data["topics"] = [Topics.ALL.value]
                self.logger.warn("No Topics found. Making Topics as 'All'")
        except jsonschema.ValidationError as e:
            error_field = str(e.path[0]) if e.path else "Unknown Field"      
            raise ValueError(f"Invalid schema for field {error_field}. Msg: {e.message}")
        return data


