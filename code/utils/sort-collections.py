
d = {2: 56, 1: 2, 5: 12, 4: 24, 6: 18, 3: 323}


# - Create a dictionary and display its keys alphabetically.
def dict_1(dc):
    print("Task 1: - Keys are: ")
    for i in sorted(dc.keys()):
        print(f"{i}, ", end='')


# - Display both the keys and values sorted in alphabetical order by the key.
def dict_2(dc):
    print("\nTask 2: - Keys and Values sorted - by the key")
    for i in sorted(dc):
        print(f"({i}, {dc[i]}) ", end='')


# - Same as part (ii), but sorted in alphabetical order by the value.
def dict_3(dc):
    print("\nTask 3: - Keys and Values sorted - by the value (output List of Tuples)")
    print(sorted(dc.items(), key=lambda kv: (kv[1], kv[0])))


def dict_3_1(dc):
    print("\nTask 3-1: - Keys and Values sorted - by the value (output Dict)")
    sorted_dc = {k: v for k, v in sorted(dc.items(), key=lambda x: x[1], reverse=True)}
    for k, v in sorted_dc.items():
        print(f"{k} - {v}")


if __name__ == "__main__":
    dict_1(d)
    dict_2(d)
    dict_3(d)
    dict_3_1(d)
