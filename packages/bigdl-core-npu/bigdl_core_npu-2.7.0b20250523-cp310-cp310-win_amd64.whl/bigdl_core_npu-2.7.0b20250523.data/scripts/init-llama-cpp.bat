@echo off
for /f "delims=" %%i in ('python -c "import importlib; print(importlib.import_module('bigdl-core-npu').__file__)"') do set "cpp_file=%%i"
for %%a in ("%cpp_file%") do set "cpp_dir=%%~dpa"

set "cpp_dir=%cpp_dir:~0,-1%"
set "lib_dir=%cpp_dir:bigdl-core-npu=intel_npu_acceleration_library%\lib\Release"
set "destination_folder=%cd%"

pushd "%lib_dir%"
for %%f in (*) do (
    if exist "%destination_folder%\%%~nxf" (
        del /f "%destination_folder%\%%~nxf"
    )
    mklink "%destination_folder%\%%~nxf" "%%~ff"
)
popd

pushd "%cpp_dir%"
for %%f in (*) do (
    if not "%%f"=="llama-cli-npu.exe" (
        if exist "%destination_folder%\%%~nxf" (
            del /f "%destination_folder%\%%~nxf"
        )
        mklink "%destination_folder%\%%~nxf" "%%~ff"
    )
)
popd

copy "%cpp_dir%\llama-cli-npu.exe" .
