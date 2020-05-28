from django.db import models

from .models.base import PictureWrapper
from .models.CarouselImage import CarouselImage
from .models.Officer import Officer
from .models.Player import Player
from .models.VegaChessEntry import VegaChessEntry
# __all__ = ['PictureWrapper', 'CarouselImage', 'Officer', 'Player', 'VegaChessEntry']
class EmptyModel(models.Model):
    bytes = models.BinaryField()
