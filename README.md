# Particle filter for lps tag (proof of concept)


## Flow
1. Get map with anchors (possible to add and remove under ongoing preocess)
2. Init m particles uniformly on the map ··
···Particles will have:··
··* position: {x,y,z}
··* state vector: [{addr:<addr>, ddist:<ddist>},{addr:<addr>,...}] (calculated from {x,y,z})
··* Weight: w (normalized)
3. Calculate the weight ··
···The weight is calculated by the multidimensionall gauss distrubution where the axises are representing one anchor.
4. The weight is normalized (w_i/sum(w_i)=weight)
5. Resample particles (low variance sampling)
6. Move particles according to accelerometer/gyro
7. Calculate new state vector
8. Go back to step 3


## Assumptions
* Measurments form anchors (ddist) is uncorelated (if sigma matrix is diagonal)
* Measurments are normal distributed
