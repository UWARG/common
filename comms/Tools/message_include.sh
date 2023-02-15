script_path=$(dirname $0)
loc_msgs=../cpp/TelemMessages

rm $script_path/$loc_msgs/Messages.hpp

echo "#pragma once\n\n" >> $script_path/../Inc/Messages.hpp

echo "const uint8_t START_FLAG = 0x7e;\n\n" >> $script_path/$loc_msgs/Messages.hpp

for FILE in $script_path/../Inc/messages/*; do
    echo "including $FILE"
    echo "#include \"messages/$(basename $FILE)\"" >> $script_path/$loc_msgs/Messages.hpp
done   

echo "\n" >> $script_path/$loc_msgs/Messages.hpp