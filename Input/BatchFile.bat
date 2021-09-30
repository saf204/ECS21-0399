rem The 'rem' keyword indicates that this is a remark

rem Batch File to Run a Scenario 
set homedir="C:\Users\sflanagan\Desktop\landis_runs\100m_final"
set scenariofile=scenario_100m_SB.txt

rem Set the directory with the input files
set inputdir=%homedir%\Input

pause
rem loop through rep
set list=1 2 3 4 5 
FOR %%a IN (%list%) DO (mkdir=%homedir%\Output\wf_50_ottmer_300yrs%%a & cd %homedir%\Output\wf_50_ottmer_300yrs%%a & call landis-ii %inputdir%\%scenariofile%)

pause
 