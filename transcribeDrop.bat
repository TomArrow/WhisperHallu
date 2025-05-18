call C:\ProgramData\Anaconda3\Scripts\activate.bat C:\ProgramData\Anaconda3
rem call conda activate base
cd %~dp0
FOR %%A IN (%*) DO (
	mkdir "%%~dA%%~pAtranscripts"
	python "path\do.py" "%%~A" "%%~dA%%~pAtranscripts\%%~nA.wav" "turbo"
)

pause