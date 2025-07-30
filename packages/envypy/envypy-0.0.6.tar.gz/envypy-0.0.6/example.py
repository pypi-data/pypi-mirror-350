import envypy

envybase = envypy.Envypy("http://localhost:3100")

envybase.database.insert(
    {
        "name": "test_document",
        "data": {"key1": "value1", "key2": "value2"},
        "created_at": "2023-10-01T12:00:00Z",
    }
)