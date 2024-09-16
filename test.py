import geopandas as gpd
import cartagen as c4
from shapely.wkt import loads

from cartagen.utils.debug import plot_debug

buildings = [
    loads('POLYGON ((668344.9 6860328.8, 668340.6 6860333.4, 668337.3 6860330.3, 668334.7 6860333.3, 668329 6860327.9, 668336.2 6860320.7, 668344.9 6860328.8))')
]

gdf = gpd.GeoDataFrame(geometry=buildings, crs='EPSG:2154')

agents = []
for i, building in gdf.iterrows():
    # Create the agent
    agent = c4.BuildingAgent(building)

    # Adding a size constraint of 250 square meters to enlarge the building if needed
    size = c4.BuildingSizeConstraint(agent, importance=1, min_area=250)

    # Adding a granularity constraint that will simplify the building if
    # an edge is above the minimum allowed length
    granularity = c4.BuildingGranularityConstraint(agent, importance=1, min_length=6)

    # Adding a squareness constraint to square the building angles if needed
    squareness = c4.BuildingSquarenessConstraint(agent, importance=1)

    agent.constraints.append(size)
    agent.constraints.append(squareness)
    agent.constraints.append(granularity)
    agents.append(agent)

c4.run_agents(agents)

plot_debug(gdf, buildings)