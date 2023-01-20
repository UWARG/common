script_path=$(dirname $0)

rm $script_path/../Inc/Messages.hpp

echo "#pragma once\n\n" >> $script_path/../Inc/Messages.hpp

echo "const uint8_t START_FLAG = 0x7e;\n\n" >> $script_path/../Inc/Messages.hpp

for FILE in $script_path/../Inc/messages/*; do
    echo "including $FILE"
    echo "#include \"messages/$(basename $FILE)\"" >> $script_path/../Inc/Messages.hpp
done   

echo "\n" >> $script_path/../Inc/Messages.hpp

for FILE in $script_path/../Inc/helpers/*; do
    echo "including $FILE helper"
    echo "#include \"helpers/$(basename $FILE)\"" >> $script_path/../Inc/Messages.hpp
done   

echo "\n" >> $script_path/../Inc/Messages.hpp