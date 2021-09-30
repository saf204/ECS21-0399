README:
All code is presented as is.  Meaning it could be cleaned up but it runs as 
currently written.
Questions can be directed to Steve Flanagan at sflanagan@talltimbers.org
The code to generate figures was originally written to be universal for all
LANDIS-II runs, and generally has a "start user input" and "end user input"
section where the user should not change the code below it.  In my time finalizing
this work I likely hardcoded something below this line that would alter the findings
of a different LANDIS-II run.  The upkeep of keeping everything universal began to
outweigh my time.  As I found limited examples of people sharing their code I was 
trying to make this universal, but as mentioned that might not be the case anymore,
but should serve as a decent starting place for other users.



LANDIS-II RUNS

There are also many areas in the code that could be cleaned up, but are simply
commented out.  Code runs fine though.

TWO things need to be changed to do a run:

The "biomassharvest_prescribedfire_SB" file in the Input directory 
should have the appropriate scenario applied to all management areas.
There are numerous extra scenarios that were generated for this study
that have not been completely removed from the code.  They can be ignored.
For wildfire scenarios in the "Prescription Wildfire" set the 
"MinimumTimesSinceLastHarvest" to the desired start year and in the 
"HarvesImplementations" have this as the scenario that is called with the 
appropriate "Begin Time".
Prescribed fire is the "Fire2yr" prescription and can simple be turned on
and the wildfire prescription turned off.
Fire supression is all prescriptions off, or a "Begin Time" that starts after
your final simulation year.

The "biomass_reductions_SB" file in the Input directory needs the correct
consumption values fdepending on if you are simulating prescribed or wildfire.
Prescribed fire is noted with a comment "otterman pr" and wilfire
with "regelbrugge blue ridge" and "reinhardt"


Additionally, the BatchFile should have the output name changed to whatever is desired.

For example:
FOR %%a IN (%list%) DO (mkdir=%homedir%\Output\rep_%%a & cd %homedir%\Output\rep_%%a . . . )
Becomes             DO (mkdir=%homedir%\Output\noburn%%a & cd %homedir%\Output\noburn_%%a . . . )

The list above this for loop can be added to if additional runs are desired.



LANDIS-II MODEL_OUTPUT

Five output files for each run
wf_# . . . is the wildfire return interval and number run
pf_ . . . is prescribed fire
nf_ . . . is fire exclusion or no fire
"ottmer" means nothing.  Just a name we were using that happened to correspond with our final runs.



PYTHON SCRIPTS AND OUTPUT

All scripts used to produce figures for the manuscript generate more images than are used.
So the following by figure will be the script name that generated it, and the folder that the image
and some additional graphs are stored.
Scripts are in "python scripts\images_for_paper" folders in "python_output"

Figure 2	landis_necn_graphs.py				necn_graphs
Figure 3	landis_weighted_spp_graphs_multiruns.py		temp_images_multruns
Figures 4/5	landis_necn_harvest_graphs.py			necn_harvest_graphs



Earlier versions of scripts that may be useful but did not produce figures for the manuscript 
are found in "python_scripts\additional_scripts"
They have not been checked to see if they run or what they produce, but were part of the process
in developing the final scripts.


LANDIS_Installers

The LANDIS_Installers directory should have every extension you need to run this version of the code.
We work on multiple projects so if anything there are more packages listed than might actually be
needed.  Please contact me if you believe a package is missing.
