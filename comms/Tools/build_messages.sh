script_path=$(dirname $0)

if [ $# = 0 ]; then 
    echo "no args passed, exiting"
    exit
fi

# for python you must pass a location for the built files
if [ $1 = "python" ]; then  
    echo "building python messages"
    for FILE in $script_path/../TelemMessages/*.lcm; do
        echo "building .py for $FILE"
        lcm-gen --python --ppath $script_path/../py/ $FILE
    done   
    python3 $script_path/py_gen_helpers.py
elif [ $1 = "cpp" ]; then
    echo "building c++ messages"
    for FILE in $script_path/TelemMessages/*; do
        echo "building .hpp for $FILE"
        lcm-gen --cpp --cpp-hpath $script_path/../cpp/TelemMessages $FILE
    done   
    exec $script_path/message_include.sh
elif [ $1 = "clean" ]; then
    echo "cleaning messages"
    rm -r $script_path/../cpp/TelemMessages
    rm -r $script_path/../py/TelemMessages

else 
    echo "arg not recognized. exiting"
    exit
fi