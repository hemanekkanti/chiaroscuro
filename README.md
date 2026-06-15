# chiaroscuro
Dufour shading (commonly known as Dufour map shading or Swiss style relief shading) is a cartographic technique used to create a realistic, three-dimensional illusion of mountain topography on flat maps. The technique is named after General Guillaume-Henri Dufour, a Swiss cartographer, engineer, and army general who supervised the creation of the Topographic Map of Switzerland (the "Dufour Map") between 1845 and 1865.

## What's so special about Dufour Shading?
Traditional historical maps used rudimentary hatching lines (hachures) to indicate slope steepness, which often made maps look cluttered and difficult to read. Dufour revolutionized this by introducing a highly artistic yet systematic method of hachure shading based on a specific lighting model:

- *North-West Illumination*: The landscape is drawn under the assumption that a light source (like the sun) is shining from the upper-left corner of the map (North-West) at a 45° angle. This is not technically or geographically accurate, but it has been theorized that this angle of shading works best for human perception.

- *Light vs. Shadow*: Slopes facing the North-West are left white or lightly shaded, while slopes facing the South-East fall into deep shadow.

- *Variable Line Thickness*: Instead of standard contours, cartographers used finely engraved parallel lines. The steeper the slope in the shadow, the thicker and closer together the lines were drawn.By masterfully blending these hachures, Dufour's team achieved a stark chiaroscuro (light and dark) effect that made the Swiss Alps visually "pop" off the paper, offering unparalleled depth perception for military and civilian navigation.

## How about the modern digital age?
While Dufour shading was executed entirely by hand using copperplates and lithographic stones, its underlying logic forms the backbone of modern GIS (Geographic Information Systems) and computer graphics. Today's digital hillshading (or shaded relief) uses elevation data (DEMs) to calculate light reflectance mathematically. The fundamental equation for calculating the brightness of a surface point mimics Dufour's traditional lighting framework using Lambert's Cosine Law:

$$
I = I_p \cdot k_d \cdot (\hat{N} \cdot \hat{L})
$$

Where:

- $I$ is the calculated shading intensity of the pixel.
- $I_p$ is the intensity of the light source.
- $k_d$ is the diffuse reflection coefficient of the terrain material.
- $\hat{N}$ is the surface normal vector (the direction the slope faces).
- $\hat{L}$ is the normalized light direction vector (traditionally hardcoded to the north-west in cartography).
