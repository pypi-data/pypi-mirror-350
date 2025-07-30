from datetime import datetime as Datetime
from enum import Enum
from typing import (TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar,
                    Union, cast)

from pydantic import BaseModel, Extra, Field
from pydantic.fields import FieldInfo


class ProcessingLevel(Enum):
    RAW="RAW"
    L1="L1"
    L2="L2"
    L3="L3"
    L4="L4"


class ObservationType(Enum):
    image="IMAGE"
    radar="RADAR"
    dem="DEM"


class ResourceType(Enum):
    cube="CUBE"
    gridded="GRIDDED"
    vector="VECTOR"
    other="OTHER"


class ItemFormat(Enum):
    shape="SHAPE"
    dimap="DIMAP"
    geotiff="GEOTIFF"
    safe="SAFE"
    theia="THEIA"
    ast_dem="AST_DEM"
    digitalglobe="DIGITALGLOBE"
    geoeye="GEOEYE"
    rapideye="RAPIDEYE"
    spot5="SPOT5"
    spot6_7="SPOT6_7"
    other="OTHER"
    terrasar="TerraSAR-X"
    csk="COSMO-SkyMed"


class AssetFormat(Enum):
    shape="SHAPE"
    geotiff="GEOTIFF"
    jpg="JPG"
    jpg2000="JPG2000"
    png="PNG"
    csv="CSV"
    json="JSON"
    zip="ZIP"
    tar="TAR"
    targz="TARGZ"
    other="OTHER"


class Role(Enum):
    airs_item="airs_item"
    thumbnail="thumbnail"
    overview="overview"
    data="data"
    metadata="metadata"
    cog="cog"
    zarr="zarr"
    datacube="datacube"
    visual="visual"
    date="date"
    graphic="graphic"
    data_mask="data-mask"
    snow_ice="snow-ice"
    land_water="land-water"
    water_mask="water-mask"
    iso_19115="iso-19115"
    reflectance="reflectance"
    temperature="temperature"
    saturation="saturation"
    cloud="cloud"
    cloud_shadow="cloud-shadow"
    incidence_angle="incidence-angle"
    azimuth="azimuth"
    sun_azimuth="sun-azimuth"
    sun_elevation="sun-elevation"
    terrain_shadow="terrain-shadow"
    terrain_occlusion="terrain-occlusion"
    terrain_illumination="terrain-illumination"
    local_incidence_angle="local-incidence-angle"
    noise_power="noise-power"
    amplitude="amplitude"
    magnitude="magnitude"
    sigma0="sigma0"
    beta0="beta0"
    gamma0="gamma0"
    date_offset="date-offset"
    covmat="covmat"
    prd="prd"


class CommonBandName(Enum):
    coastal="coastal"
    blue="blue"
    green="green"
    red="red"
    yellow="yellow"
    pan="pan"
    rededge="rededge"
    nir="nir"
    nir08="nir08"
    nir09="nir09"
    cirrus="cirrus"
    swir16="swir16"
    swir22="swir22"
    lwir="lwir"
    lwir11="lwir11"
    lwir12="lwir12"
    

class VariableType(Enum):
    data="data"
    auxiliary="auxiliary"


class DimensionType(Enum):
    spatial="spatial"
    temporal="temporal"
    geometry="geometry"
    

class RasterType(BaseModel):
    source:str
    format:str


class Raster(BaseModel):
    type:RasterType
    path:str
    id:str


class Axis(Enum):
    x="x"
    y="y"
    z="z"
    t="t"


class Indicators(BaseModel):
    time_compacity: float | None = Field(default=None, title="Indicates whether the temporal extend of the temporal slices (groups) are compact or not compared to the cube temporal extend. Computed as follow: 1-range(group rasters) / range(cube rasters).")
    spatial_coverage: float | None = Field(default=None, title="Indicates the proportion of the region of interest that is covered by the input rasters. Computed as follow: area(intersection(union(rasters),roi)) / area(roi))")
    group_lightness: float | None = Field(default=None, title="Indicates the proportion of non overlapping regions between the different input rasters. Computed as follow: area(intersection(union(rasters),roi)) / sum(area(intersection(raster, roi)))")
    time_regularity: float | None = Field(default=None, title="Indicates the regularity of the extends between the temporal slices (groups). Computed as follow: 1-std(inter group temporal gaps)/avg(inter group temporal gaps)")


