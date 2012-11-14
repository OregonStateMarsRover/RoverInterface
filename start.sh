echo "Initializing USB ownership..."
./InitScripts/initUSB.sh
echo "Starting XBox Controller Parser"
python xboxcontroller_parser.py
