datestr=$(date +'%Y%m%d_%H%M%S')

cp ./mainwindow.ui "./ui_backup/mainwindow_${datestr}.ui"
pyuic6 -x ./mainwindow.ui -o ./ui.py