class Group(BaseModel):
    timestamp: int | None = Field(default=None, title="The timestamp of this temporal group.")
    rasters: List[Raster] | None = Field(default=None, title="The rasters belonging to this temporal group.")
    quality_indicators: Indicators | None = Field(default=None, title="Set of indicators for estimating the quality of the datacube group. The indicators are group based.")


class Band(BaseModel, extra=Extra.allow):
    name: str = Field(title="The name of the band (e.g., B01, B8, band2, red).", max_length=300)
    common_name: str | None = Field(default=None, title="The name commonly used to refer to the band to make it easier to search for bands across instruments. See the list of accepted common names.")
    description: str | None = Field(default=None, title="Description to fully explain the band. CommonMark 0.29 syntax MAY be used for rich text representation.", max_length=300)
    center_wavelength: float | None = Field(default=None, title="The center wavelength of the band, in micrometers (μm).")
    full_width_half_max: float | None = Field(default=None, title="Full width at half maximum (FWHM). The width of the band, as measured at half the maximum transmission, in micrometers (μm).")
    solar_illumination: float | None = Field(default=None, title="The solar illumination of the band, as measured at half the maximum transmission, in W/m2/micrometers.")
    quality_indicators: Indicators | None = Field(default=None, title="Set of indicators for estimating the quality of the datacube variable (band).")


