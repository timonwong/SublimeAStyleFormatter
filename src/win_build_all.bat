@echo off
:: Windows SDK for Windows 7 (7.0) should be installed first.
:: And the "%VS90COMNTOOLS%" enviornment variable should be set correctly.
:: NOTE: For Python 3.3, MSVC 10 is required for building.

:: Configuration
set PYTHON26_X86="F:\Langs\Python26\python.exe"
set PYTHON26_X64="F:\Langs\Python26_x64\python.exe"
set PYTHON33_X86="F:\Langs\Python33\python.exe"
set PYTHON33_X64="F:\Langs\Python33_x64\python.exe"

:: Clean
:: if exist pyastyle\build rmdir /s /q pyastyle\build > NUL

call :buildExtension %PYTHON26_X86%
call :buildExtension %PYTHON26_X64%
call :buildExtension %PYTHON33_X86%
call :buildExtension %PYTHON33_X64%
goto done

:buildExtension

setlocal

if not exist %~1 (
    echo Python executable "%~1" cannot be found.
    goto buildExtensionReturn
)

set PY_PRINT_VERSION=%~1 -c "import sys;print('.'.join(map(lambda x: str(x), sys.version_info[:2])))"
set PY_PRINT_32OR64=%~1 -c "import struct;print(8 * struct.calcsize('P'))"
for /f "tokens=*" %%i in ('%PY_PRINT_VERSION%') do set PY_VERSION=%%i
for /f "tokens=*" %%i in ('%PY_PRINT_32OR64%') do set PY_32OR64=%%i

if "%PY_32OR64%" == "32" (
    set PY_BUILD_ARCH=32
)

if "%PY_32OR64%" == "64" (
    set PY_BUILD_ARCH=-amd64
)

set PY_VERSION_OK=0
set MSSdk=
set DISTUTILS_USE_SDK=

if "%PY_VERSION%" == "2.6" (
    set PY_VERSION_OK=1
    set PY_VERSION_MAJOR=2

    set MSSdk=1
    set DISTUTILS_USE_SDK=1

    if "%PY_32OR64%" == "32" (
        call "%VS90COMNTOOLS%\vcvars32.bat"
    )

    if "%PY_32OR64%" == "64" (
        call "%VS90COMNTOOLS%\vcvars64.bat"
    )
)

if "%PY_VERSION%" == "3.3" (
    set PY_VERSION_OK=1
    set PY_VERSION_MAJOR=3
)

if "%PY_VERSION_OK%" == "0" (
    echo "Invalid python version: %PY_VERSION%"
    goto buildExtensionReturn
)

set OUTPUT_FILE=pyastyle\build\lib.win%PY_BUILD_ARCH%-%PY_VERSION%\pyastyle.pyd
set TARGET_DIR=..\pyastyle\python%PY_VERSION_MAJOR%\_win%PY_32OR64%\

cd pyastyle
:: Compilation
%~1 setup.py build --compiler=msvc
cd ..

if not exist %TARGET_DIR% mkdir %TARGET_DIR%
copy /y %OUTPUT_FILE% %TARGET_DIR%
echo Finished building extension for Python %PY_VERSION% (%PY_32OR64%bit)
echo.

:buildExtensionReturn
endlocal
goto :eof

:done
