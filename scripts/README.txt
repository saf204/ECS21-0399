These are what each script creates.

nee_landis_and_ED_flux.py
Monthly, yearly, and average flux plots compared to the towers.
stored in images\flux_imgs\
The image for the paper is ED and LANDIS on the same plot comparing their monthly predictions to the data.
It is stored in images\final_images\ as flux_final

landis_and_ed_species_and_agb
Combination of many codes:
landis_weighted_spp_graphs_multiruns.py + ED_biomass.py and part of landis_biomass_weighted_multruns.
spp_graphs produced longleaf vs other species previously. It was modified to also produce species graphs.
ED_biomass produced longleaf vs other species and total AGB
biomass_weighted was previously used for LANDIS AGB but is now contained in this script.
Many individual plots by ecoregion, species, scenario . . .
The main images we want from this are now/will be if run, saved in the final_images folder
landis_and_ED_AGB, landis_and_ED_longleaf_vs_species, and a folder for landis "species_by_scenario"