from bson import ObjectId

class MongoDataDeserializer:
    def __init__(self, data):
        self.data = data

    def deserialize(self):
        """
        Convert MongoDB/BSON data into a Python dictionary.
        This includes converting ObjectId to string for JSON compatibility.
        """
        if isinstance(self.data, list):
            return [self._deserialize_data(item) for item in self.data]
        return self._deserialize_data(self.data)

    def _deserialize_data(self, data):
        """
        Recursive method to handle the deserialization of MongoDB/BSON data.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, ObjectId):
                    data[key] = str(value)
                elif isinstance(value, list):
                    data[key] = [self._deserialize_data(item) for item in value]
                elif isinstance(value, dict):
                    data[key] = self._deserialize_data(value)
        elif isinstance(data, list):
            return [self._deserialize_data(item) for item in data]
        return data

    @classmethod
    def deserialize_results(cls, results):
        """
        Class method to handle deserialization of a list of results (e.g., abc_student_accounts).
        This will create an instance for each result and deserialize them.
        """
        return [cls(result.dict()).deserialize() for result in results]
