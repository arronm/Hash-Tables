# '''
# Linked List hash table key/value pair
# '''
class LinkedPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    '''
    A hash table that with `capacity` buckets
    that accepts string keys
    '''
    def __init__(self, capacity):
        self.capacity = capacity  # Number of buckets in the hash table
        self.storage = [None] * capacity


    def _hash(self, key):
        '''
        Hash an arbitrary key and return an integer.

        You may replace the Python hash with DJB2 as a stretch goal.
        '''
        return hash(key)


    def _hash_djb2(self, key):
        '''
        Hash an arbitrary key using DJB2 hash

        OPTIONAL STRETCH: Research and implement DJB2
        '''
        hash = 5381  # 52711
        for letter in key:
            hash = (( hash << 5) + hash) + ord(letter)
        return hash  # & 0xFFFFFFFF


    def _hash_mod(self, key):
        '''
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        '''
        return self._hash_djb2(key) % self.capacity


    def insert(self, key, value):
        '''
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Fill this in.
        '''
        index = self._hash_mod(key)

        if self.storage[index] is None:
            self.storage[index] = LinkedPair(key, value)
        else:
            lookup = self.storage[index]
            while lookup.next:
                if lookup.key == key:
                    break
                lookup = lookup.next

            if lookup.key == key:
                lookup.value = value
            else:
                lookup.next = LinkedPair(key, value)


    def remove(self, key):
        '''
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Fill this in.
        '''
        index = self._hash_mod(key)
        
        current = self.storage[index]

        # handle case where key is first linked
        if current.key == key:
            # Our item is first in the linked list, check if next
            if current.next is None:
                # No other items in this list, reset storage at index
                self.storage[index] = None
            else:
                self.storage[index] = current.next
            
            return current.value
        
        # while we have a next link, and that next link is not our desired key
        while current.next and current.next.key != key:
            current = current.next
        
        removed = current.next
        current.next = removed.next
        return removed.value


    def retrieve(self, key):
        '''
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Fill this in.
        '''
        index = self._hash_mod(key)

        lookup = self.storage[index]
        if lookup is None:
            return None

        while lookup.key != key:
            if lookup.next is None:
                return None
            lookup = lookup.next
        
        return lookup.value


    def resize(self):
        # Check current capacity and resize as necessary
        # 0.7 capacity, double
        # 0.2 capacity, halve
        pass
    
    def _double(self):
        '''
        Doubles the capacity of the hash table and
        rehash all key/value pairs.

        Fill this in.
        '''
        # Double our capacity
        old_storage = self.storage
        old_capacity = self.capacity
        self.capacity *= 2
        self.storage = [None] * self.capacity

        # Loop through old storage to rehash k,v pairs
        for i in range(old_capacity):
            current = old_storage[i]

            # skip empty indexes
            if current is None:
                continue
            
            while current.next:
                self.insert(current.key, current.value)
                current = current.next

            # Insert last linked pair
            self.insert(current.key, current.value)

    def _halve(self):
        pass



if __name__ == "__main__":
    ht = HashTable(2)

    ht.insert("line_1", "Tiny hash table")
    ht.insert("line_2", "Filled beyond capacity")
    ht.insert("line_3", "Linked list saves the day!")

    print("")

    # Test storing beyond capacity
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    ht.resize()
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    print("")
