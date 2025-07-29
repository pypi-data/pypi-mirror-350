import json
from typing import Any

__all__ = ["GeometryConverter"]

try:
    import geoalchemy2
    import shapely

    class GeometryConverter:
        def two_way_converter_generator(self, type=""):
            """
            Generate a two-way converter for a specific geometry type.

            Args:
                type (str, optional): The geometry type. Defaults to ''.

            Returns:
                Callable[[geoalchemy2.WKBElement | shapely.geometry.base.BaseGeometry | dict[str, Any] | str], Any]: The two-way converter.
            """

            def two_way_converter(
                value: (
                    geoalchemy2.WKBElement
                    | shapely.geometry.base.BaseGeometry
                    | dict[str, Any]
                    | str
                ),
            ):
                return self.two_way_converter(value, type)

            return two_way_converter

        def two_way_converter(
            self,
            value: (
                geoalchemy2.WKBElement
                | shapely.geometry.base.BaseGeometry
                | dict[str, Any]
                | str
            ),
            type: str = "",
        ):
            """
            Convert between WKB, WKT, GeoJSON, and shapely geometries.

            - WKBElement -> GeoJSON
            - BaseGeometry -> GeoJSON
            - GeoJSON -> WKT
            - WKT -> WKT (Check validity)

            Args:
                value (geoalchemy2.WKBElement | shapely.geometry.base.BaseGeometry | dict[str, Any] | str): Value to convert.
                type (str, optional): The geometry type to check for. Empty means no check. Defaults to "".

            Raises:
                ValueError: If the value is not a valid geometry.

            Returns:
                dict[str, Any] | str: Converted value.
            """
            if isinstance(value, geoalchemy2.WKBElement) or isinstance(
                value, shapely.geometry.base.BaseGeometry
            ):
                return self.to_geojson(value)

            if isinstance(value, dict):
                try:
                    return self.from_geojson(json.dumps(value)).wkt
                except shapely.errors.GEOSException as e:
                    raise ValueError(str(e))

            try:
                value_type = shapely.from_wkt(value).geom_type.capitalize()
                type = type.capitalize()
                if type and value_type != type:
                    raise ValueError(f"Expected {type} but got {value_type}")
            except shapely.errors.GEOSException as e:
                raise ValueError(str(e))
            return value

        def to_geojson(
            self, value: shapely.geometry.base.BaseGeometry | geoalchemy2.WKBElement
        ):
            """
            Convert a shapely geometry or WKBElement to GeoJSON.

            Args:
                value (shapely.geometry.base.BaseGeometry | geoalchemy2.WKBElement): Geometry to convert.

            Returns:
                dict[str, Any]: Converted GeoJSON.
            """
            if isinstance(value, geoalchemy2.WKBElement):
                value = self.from_wkb(value)
            data: dict[str, Any] = json.loads(shapely.to_geojson(value))
            return data

        def from_wkb(self, value: geoalchemy2.WKBElement):
            """
            Convert a WKBElement to a shapely geometry.

            Args:
                value (geoalchemy2.WKBElement): WKBElement to convert.

            Returns:
                shapely.geometry.base.BaseGeometry: Converted geometry.
            """
            return geoalchemy2.shape.to_shape(value)

        def from_geojson(self, value: dict[str, Any] | str):
            """
            Convert a GeoJSON string or dict to a shapely geometry.

            Args:
                value (dict[str, Any] | str): GeoJSON to convert.

            Raises:
                ValueError: If the GeoJSON is not valid.

            Returns:
                shapely.geometry.base.BaseGeometry: Converted geometry.
            """
            if isinstance(value, dict):
                value = json.dumps(value)
            return shapely.from_geojson(value, on_invalid="raise")

except ImportError:

    class GeometryConverter:
        def __call__(self, *args: Any, **kwds: Any) -> Any:
            raise ImportError(
                "geoalchemy2 and shapely must be installed to use this feature"
            )
