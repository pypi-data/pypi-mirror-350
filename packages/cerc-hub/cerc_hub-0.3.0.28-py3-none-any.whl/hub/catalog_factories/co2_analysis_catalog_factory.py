"""
CO2 analysis catalog factory
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2019 - 2025 Concordia CERC group
Project Coder Koa Wells kekoa.wells@concordia.ca
"""

from pathlib import Path
from typing import TypeVar

from hub.catalog_factories.co2_analysis.hub_catalog import HubCatalog
from hub.helpers.utils import validate_import_export_type

Catalog = TypeVar('Catalog')


class Co2AnalysisCatalogFactory:
  """
  Co2AnalysisCatalogFactory class
  """
  def __init__(self, handler, base_path=None):
    if base_path is None:
      base_path = Path(Path(__file__).parent.parent / 'data/co2_analysis')
    self._handler = '_' + handler.lower()
    validate_import_export_type(Co2AnalysisCatalogFactory, handler)
    self._path = base_path

  @property
  def _hub_catalog(self):
    """
    Retrieve Hub CO2 analysis catalog
    """
    return HubCatalog(self._path)

  @property
  def catalog(self) -> Catalog:
    """
    Return a Co2Analysis catalog
    :return: Co2Analysis Catalog
    """
    _handlers = {
      '_hub_catalog': self._hub_catalog
    }
    return _handlers[self._handler]

