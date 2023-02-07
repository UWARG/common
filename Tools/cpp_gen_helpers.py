# importing the module
import json
import os
import sys



loc = os.path.realpath(os.path.dirname(__file__))

# if not os.path.exists(loc + '/..//helpers'):
#     print("creating helpers folder")
#     os.mkdir(loc + '/../Inc/helpers')

with open(loc + '/helper.template', 'r') as file: 
    template_string = file.read()
# Opening JSON file
    with open(loc + '/../TelemMessages/messages.json') as json_file:
        data = json.load(json_file)
        for msg in data:
            length = msg["length"].to_bytes(2, byteorder='big')
            file_contents = template_string

            file_contents = file_contents.replace("{{name}}", msg["name"])
            file_contents = file_contents.replace("{{type}}", str(msg["type"]))
            file_contents = file_contents.replace("{{length_0}}", str(length[0]))
            file_contents = file_contents.replace("{{length_1}}", str(length[1]))

            output_file_path = loc + '/../cpp/TelemMessages/' + msg["name"] + "_helper.hpp"

            if os.path.exists(output_file_path):
                print("deleting " + msg["name"] + " helper file")
                os.remove(output_file_path)
                
            output_file = open(output_file_path, "w")

            output_file.write(file_contents)
            output_file.close()
