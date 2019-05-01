#!/bin/bash
echo "Creating .egg file......."
python setup.py bdist_egg
echo "Installing .egg file....."
sudo easy_install ./dist/*.egg
echo "Deleting build folder"
rm -rf Oggy.egg-info
rm -rf build


