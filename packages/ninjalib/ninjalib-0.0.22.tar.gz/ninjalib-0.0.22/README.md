# ninjalib is a data science library
# 
# import ninjalib
# ninja = ninjalib.ninjalib(data).anomaly()
# ninja = ninjalib.ninjalib(data,nth=0).flatten_list()
# ninja = ninjalib.ninjalib(data,nth=0).flatten_tuple()
# ninja = ninjalib.ninjalib(data).project()
# ninja = ninjalib.ninjalib(data,axis,angle).rotate_camera()
# ninja = ninjalib.ninjalib(data).mean()
# ninja = ninjalib.ninjalib(team_1,team_2).odds()
# ninja = ninjalib.ninjalib([host,port],protocol=-1).status()
# ninja = ninjalib.ninjalib(data).varint()
# 
# Notes:
# flatten_list and flatten_tuple will by default flatten down to 1D. To control this, pass the amount to flatten
# project and rotate camera are for 3D rendering on a 2D plane
# varint is for Minecraft Java
# rotate_camera accepts data as a 2D list of x,y,z coordinates, axis as a string (x,y,or,z) and an angle (90 degrees for right angle)
# odds calculates the odds of two ncaa teams. Pass the scores as a list of game points
# status returns the packets needed to query the status of a Minecraft Java server. As of 1.21.5, it is 770. -1 Queries the server protocol
