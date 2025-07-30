from .interpolation import Interpolation
from .average_uniform import AverageUniform
from .grid_interpolation import GridInterpolation
from .inverse_distance import InverseDistance
from .linear_triangle import LinearTriangle
from .thiessen_polygon import ThiessenPolygon
from whitebox_workflows import Raster
import logging
logger = logging.getLogger(__name__)

def WriteWeightFile(method:str, radius:int, parameter_h5_file:str, weight_name:str,mask_raster:Raster, station_coordinates:list):
    #get interpolation object based on method
    interploation = Interpolation(parameter_h5_file, weight_name)
    if method == "average_uniform":
        interploation = AverageUniform(parameter_h5_file, weight_name)
    elif method == "grid_interpolation":
        interploation = GridInterpolation(parameter_h5_file, weight_name)
    elif method == "inverse_distance":
        interploation = InverseDistance(parameter_h5_file, weight_name, radius)
    elif method == "linear_triangle":
        interploation = LinearTriangle(parameter_h5_file, weight_name)
    elif method == "thiessen_polygon":
        interploation = LinearTriangle(parameter_h5_file, weight_name)
    else:
        logger.info(f"Interpolation method {method} is not valide. Use inverst distance method instead.")
        interploation = InverseDistance(parameter_h5_file, weight_name)

    #generate the file
    interploation.write_weight(mask_raster, station_coordinates)
    
