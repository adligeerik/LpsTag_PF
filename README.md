# Particle filter for lps tag (proof of concept)


## Flow
1. Get map with anchors (possible to add and remove under ongoing process)
2. Init m particles uniformly on the map ··
···Particles will have:··
··* position: {x,y,z}
··* state vector: [{addr:<addr>, ddist:<ddist>},{addr:<addr>,...}] (calculated from {x,y,z})
··* Weight: w (normalized)
3. Calculate the weight ··
···The weight is calculated by the multidimensional Gauss distribution where the axes are representing one anchor.
4. The weight is normalized (w_i/sum(w_i)=weight)
5. Re-sample particles (low variance sampling)
6. Move particles according to accelerometer/gyro
7. Calculate new state vector
8. Go back to step 3


## Assumptions
* Measurements form anchors (ddist) is uncorrelated (Sigma matrix is diagonal)
* Measurements are normal distributed
* The tag will have had the same acceleration from the previous measurement until the latest measurement
* Accelerometer has the same variance for all axis 


## Miscellaneous
If all anchors are in or close to be in the same plane, the tag will have a good estimate of the position in that plane, but not in the third axis perpendicular from the plane.
