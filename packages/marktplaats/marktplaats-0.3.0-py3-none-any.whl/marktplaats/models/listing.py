import warnings
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from marktplaats.models import ListingSeller, ListingFirstImage
from marktplaats.models.listing_image import fetch_listing_images
from marktplaats.models.listing_location import ListingLocation
from marktplaats.models.price_type import PriceType


@dataclass
class Listing:
    id: str
    title: str
    description: str
    date: Optional[datetime]
    seller: ListingSeller
    location: ListingLocation
    price: float
    price_type: PriceType
    link: str
    _images: list[ListingFirstImage]
    category_id: int
    attributes: list
    extended_attributes: list

    @property
    def images(self) -> list[ListingFirstImage]:
        warnings.warn("Listing.images is deprecated since marktplaats version 0.3.0. "
                      "Please use Listing.first_image or Listing.get_images() instead.",
                      category=DeprecationWarning,
                      stacklevel=2)
        return self._images

    @property
    def first_image(self) -> ListingFirstImage | None:
        try:
            return self._images[0]
        except IndexError:
            # there seem to be no images in the listing, so return None
            return None


    def get_images(self) -> list[str]:
        return fetch_listing_images(self.id)

    def __eq__(self, other):
        if not isinstance(other, Listing):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def price_as_string(self, euro_sign: bool = True, lang: str = "en") -> str:
        return self.price_type._as_string(self.price, euro_sign, lang)
