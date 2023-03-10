"""
Generates the helper.py file
"""

import json
import os
import sys


def search_in_file(phrase: str, lines: list) -> int:
    """
    Searches for string in each line
    """
    for (i, line) in enumerate(lines):
        if phrase in line:
            return i
    return -1


def replace_import(directory: str):
    """
    Replace absolute imports with relative imports
    """
    file_names = [f for f in directory if (str(f))[-3:] == ".py"]
    for file_name in file_names:
        with open(module_path + file_name, "r+") as fd:
            contents = fd.readlines()
            print("Opened " + file_name)

            # Get locations
            import_index = search_in_file("import TelemMessages.", contents)
            class_index = search_in_file("class", contents)
            if import_index == -1 or class_index == -1 or class_index < import_index:
                print("import and/or class not found, skip")
                continue

            # Replace import
            contents[import_index] = "from .. import TelemMessages\n"
            # Replace with empty lines
            for i in range(import_index + 1, class_index):
                contents[i] = "\n"

            fd.seek(0)
            fd.writelines(contents)
            fd.truncate()


def decoder_header() -> str:
    """
    Part of generating decode_msg()
    """
    decoder = "def decode_msg(buf):\n"
    decoder += "    \"\"\"\n"
    decoder += "    Returns message class based on header type\n"
    decoder += "    \"\"\"\n"
    decoder += "\n"
    decoder += "    raw_data = buf.getbuffer().tobytes()\n"
    # Spaces before if
    decoder += "    "
    return decoder


def decoder_append(message_type: str, message_name: str) -> str:
    """
    Part of generating decode_msg()
    """
    # if or elif with spaces
    decoder = "if raw_data[3] == " + message_type + ":\n"
    decoder += "        return TelemMessages." + message_name + "()._decode_one(buf)\n"
    decoder += "    el"
    return decoder


def decoder_footer() -> str:
    """
    Part of generating decode_msg()
    """
    decoder = "se:\n"
    decoder += "        return None\n"
    return decoder


def picker_header(num_types_of_messages: int) -> str:
    """
    Part of generating message_picker() for testing
    """
    picker = "def message_picker(i: int):\n"
    picker += "    \"\"\"\n"
    picker += "    Returns message class based on modulus\n"
    picker += "    \"\"\"\n"
    picker += "\n"
    picker += "    message = i % " + str(num_types_of_messages) + "\n"
    # Spaces before if
    picker += "    "
    return picker


def picker_append(message_type: str, message_name: str) -> str:
    """
    Part of generating message_picker() for testing
    """
    # if or elif with spaces
    picker = "if message == " + message_type + ":\n"
    picker += "        return TelemMessages." + message_name + "()\n"
    picker += "    el"
    return picker


def picker_footer() -> str:
    """
    Part of generating message_picker() for testing
    """
    picker = "se:\n"
    picker += "        return None\n"
    return picker


if __name__ == "__main__":
    loc = os.path.realpath(os.path.dirname(__file__))

    msg_path = loc + '/../TelemMessages/'
    module_path = loc + '/../modules/TelemMessages/'

    # Import replacement required for submodule support
    print("Import replacement")
    replace_import(os.listdir(module_path))

    helper = "\"\"\"\n"
    helper += "Autogenerated helper functions\n"
    helper += "\"\"\"\n"
    helper += "\n"
    helper += "from . import TelemMessages\n"
    helper += "\n"
    helper += "\n"

    # Build helper function strings
    decoder = decoder_header()
    picker = None

    # Open JSON file containing metadata
    with open(msg_path + "messages.json") as json_file:
        data = json.load(json_file)
        picker = picker_header(len(data))
        for msg in data:
            length = msg["length"].to_bytes(2, byteorder="big")

            # Open each message class
            with open(module_path + msg["name"] + ".py", "r+") as fd:
                contents = fd.readlines()
                # print("opened " + msg["name"])

                # Insert helper methods for message identification
                index = search_in_file("self.header", contents)
                if index == -1:
                    print("self.header not found in file!")
                    sys.exit(-1)

                print(index)
                contents.insert(index + 1, "        self.header.flag = 0x7e\n")
                contents.insert(index + 2, "        self.header.type = " + hex(msg["type"]) + "\n")
                contents.insert(index + 3, "        self.header.length = bytes([ " + hex(length[0]) + ", " + hex(length[1]) + " ])\n")

                if "lists" in msg.keys():
                    for key, value in msg["lists"].items():
                        index = search_in_file("self." + key, contents)
                        if index != -1:
                            contents[index] = "        self." + key + " = bytes(" + str(value)  + ")\n"

                fd.seek(0)
                fd.writelines(contents)
                fd.truncate()

                decoder += decoder_append(hex(msg["type"]), msg["name"])
                picker += picker_append(hex(msg["type"]), msg["name"])

    decoder += decoder_footer()
    picker += picker_footer()

    helper += decoder
    helper += "\n"
    helper += "\n"
    helper += picker

    output_file = open(module_path + "../helper.py", "w")

    output_file.write(helper)
    output_file.close()
