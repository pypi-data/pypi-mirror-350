"""
Saves a city and buildings to a geojson file
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2019 - 2025 Concordia CERC group
Project Coder Koa Wells kekoa.wells@concordia.ca
"""
import json
from pathlib import Path

from hub.exports.formats.geojson import Geojson as GeojsonFormat

class Geojson:
  """
  Export to a geojson file
  """
  def __init__(self, city, path):
    """
    :param city: the city object to export
    :param path: the path to export results
    """
    self._city = city
    self._path = path
    self._output_file = Path(f'{self._path}/{self._city.name}.geojson').resolve()
    self._building_properties = ['name',
                                 'year_of_construction',
                                 'height',
                                 'number_of_storeys',
                                 'footprint_area',
                                 'total_area',
                                 'energy_system',
                                 'aliases']
    self._building_energy_results = ['cooling_peak_load',
                                     'heating_peak_load',
                                     'lighting_peak_load',
                                     'appliances_peak_load',
                                     'cooling_demand',
                                     'heating_demand',
                                     'lighting_electrical_demand',
                                     'appliances_electrical_demand',
                                     'domestic_hot_water_heat_demand',
                                     'heating_consumption',
                                     'cooling_consumption',
                                     'domestic_hot_water_consumption',
                                     'distribution_systems_electrical_consumption']
    self._export()

  def _export(self):
    """
    Export the city to a geojson file
    :return: None
    """
    GeojsonFormat(self._city, self._path,  self._city.buildings)
    with open(self._output_file, 'r') as f:
      city = json.load(f)
      buildings = city['features']

    count = 0
    for building in buildings:
      name = building['id']
      count += 1
      for city_object in self._city.buildings:
        if city_object.name == name:
          height = city_object.max_height
          number_of_storeys = city_object.storeys_above_ground
          footprint_area = city_object.floor_area
          total_area = footprint_area * number_of_storeys
          energy_system = city_object.energy_systems_archetype_name
          aliases = city_object.aliases

          building['properties']['name'] = name
          building['properties']['height'] = height
          building['properties']['number_of_storeys'] = number_of_storeys
          building['properties']['footprint_area'] = footprint_area
          building['properties']['total_area'] = total_area
          building['properties']['energy_system'] = energy_system
          building['properties']['aliases'] = aliases

          for energy_result in self._building_energy_results:
            result = getattr(city_object, energy_result)
            if result:
              for key, energy_values in result.items():
                unit = ''
                if 'peak' in energy_result:
                  unit = '(kW)'
                elif 'demand' in energy_result or 'consumption' in energy_result:
                  unit = '(J)'
                building['properties'][f'{key}_{energy_result} {unit}'] = energy_values
          break

    with open(self._output_file, 'w') as output_file:
      output_file.write(json.dumps(city, indent=2))