class Asset(BaseModel, extra=Extra.allow):
    name: str | None = Field(default=None, title="Asset's name. But be the same as the key in the `assets` dictionary.", max_length=300)
    size: int | None = Field(default=None, title="Asset's size in Bytes.")
    href: str | None = Field(default=None, title="Absolute link to the asset object.")
    asset_type: str | None = Field(default=None, title="Type of data (ResourceType)")
    asset_format: str | None = Field(default=None, title="Data format (AssetFormat)")
    storage__requester_pays: bool | None = Field(default=None, title="Is the data requester pays or is it data manager/cloud provider pays. Defaults to false. Whether the requester pays for accessing assets")
    storage__tier: str | None = Field(default=None, title="Cloud Provider Storage Tiers (Standard, Glacier, etc.)")
    storage__platform: str | None = Field(default=None, title="PaaS solutions (ALIBABA, AWS, AZURE, GCP, IBM, ORACLE, OTHER)")
    storage__region: str | None = Field(default=None, title="The region where the data is stored. Relevant to speed of access and inter region egress costs (as defined by PaaS provider)")
    airs__managed: bool | None = Field(default=True, title="Whether the asset is managed by AIRS or not.")
    airs__object_store_bucket: str | None = Field(default=None, title="Object store bucket for the asset object.")
    airs__object_store_key: str | None = Field(default=None, title="Object store key of the asset object.")
    title: str | None = Field(default=None, title="Optional displayed title for clients and users.", max_length=300)
    description: str | None = Field(default=None, title="A description of the Asset providing additional details, such as how it was processed or created. CommonMark 0.29 syntax MAY be used for rich text representation.", max_length=300)
    type: str | None = Field(default=None, title="Optional description of the media type. Registered Media Types are preferred. See MediaType for common media types.", max_length=300)
    roles: List[str] | None = Field(default=None, title="Optional, Semantic roles (i.e. thumbnail, overview, data, metadata) of the asset.", max_length=300)
    extra_fields: Dict[str, Any] | None = Field(default=None, title="Optional, additional fields for this asset. This is used by extensions as a way to serialize and deserialize properties on asset object JSON.")
    gsd: float | None = Field(default=None, title="Ground Sampling Distance (resolution) of the asset")
    eo__bands: List[Band] | None = Field(default=None, title="An array of available bands where each object is a Band Object. If given, requires at least one band.", )
    sar__instrument_mode: str | None = Field(default=None, title="The name of the sensor acquisition mode that is commonly used. This should be the short name, if available. For example, WV for \"Wave mode\" of Sentinel-1 and Envisat ASAR satellites.")
    sar__frequency_band: str | None = Field(default=None, title="The common name for the frequency band to make it easier to search for bands across instruments. See section \"Common Frequency Band Names\" for a list of accepted names.")
    sar__center_frequency: float | None = Field(default=None, title="The center frequency of the instrument, in gigahertz (GHz).")
    sar__polarizations: str | None = Field(default=None, title="Any combination of polarizations.")
    sar__product_type: str | None = Field(default=None, title="The product type, for example SSC, MGD, or SGC")
    sar__resolution_range: float | None = Field(default=None, title="The range resolution, which is the maximum ability to distinguish two adjacent targets perpendicular to the flight path, in meters (m).")
    sar__resolution_azimuth: float | None = Field(default=None, title="The azimuth resolution, which is the maximum ability to distinguish two adjacent targets parallel to the flight path, in meters (m).")
    sar__pixel_spacing_range: float | None = Field(default=None, title="The range pixel spacing, which is the distance between adjacent pixels perpendicular to the flight path, in meters (m). Strongly RECOMMENDED to be specified for products of type GRD.")
    sar__pixel_spacing_azimuth: float | None = Field(default=None, title="The azimuth pixel spacing, which is the distance between adjacent pixels parallel to the flight path, in meters (m). Strongly RECOMMENDED to be specified for products of type GRD.")
    sar__looks_range: float | None = Field(default=None, title="Number of range looks, which is the number of groups of signal samples (looks) perpendicular to the flight path.")
    sar__looks_azimuth: float | None = Field(default=None, title="Number of azimuth looks, which is the number of groups of signal samples (looks) parallel to the flight path.")
    sar__looks_equivalent_number: float | None = Field(default=None, title="The equivalent number of looks (ENL).")
    sar__observation_direction    : str | None = Field(default=None, title="Antenna pointing direction relative to the flight trajectory of the satellite, either left or right.")
    proj__epsg: int | None = Field(default=None, title="EPSG code of the datasource.")
    proj__wkt2: str | None = Field(default=None, title="PROJJSON object representing the Coordinate Reference System (CRS) that the proj:geometry and proj:bbox fields represent.")
    proj__geometry: Any | None = Field(default=None, title="Defines the footprint of this Item.")
    proj__bbox: List[float] | None = Field(default=None, title="Bounding box of the Item in the asset CRS in 2 or 3 dimensions.")
    proj__centroid: Any | None = Field(default=None, title="Coordinates representing the centroid of the Item (in lat/long).")
    proj__shape: List[float] | None = Field(default=None, title="Number of pixels in Y and X directions for the default grid.")
    proj__transform: List[float] | None = Field(default=None, title="The affine transformation coefficients for the default grid.")


