import hashlib

PLUGINS_FILE_PATH = "plugins.json"


def hash_file(filepath, algorithm="sha256"):
    hash_func = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def write_hash_to_file(filepath):
    hash_value = hash_file(filepath)
    output_file = f"{filepath}.hash"
    with open(output_file, "w") as f:
        f.write(f"{hash_value}\n")


def main():
    write_hash_to_file(PLUGINS_FILE_PATH)


if __name__ == "__main__":
    main()
