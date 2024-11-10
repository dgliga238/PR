import re

def custom_deserialize(serialized_str):

    if serialized_str.startswith('{') and serialized_str.endswith('}'):
        items = split_items(serialized_str[1:-1], ';')
        return {k: custom_deserialize(v) for k, v in (item.split('=', 1) for item in items)}
    elif serialized_str.startswith('[') and serialized_str.endswith(']'):
        items = split_items(serialized_str[1:-1], ',')
        return [custom_deserialize(item) for item in items]
    elif serialized_str.startswith('"') and serialized_str.endswith('"'):
        return serialized_str[1:-1]
    elif serialized_str.startswith('i:'):
        return int(serialized_str[2:])
    else:
        return serialized_str

def split_items(serialized_str, delimiter):

    items = []
    depth = 0
    in_string = False
    current_item = []

    for char in serialized_str:
        if char == '"':
            in_string = not in_string
        elif not in_string:
            if char in "{[":
                depth += 1
            elif char in "}]":
                depth -= 1
            elif char == delimiter and depth == 0:
                items.append(''.join(current_item).strip())
                current_item = []
                continue
        current_item.append(char)

    items.append(''.join(current_item).strip())
    return items

def custom_serialize(obj):

    if isinstance(obj, dict):
        return '{' + '+'.join(f"{k}={custom_serialize(v)}" for k, v in obj.items()) + '}'
    elif isinstance(obj, list):
        return '[' + ','.join(custom_serialize(item) for item in obj) + ']'
    elif isinstance(obj, str):
        return f'"{obj}"'
    elif isinstance(obj, int):
        return f'i:{obj}'
    else:
        raise TypeError(f"Unsupported type: {type(obj)}")

def example_serialization_deserialization():
    # Test data: a dictionary containing various types
    test_data = {
        "string": "Hello, World!",
        "integer": 42,
        "list": [1, 2, 3, "four", {"nested_dict": "value"}],
        "dict": {
            "key1": "value1",
            "key2": 99,
            "key3": ["item1", "item2", 3]
        }
    }

    # Additional sample list
    sample_list = [
        {
            "name": "Apple iPhone 15 Pro Max 256 GB Natural Titanium",
            "price": "1349 EUR",
            "product": "Apple",
            "link": "https://darwin.md/apple-iphone-15-pro-max-8-gb-256-gb-single-sim-5gtitanium-natural.html",
            "timestamp": "2024-10-18T12:32:47.039794"
        },
        {
            "name": "Apple iPhone 15 Pro Max 256 GB Blue Titanium",
            "price": "1349 EUR",
            "product": "Apple",
            "link": "https://darwin.md/apple-iphone-15-pro-max-8-gb-256-gb-single-sim-5gtitanium-blue.html",
            "timestamp": "2024-10-18T12:32:51.060152"
        },
        {
            "name": "Apple iPhone 15 Pro Max 256 GB Black Titanium",
            "price": "1349 EUR",
            "product": "Apple",
            "link": "https://darwin.md/smartphone-apple-iphone-15-pro-max-mu773rx-a-8-gb-256-gb-single-sim-5g-black-titanium.html",
            "timestamp": "2024-10-18T12:32:53.349339"
        },
        {
            "name": "Apple iPhone 15 Pro Max 256 GB White Titanium",
            "price": "1349 EUR",
            "product": "Apple",
            "link": "https://darwin.md/apple-iphone-15-pro-max-8-gb-256-gb-single-sim-5gtitanium-white.html",
            "timestamp": "2024-10-18T12:32:55.729884"
        }
    ]

    # Serialize the test data
    serialized_data = custom_serialize(test_data)
    print("Serialized test data:")
    print(serialized_data)

    # Deserialize the serialized test data back to a Python object
    deserialized_data = custom_deserialize(serialized_data)
    print("\nDeserialized test data:")
    print(deserialized_data)



    # Serialize the additional sample list
    serialized_sample_list = custom_serialize(sample_list)
    print("\nSerialized sample list:")
    print(serialized_sample_list)

    # Deserialize the serialized sample list back to a Python object
    deserialized_sample_list = custom_deserialize(serialized_sample_list)
    print("\nDeserialized sample list:")
    print(deserialized_sample_list)


if __name__ == "__main__":
    example_serialization_deserialization()
