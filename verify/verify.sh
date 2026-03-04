export PW=`pwd`
python -m venv ufswm
     source ufswm/bin/activate
cd  $PW
python cmp.py  ./verify_hafs/T2O_2020092200_17L/control.sys_python/sfcf015.nc ./verify_hafs/T2O_2020092200_17L/butterfly.sys_python/sfcf015.nc  ./T2O_2020092200_17L/sfcf015.nc


