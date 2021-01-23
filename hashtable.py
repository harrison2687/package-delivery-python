# Susan Harrison - 000854062
# C950 OA
class HashTable(object):
    def __init__(self, size=10):
        self._struct = self._create_struct(size)

    # this hashes the key and finds the modulo,
    # then uses the modulo to find the right bucket to append it to
    # O(n) complexity
    def insert(self, key, value):
        hashed_key = hash(key)
        bucket = self._find_bucket(hashed_key)

        extent = self._find_keyvalue_pair(hashed_key, bucket)

        if len(extent) == 0:
            bucket.append([hashed_key, value])
        else:
            extent[1] = value

        return True

    # this takes a key, hashes it, then finds the matching bucket
    # and loops through the bucket to find the value
    # O(n) complexity
    def find(self, key):
        hashed_key = hash(key)
        bucket = self._find_bucket(hashed_key)

        keyvalue_pair = self._find_keyvalue_pair(hashed_key, bucket)

        if keyvalue_pair:
            return keyvalue_pair[1]

        raise Exception("The key-value pair doesn't exist")

    # this loops through the hash table and creates buckets that will be used later
    # O(n) complexity
    def _create_struct(self, size):
        struct = []
        for i in range(size):
            struct.append([])
        return struct

    # this uses the modulo of the hashed key to find the right bucket
    # O(1) complexity
    def _find_bucket(self, key):
        return self._struct[key % len(self._struct)]

    # this loops through the bucket to find key-value pairs
    # O(n) complexity
    def _find_keyvalue_pair(self, key, bucket):
        for keyvalue_pair in bucket:
            if keyvalue_pair[0] == key:
                return keyvalue_pair

        return []
