from geoseeq.dashboard.dashboard import Dashboard
from geoseeq import Knex
from geoseeq.id_constructors import project_from_id

knex = Knex().load_profile("dev")
proj = project_from_id(knex, "97b9ee26-3616-4557-833b-dd21f4c239f3")
dash = Dashboard(knex, proj, "Default dashboard")
dash.get()

for tile in dash.tiles:
    tile.title += "g"
dash.add_tile(tile)

dash.save()