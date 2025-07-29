"""
Saves a city and buildings to a csv file
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2019 - 2025 Concordia CERC group
Project Coder Koa Wells kekoa.wells@concordia.ca
"""
import csv

class Csv:
  """
  Export to a csv file
  """
  def __init__(self, city, path):
    """
    :param city: the city object to export
    :param path: the path to export results
    """

    self._city = city
    self._file_path = path
    self._headers = ['name',
                     'function',
                     'year_of_construction',
                     'height',
                     'number_of_storeys',
                     'footprint_area',
                     'total_area',
                     'energy_system',
                     'aliases']
    self._energy_columns = ['cooling_peak_load',
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
    self._headers_written = False
    self._export()

  def _export(self):
    """
    Export the city to a csv file
    :return: None
    """
    with open(self._file_path, 'w', newline='') as csv_file:
      csv_writer = csv.writer(csv_file, delimiter=',',)

      for building in self._city.buildings:
        row = []

        name = building.name
        function = building.function
        year_of_construction = building.year_of_construction
        height = building.max_height
        number_of_storeys = building.storeys_above_ground
        footprint_area = building.floor_area
        total_area = footprint_area * number_of_storeys
        energy_system = "N/A"
        if building.energy_systems_archetype_name is not None:
          energy_system = building.energy_systems_archetype_name
        aliases = building.aliases

        row.append(name)
        row.append(function)
        row.append(year_of_construction)
        row.append(height)
        row.append(number_of_storeys)
        row.append(footprint_area)
        row.append(total_area)
        row.append(energy_system)
        row.append(aliases)

        for energy_column in self._energy_columns:
          if getattr(building, energy_column):
            for key in getattr(building, energy_column).keys():
              if not self._headers_written:
                if f'{key}_{energy_column}' not in self._headers:
                  unit = ''
                  if 'peak' in energy_column:
                    unit = '(kW)'
                  elif 'demand' in energy_column or 'consumption' in energy_column:
                    unit = '(J)'
                  self._headers.append(f'{key}_{energy_column} {unit}')
              energy_values = getattr(building, energy_column)[key]
              for energy_value in range(len(energy_values)):
                energy_values[energy_value] = float(energy_values[energy_value])
              row.append(energy_values)

        if not self._headers_written:
          csv_writer.writerow(self._headers)
          self._headers_written = True
        csv_writer.writerow(row)