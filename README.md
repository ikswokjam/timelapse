# timelapse 

Klein script voor op de Raspberry Pi een timelapse te maken her en der geleend have fun.


mkdir ~/timelapse

mkdir ~/timelapse/scripts
mkdir ~/timelapse/scripts/foto

virtualenv --python=python3 ~/timelapse

cd timelapse/

your script should also by in this directory

source ./bin/activate

pip install -r requirements.txt

python timelapse_fromdawntilldusk.py