"""
ExportsFactory export a city and the buildings of a city
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2019 - 2025 Concordia CERC group
Code Contributor: Koa Wells kekoa.wells@concordia.ca
"""

from pathlib import Path

from hub.exports.results_factory_formats.csv import Csv
from hub.exports.results_factory_formats.geojson import Geojson
from hub.helpers.utils import validate_import_export_type


class ResultsExportFactory:
  """
  Exports factory class for results and hub building data
  """

  def __init__(self, city, handler, path):
    """
    :param city: the city object to export
    :param handler: the handler object determine output file format
    :param path: the path to export results
    """

    self._city = city
    self._handler = '_' + handler.lower()
    validate_import_export_type(ResultsExportFactory, handler)
    if isinstance(path, str):
      path = Path(path)
    self._path = path

  def _csv(self):
    """
    Export city results to csv file
    :return: none
    """
    return Csv(self._city, self._path)

  def _geojson(self):
    """
    Export city results to a geojson file
    :return: none
    """
    return Geojson(self._city, self._path)

  def _parquet(self):
    """
    Export city results to a parquet file
    :return: none
    """
    # todo: add parquet handler
    raise NotImplementedError()

  def export(self):
    """
    Export the city given to the class using the given export type handler
    :return: None
    """
    _handlers = {
      '_csv': self._csv,
      '_geojson': self._geojson,
      '_parquet': self._parquet
    }
    return _handlers[self._handler]()
