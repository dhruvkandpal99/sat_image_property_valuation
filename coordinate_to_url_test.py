# This is a test code that you can use to check if you can still access an image from the server (i.e., have not hit server limit)

import mercantile

# Your coordinates
lat, lon = 47.5892, -122.203
zoom = 18

# Calculate Tile
tile = mercantile.tile(lon, lat, zoom)
url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{tile.y}/{tile.x}"

print("Click this link to test:")
print(url)