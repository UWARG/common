script_path=$(dirname $0)

if [ $# = 0 ]; then 
    echo "no args passed, exiting"
    exit
fi

# for python you must pass a location for the built files
if [ $1 = "python" ]; then  
    echo "building python messages"
    if [ $# != 2 ]; then
        echo "python option needs a location argument. Not enough args. Exiting"
        exit
    fi
    for FILE in $script_path/../Inc/Msgs/*; do
        echo "building .py for $FILE"
        lcm-gen --python --ppath $2 $FILE
    done   
elif [ $1 = "cpp" ]; then
    echo "building c++ messages"
    for FILE in $script_path/../Inc/Msgs/*; do
        echo "building .hpp for $FILE"
        lcm-gen --cpp --cpp-hpath $script_path/../Inc/ $FILE
    done   
    exec $script_path/message_include.sh
elif [ $1 = "clean" ]; then
    echo "cleaning messages"
    rm -r $script_path/../Inc/messages
else 
    echo "arg not recognized. exiting"
    exit
fi