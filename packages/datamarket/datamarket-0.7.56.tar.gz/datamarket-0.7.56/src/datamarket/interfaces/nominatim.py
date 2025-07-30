########################################################################################################################
# IMPORTS

import gettext
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

import pycountry
import requests
from geopy.distance import geodesic
from jellyfish import jaro_winkler_similarity

from ..params.nominatim import POSTCODES
from ..utils.strings import normalize

########################################################################################################################
# PARAMETERS

JARO_WINKLER_THRESHOLD = 0.85

########################################################################################################################
# CLASSES

logger = logging.getLogger(__name__)
spanish = gettext.translation("iso3166-1", pycountry.LOCALES_DIR, languages=["es"])
spanish.install()


class GeoNames:
    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint

    @staticmethod
    def validate_postcode(postcode: Union[int, str]) -> Optional[str]:
        if isinstance(postcode, int):
            postcode = str(postcode)

        if postcode and len(postcode) == 5 and postcode[:2] in POSTCODES:
            return postcode

        if postcode and len(postcode) == 4:
            postcode = f"0{postcode}"
            if postcode[:2] in POSTCODES:
                return postcode

    @staticmethod
    def get_province_from_postcode(postcode: Optional[str]) -> Optional[str]:
        if postcode:
            return POSTCODES[postcode[:2]]

    def reverse(self, lat: Union[float, str], lon: Union[float, str]) -> Dict[str, Any]:
        return requests.get(f"{self.endpoint}/reverse?lat={lat}&lon={lon}", timeout=30).json()