class Properties(BaseModel, extra=Extra.allow):
    datetime: Datetime | None = Field(default=None, title="datetime associated with this item. If None, a start_datetime and end_datetime must be supplied.")
    start_datetime: Datetime | None = Field(default=None, title="Optional start datetime, part of common metadata. This value will override any start_datetime key in properties.")
    end_datetime: Datetime | None = Field(default=None, title="Optional end datetime, part of common metadata. This value will override any end_datetime key in properties.")
    programme: str | None = Field(default=None, title="Name of the programme")
    constellation: str | None = Field(default=None, title="Name of the constellation")
    satellite: str | None = Field(default=None, title="Name of the satellite")
    instrument: str | None = Field(default=None, title="Name of the instrument")
    sensor: str | None = Field(default=None, title="Name of the sensor")
    sensor_type: str | None = Field(default=None, title="Type of sensor")
    annotations: str | None = Field(default=None, title="Human annotations for the item")
    gsd: float | None = Field(default=None, title="Ground Sampling Distance (resolution)")
    secondary_id: str | None = Field(default=None, title="Secondary identifier")
    data_type: str | None = Field(default=None, title="Type of data")
    item_type: str | None = Field(default=None, title="Type of data (ResourceType)")
    item_format: str | None = Field(default=None, title="Data format (ItemFormat)")
    main_asset_format: str | None = Field(default=None, title="Data format of the main asset (AssetFormat)")
    main_asset_name: str | None = Field(default=None, title="Name of the main asset (AssetFormat)")
    observation_type: str | None = Field(default=None, title="Type of observation (ObservationType)")
    data_coverage: float | None = Field(default=None, title="Estimate of data cover")
    water_coverage: float | None = Field(default=None, title="Estimate of water cover")
    locations: List[str] | None = Field(default=None, title="List of locations covered by the item")
    create_datetime: int | None = Field(default=None, title="Date of item creation in the catalog, managed by the ARLAS Item Registration Service")
    update_datetime: int | None = Field(default=None, title="Update date of the item in the catalog, managed by the ARLAS Item Registration Service")
    view__off_nadir: float | None = Field(default=None, title="The angle from the sensor between nadir (straight down) and the scene center. Measured in degrees (0-90).")
    view__incidence_angle: float | None = Field(default=None, title="The incidence angle is the angle between the vertical (normal) to the intercepting surface and the line of sight back to the satellite at the scene center. Measured in degrees (0-90).")
    view__azimuth: float | None = Field(default=None, title="Viewing azimuth angle. The angle measured from the sub-satellite point (point on the ground below the platform) between the scene center and true north. Measured clockwise from north in degrees (0-360).")
    view__sun_azimuth: float | None = Field(default=None, title="Sun azimuth angle. From the scene center point on the ground, this is the angle between truth north and the sun. Measured clockwise in degrees (0-360).")
    view__sun_elevation: float | None = Field(default=None, title="Sun elevation angle. The angle from the tangent of the scene center point to the sun. Measured from the horizon in degrees (-90-90). Negative values indicate the sun is below the horizon, e.g. sun elevation of -10° means the data was captured during nautical twilight.")
    storage__requester_pays: bool | None = Field(default=None, title="Is the data requester pays or is it data manager/cloud provider pays. Defaults to false. Whether the requester pays for accessing assets")
    storage__tier: str | None = Field(default=None, title="Cloud Provider Storage Tiers (Standard, Glacier, etc.)")
    storage__platform: str | None = Field(default=None, title="PaaS solutions (ALIBABA, AWS, AZURE, GCP, IBM, ORACLE, OTHER)")
    storage__region: str | None = Field(default=None, title="The region where the data is stored. Relevant to speed of access and inter region egress costs (as defined by PaaS provider)")
    eo__cloud_cover: float | None = Field(default=None, title="Estimate of cloud cover.")
    eo__snow_cover: float | None = Field(default=None, title="Estimate of snow and ice cover.")
    eo__bands: List[Band] | None = Field(default=None, title="An array of available bands where each object is a Band Object. If given, requires at least one band.")
    processing__expression: str | None = Field(default=None, title="An expression or processing chain that describes how the data has been processed. Alternatively, you can also link to a processing chain with the relation type processing-expression (see below).")
    processing__lineage: str | None = Field(default=None, title="Lineage Information provided as free text information about the how observations were processed or models that were used to create the resource being described NASA ISO.")
    processing__level: str | None = Field(default=None, title="The name commonly used to refer to the processing level to make it easier to search for product level across collections or items. The short name must be used (only L, not Level).")
    processing__facility: str | None = Field(default=None, title="The name of the facility that produced the data. For example, Copernicus S1 Core Ground Segment - DPA for product of Sentinel-1 satellites.")
    processing__software: Dict[str, str] | None = Field(default=None, title="A dictionary with name/version for key/value describing one or more softwares that produced the data.")
    dc3__quality_indicators: Indicators | None = Field(default=None, title="Set of indicators for estimating the quality of the datacube based on the composition. The indicators are group based. A cube indicator is the product of its corresponding group indicator.")
    dc3__composition: List[Group] | None = Field(default=None, title="List of raster groups used for elaborating the cube temporal slices.")
    dc3__number_of_chunks: int | None = Field(default=None, title="Number of chunks (if zarr or similar partitioned format) within the cube.")
    dc3__chunk_weight: int | None = Field(default=None, title="Weight of a chunk (number of bytes).")
    dc3__fill_ratio: float | None = Field(default=None, title="1: the cube is full, 0 the cube is empty, in between the cube is partially filled.")
    cube__dimensions: Dict[str, DimensionType] | None = Field(default=None, title="Uniquely named dimensions of the datacube.")
    cube__variables: Dict[str, VariableType] | None = Field(default=None, title="Uniquely named variables of the datacube.")
    acq__acquisition_mode: str | None = Field(default=None, title="The name of the acquisition mode.")
    acq__acquisition_orbit_direction: str | None = Field(default=None, title="Acquisition orbit direction (ASCENDING or DESCENDING).")
    acq__acquisition_type: str | None = Field(default=None, title="Acquisition type (STRIP)")
    acq__across_track: float | None = Field(default=None, title="Across track angle")
    acq__along_track: float | None = Field(default=None, title="Along track angle")
    acq__archiving_date: Datetime | None = Field(default=None, title="Archiving date")
    acq__download_orbit: float | None = Field(default=None, title="Download orbit")
    acq__request_id: str | None = Field(default=None, title="Original request identifier")
    acq__quality_average: float | None = Field(default=None, title="Quality average")
    acq__quality_computation: str | None = Field(default=None, title="Quality computation")
    acq__receiving_station: str | None = Field(default=None, title="Receiving station")
    acq__reception_date: Datetime | None = Field(default=None, title="Reception date")
    acq__spectral_mode: str | None = Field(default=None, title="Spectral mode")
    sar__instrument_mode: str | None = Field(default=None, title="The name of the sensor acquisition mode that is commonly used. This should be the short name, if available. For example, WV for \"Wave mode\" of Sentinel-1 and Envisat ASAR satellites.")
    sar__frequency_band: str | None = Field(default=None, title="The common name for the frequency band to make it easier to search for bands across instruments. See section \"Common Frequency Band Names\" for a list of accepted names.")
    sar__center_frequency: float | None = Field(default=None, title="The center frequency of the instrument, in gigahertz (GHz).")
    sar__polarizations: str | None = Field(default=None, title="Any combination of polarizations.")
    sar__product_type: str | None = Field(default=None, title="The product type, for example SSC, MGD, or SGC")
    sar__resolution_range: float | None = Field(default=None, title="The range resolution, which is the maximum ability to distinguish two adjacent targets perpendicular to the flight path, in meters (m).")
    sar__resolution_azimuth: float | None = Field(default=None, title="The azimuth resolution, which is the maximum ability to distinguish two adjacent targets parallel to the flight path, in meters (m).")
    sar__pixel_spacing_range: float | None = Field(default=None, title="The range pixel spacing, which is the distance between adjacent pixels perpendicular to the flight path, in meters (m). Strongly RECOMMENDED to be specified for products of type GRD.")
    sar__pixel_spacing_azimuth: float | None = Field(default=None, title="The azimuth pixel spacing, which is the distance between adjacent pixels parallel to the flight path, in meters (m). Strongly RECOMMENDED to be specified for products of type GRD.")
    sar__looks_range: float | None = Field(default=None, title="Number of range looks, which is the number of groups of signal samples (looks) perpendicular to the flight path.")
    sar__looks_azimuth: float | None = Field(default=None, title="Number of azimuth looks, which is the number of groups of signal samples (looks) parallel to the flight path.")
    sar__looks_equivalent_number: float | None = Field(default=None, title="The equivalent number of looks (ENL).")
    sar__observation_direction: str | None = Field(default=None, title="Antenna pointing direction relative to the flight trajectory of the satellite, either left or right.")
    proj__epsg: int | None = Field(default=None, title="EPSG code of the datasource.")
    proj__wkt2: str | None = Field(default=None, title="PROJJSON object representing the Coordinate Reference System (CRS) that the proj:geometry and proj:bbox fields represent.")
    proj__geometry: Any | None = Field(default=None, title="Defines the footprint of this Item.")
    proj__bbox: List[float] | None = Field(default=None, title="Bounding box of the Item in the asset CRS in 2 or 3 dimensions.")
    proj__centroid: Any | None = Field(default=None, title="Coordinates representing the centroid of the Item (in lat/long).")
    proj__shape: List[float] | None = Field(default=None, title="Number of pixels in Y and X directions for the default grid.")
    proj__transform: List[float]      | None = Field(default=None, title="The affine transformation coefficients for the default grid.")
    generated__has_overview: bool | None = Field(default=False, title="Whether the item has an overview or not.")
    generated__has_thumbnail: bool | None = Field(default=False, title="Whether the item has a thumbnail or not.")
    generated__has_metadata: bool | None = Field(default=False, title="Whether the item has a metadata file or not.")
    generated__has_data: bool | None = Field(default=False, title="Whether the item has a data file or not.")
    generated__has_cog: bool | None = Field(default=False, title="Whether the item has a cog or not.")
    generated__has_zarr: bool | None = Field(default=False, title="Whether the item has a zarr or not.")
    generated__date_keywords: List[str] | None = Field(default=None, title="A list of keywords indicating clues on the date")
    generated__day_of_week: int | None = Field(default=None, title="Day of week.")
    generated__day_of_year: int | None = Field(default=None, title="Day of year.")
    generated__hour_of_day: int | None = Field(default=None, title="Hour of day.")
    generated__minute_of_day: int | None = Field(default=None, title="Minute of day.")
    generated__month: int | None = Field(default=None, title="Month")
    generated__year: int | None = Field(default=None, title="Year")
    generated__season: str | None = Field(default=None, title="Season")
    generated__tltrbrbl: List[List[float]] | None = Field(default=None, title="The coordinates of the top left, top right, bottom right, bottom left corners of the item.")
    generated__band_common_names: List[str] | None = Field(default=None, title="List of the band common names.")
    generated__band_names: List[str] | None = Field(default=None, title="List of the band names.")
    generated__geohash2: str | None = Field(default=None, title="Geohash on the first two characters.")
    generated__geohash3: str | None = Field(default=None, title="Geohash on the first three characters.")
    generated__geohash4: str | None = Field(default=None, title="Geohash on the first four characters.")
    generated__geohash5: str | None = Field(default=None, title="Geohash on the first five characters.")


class Item(BaseModel, extra=Extra.allow):
    collection: str | None = Field(default=None, title="Name of the collection the item belongs to.", max_length=300)
    catalog: str | None = Field(default=None, title="Name of the catalog the item belongs to.", max_length=300)
    id: str | None = Field(default=None, title="Unique item identifier. Must be unique within the collection.", max_length=300)
    geometry: Dict[str, Any] | None = Field(default=None, title="Defines the full footprint of the asset represented by this item, formatted according to `RFC 7946, section 3.1 (GeoJSON) <https://tools.ietf.org/html/rfc7946>`_")
    bbox: List[float] | None = Field(default=None, title="Bounding Box of the asset represented by this item using either 2D or 3D geometries. The length of the array must be 2*n where n is the number of dimensions. Could also be None in the case of a null geometry.")
    centroid: List[float] | None = Field(default=None, title="Coordinates (lon/lat) of the geometry's centroid.")
    assets: Dict[str, Asset] | None = Field(default=None, title="A dictionary mapping string keys to Asset objects. All Asset values in the dictionary will have their owner attribute set to the created Item.")
    properties: Properties | None = Field(default=None, title="Item properties")
