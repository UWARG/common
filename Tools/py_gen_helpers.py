# importing the module
import json
import os
import sys


def search_in_file(phrase, f):
    for (i, line) in enumerate(f):
        if phrase in line:
            return i
    return -1



loc = os.path.realpath(os.path.dirname(__file__))

msg_path = loc + '/../TelemMessages/'
py_path = loc + '/../py/TelemMessages/'



helper = "import TelemMessages\n\n"
helper = helper + "def decode_msg(buf):\n\t"
helper = helper + "raw_data = buf.getbuffer().tobytes()\n\t"

# open json file
with open(msg_path + 'messages.json') as json_file:
    data = json.load(json_file)
    for msg in data:
        length = msg["length"].to_bytes(2, byteorder='big')
         
        with open(py_path + msg["name"] + '.py', 'r+') as fd:
            contents = fd.readlines()
            print("opened " + msg["name"])

            # find line number of phrase
            index = search_in_file(phrase="self.header", f=contents)
            if index == -1:
                print("phrase not found in file, its broken")
                quit()
            print(index)
            contents.insert(index + 1, "        self.header.flag = 0x7e\n")
            contents.insert(index + 2, "        self.header.type = " + hex(msg["type"]) + "\n")
            contents.insert(index + 3, "        self.header.length = bytes([ " + hex(length[0]) + ", " + hex(length[1]) + " ])\n")

            fd.seek(0)
            fd.writelines(contents)

            helper = helper + "if raw_data[3] == " + hex(msg["type"]) + ":\n\t\t"
            helper = helper + "return TelemMessages." + msg["name"] + "()._decode_one(buf)\n\tel"

helper = helper + "se:\n\t\treturn None"
output_file = open(py_path + "../helper.py", "w")

output_file.write(helper)
output_file.close()
