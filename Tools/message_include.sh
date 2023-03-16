script_path=$(dirname $0)
loc_msgs=../cpp/TelemMessages

rm $script_path/$loc_msgs/Messages.h

echo $'#pragma once\n' >> $script_path/$loc_msgs/Messages.h

echo $'const uint8_t START_FLAG = 0x7e;\n' >> $script_path/$loc_msgs/Messages.h

for FILE in $script_path/$loc_msgs/*.hpp; do
    echo "including $FILE"
    sed -i 's%<lcm/lcm_coretypes.h>%"lcm_coretypes.h"%g' $FILE
    sed -i 's%TelemMessages/%%g' $FILE
    echo "#include \"$(basename $FILE)\"" >> $script_path/$loc_msgs/Messages.h
done   

echo $'\n' >> $script_path/$loc_msgs/Messages.h