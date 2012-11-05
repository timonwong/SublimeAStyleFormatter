::@echo off
:: Windows SDK for Windows 7 (7.0) should be installed first.
:: And the "%VS90COMNTOOLS%" enviornment variable should be set correctly.

:: Configuration
set PYTHON32="F:\Langs\Python26\python.exe"
set PYTHON64="F:\Langs\Python26_x64\python.exe"

set MSSdk=1
set DISTUTILS_USE_SDK=1

if not exist ..\_win32 mkdir ..\_win32
if not exist ..\_win64 mkdir ..\_win64

:: Clean
rmdir /s /q pyastyle\build

setlocal
call "%VS90COMNTOOLS%\%vcvars32.bat"
cd pyastyle
%PYTHON32% setup.py build
cd ..
endlocal

setlocal
call "%VS90COMNTOOLS%\vcvars64.bat"
cd pyastyle
%PYTHON64% setup.py build
cd ..
endlocal

copy /y pyastyle\build\lib.win32-2.6\pyastyle.pyd ..\_win32\
copy /y pyastyle\build\lib.win-amd64-2.6\pyastyle.pyd ..\_win64\

