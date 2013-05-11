echo "Removing all .pyc files";
rm -r ./*.pyc
echo "Starting GUI"
python GUI/gui.py &
echo "Starting GPS Module"
python GUI/modules/gps_module.py &
echo "GUI Started, launching Receptionist"
