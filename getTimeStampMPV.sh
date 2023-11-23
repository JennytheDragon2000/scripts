dir_to_load="/tmp/mpv"
filename=$(ls -R $dir_to_load | dmenu -l 20 -p "Select the File")
echo $filename
timestamp=$(echo $filename | awk -F ',' '{print $3}')
# filename=$(echo $filename | awk -F ',' '{print $2}' | tr '\' '/')
filename=$(echo $filename | awk -F ',' '{print $2}' | tr '\\\\' '/')
echo $filename
echo $timestamp
mpv --pause "$filename" --start=$timestamp