class Nominatim:
    def __init__(self, nominatim_endpoint: str, geonames_endpoint: str) -> None:
        self.endpoint = nominatim_endpoint
        self.geonames = GeoNames(geonames_endpoint)

    @staticmethod
    def _get_attribute(raw_json: Dict[str, Any], keys: List[str]) -> Any:
        for key in keys:
            if key in raw_json:
                return raw_json[key]

    def _calculate_distance(self, lat_str: Optional[str], lon_str: Optional[str], input_coords: Tuple[float, float]) -> float:
        dist = float("inf")
        if lat_str and lon_str:
            try:
                coords = (float(lat_str), float(lon_str))
                dist = geodesic(input_coords, coords).km
            except (ValueError, TypeError):
                logger.warning("Invalid coordinates for distance calculation.")
        return dist

    def _parse_nominatim_result(self, nominatim_raw_json: Dict[str, Any]) -> Dict[str, Optional[str]]:
        raw_address = nominatim_raw_json.get("address", {})

        postcode_str = str(raw_address.get("postcode", ""))
        postcode = self.geonames.validate_postcode(postcode_str)

        city = self._get_attribute(raw_address, ["city", "town", "village"])
        district, quarter = self._get_district_quarter(raw_address)

        return {
            "country": raw_address.get("country"),
            "country_code": (raw_address.get("country_code") or "").lower(),
            "state": raw_address.get("state"),
            "province": raw_address.get("province"),
            "city": city,
            "postcode": postcode,
            "district": district,
            "quarter": quarter,
            "street": raw_address.get("road"),
            "number": raw_address.get("house_number"),
        }

    def _parse_geonames_result(self, geonames_raw_json: Dict[str, Any]) -> Dict[str, Optional[str]]:
        geonames_country_code_str = geonames_raw_json.get("country_code")
        country_name = None
        if geonames_country_code_str:
            try:
                country_obj = pycountry.countries.get(alpha_2=geonames_country_code_str.upper())
                if country_obj:
                    country_name = spanish.gettext(country_obj.name)
            except LookupError:
                logger.warning(f"Country name not found for code: {geonames_country_code_str} using pycountry.")

        postcode_str = str(geonames_raw_json.get("postal_code", ""))
        postcode = self.geonames.validate_postcode(postcode_str)
        province = self.geonames.get_province_from_postcode(postcode) if postcode else None
        city = geonames_raw_json.get("place_name")

        return {
            "country": country_name,
            "country_code": (geonames_country_code_str or "").lower(),
            "state": geonames_raw_json.get("community"),
            "province": province,
            "city": city,
            "postcode": postcode,
            "district": None,
            "quarter": None,
            "street": None,
            "number": None,
        }

    def _get_empty_address_result(self) -> Dict[str, None]:
        return {
            "country": None,
            "country_code": None,
            "state": None,
            "province": None,
            "city": None,
            "postcode": None,
            "district": None,
            "quarter": None,
            "street": None,
            "number": None,
        }

    def _select_postcode_and_derived_province(
        self, parsed_nominatim_result: Dict[str, Optional[str]], parsed_geonames_result: Dict[str, Optional[str]], nominatim_address_province_raw: Optional[str]
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Determines the postcode and its derived province based on comparisons
        between Nominatim and GeoNames data, and Nominatim's raw address province.
        """
        nominatim_postcode = parsed_nominatim_result.get("postcode")
        geonames_postcode = parsed_geonames_result.get("postcode")

        province_from_nominatim_postcode = self.geonames.get_province_from_postcode(nominatim_postcode)
        province_from_geonames_postcode = self.geonames.get_province_from_postcode(geonames_postcode)

        norm_raw_nominatim_province = (
            normalize(nominatim_address_province_raw) if nominatim_address_province_raw else ""
        )
        norm_province_from_nominatim_postcode = (
            normalize(province_from_nominatim_postcode) if province_from_nominatim_postcode else ""
        )
        norm_province_from_geonames_postcode = (
            normalize(province_from_geonames_postcode) if province_from_geonames_postcode else ""
        )

        selected_postcode = None
        selected_province_from_postcode = None

        # If provinces derived from Nominatim and GeoNames postcodes differ
        nominatim_postcode_province_matches = False
        if norm_province_from_nominatim_postcode and norm_raw_nominatim_province:
            nominatim_postcode_province_matches = (
                jaro_winkler_similarity(norm_province_from_nominatim_postcode, norm_raw_nominatim_province)
                > JARO_WINKLER_THRESHOLD
            )

        geonames_postcode_province_matches = False
        if norm_province_from_geonames_postcode and norm_raw_nominatim_province:
            geonames_postcode_province_matches = (
                jaro_winkler_similarity(norm_province_from_geonames_postcode, norm_raw_nominatim_province)
                > JARO_WINKLER_THRESHOLD
            )

        # Prefer GeoNames postcode if its province matches Nominatim's raw address province,
        # and Nominatim's own postcode-derived province does not.
        if nominatim_postcode_province_matches:
            selected_postcode = nominatim_postcode
            selected_province_from_postcode = province_from_nominatim_postcode
        if geonames_postcode_province_matches and not nominatim_postcode_province_matches:
            selected_postcode = geonames_postcode
            selected_province_from_postcode = province_from_geonames_postcode

        return selected_postcode, selected_province_from_postcode

    def _select_final_result(
        self,
        parsed_nominatim_result: Dict[str, Optional[str]],
        parsed_geonames_result: Dict[str, Optional[str]],
        dist_nominatim: float,
        dist_geonames: float,
        authoritative_postcode: Optional[str],
        authoritative_province_from_postcode: Optional[str],
        nominatim_address_province_raw: Optional[str],
    ) -> Dict[str, Optional[str]]:
        """
        Selects the final address result based on distances and applies the authoritative postcode/province.
        """
        if dist_nominatim <= dist_geonames and dist_nominatim != float("inf"):
            final_result = parsed_nominatim_result
            final_result["postcode"] = authoritative_postcode
            final_result["province"] = nominatim_address_province_raw
        elif dist_geonames < dist_nominatim and dist_geonames != float("inf"):
            final_result = parsed_geonames_result
            final_result["postcode"] = authoritative_postcode
            final_result["province"] = authoritative_province_from_postcode
        else:
            final_result = self._get_empty_address_result()
        return final_result

    def _get_district_quarter(self, raw_json: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
        district = self._get_attribute(raw_json, ["city_district", "suburb", "borough"])
        quarter = self._get_attribute(raw_json, ["quarter", "neighbourhood"])

        if not district and quarter:
            district = quarter
            quarter = None

        return district, quarter

    def geocode(self, address: str) -> List[Dict[str, Any]]:
        return requests.get(f"{self.endpoint}/search?q={address}&format=json", timeout=30).json()

    def geocode_parsed(self, address: str) -> Optional[Dict[str, Optional[str]]]:
        results = self.geocode(address)

        if results:
            return self.reverse_parsed(results[0]["lat"], results[0]["lon"])

    def reverse(self, lat: Union[float, str], lon: Union[float, str]) -> Dict[str, Any]:
        return requests.get(f"{self.endpoint}/reverse?lat={lat}&lon={lon}&format=json", timeout=30).json()

    def reverse_parsed(self, lat: Union[float, str], lon: Union[float, str]) -> Dict[str, Optional[str]]:
        nominatim_response = self.reverse(lat, lon)
        geonames_response = self.geonames.reverse(lat, lon)

        # Initial parsing
        parsed_nominatim_result = self._parse_nominatim_result(nominatim_response)
        parsed_geonames_result = self._parse_geonames_result(geonames_response)

        # Determine authoritative postcode
        raw_nominatim_province = nominatim_response.get("address", {}).get("province")
        selected_postcode, selected_province_from_postcode = self._select_postcode_and_derived_province(
            parsed_nominatim_result, parsed_geonames_result, raw_nominatim_province
        )

        # Calculate distances
        nominatim_response_lat = nominatim_response.get("lat")
        nominatim_response_lon = nominatim_response.get("lon")
        geonames_response_lat = geonames_response.get("lat")
        geonames_response_lon = geonames_response.get("lon")

        input_coords = None
        try:
            input_coords = (float(lat), float(lon))
        except (ValueError, TypeError):
            logger.error(f"Invalid input coordinates for distance calculation: lat={lat}, lon={lon}")
            return self._get_empty_address_result()

        dist_nominatim = self._calculate_distance(nominatim_response_lat, nominatim_response_lon, input_coords)
        dist_geonames = self._calculate_distance(geonames_response_lat, geonames_response_lon, input_coords)

        # Select final result
        final_result = self._select_final_result(
            parsed_nominatim_result,
            parsed_geonames_result,
            dist_nominatim,
            dist_geonames,
            selected_postcode,
            selected_province_from_postcode,
            raw_nominatim_province,
        )

        return final_result


class NominatimInterface(Nominatim):
    def __init__(self, config: Dict[str, Any]) -> None:
        if "osm" in config:
            self.config = config["osm"]

            self.nominatim_endpoint = self.config["nominatim_endpoint"]
            self.geonames_endpoint = self.config["geonames_endpoint"]

            super().__init__(self.nominatim_endpoint, self.geonames_endpoint)
        else:
            logger.warning("no osm section in config")
