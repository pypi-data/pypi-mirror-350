# -*- coding: utf-8 -*-
"""
Author: Daniel Philippus
Date: 2025-02-05

BMI implementation of SCHEMA.
"""

from bmipy import Bmi
import numpy as np

logalot = False

class SchemaBmi(Bmi):
    """
    BMI implementation for SCHEMA.
    Example: https://github.com/csdms/bmi-example-python/blob/master/heat/bmi_heat.py
    """
    def __init__(self, name, inputs, input_map, input_units, output,
                 output_units):
        """
        Parameters
        ----------
        name : str
            Model name (e.g., "TempEst-NEXT")
        inputs : tuple of str
            Required input variables as CSDMS standard variable names
            (e.g., "land_surface_air__temperature")
        input_map : {dict of str:str}
            Map CSDMS inputs to the names used in the model.  Key = CSDMS name,
            value = model name.
        input_units : list of str
            Units of inputs in CSDMS standard notation (e.g., "Celsius").
        output : str
            Output variable as CSDMS standard variable name
            (e.g., "channel_water__temperature")
        output_units : str
            Units of outputs in CSDMS standard notation (e.g., "Celsius").
        """
        self._model = None
        self._values = {k: [] for k in inputs} | {output: []}
        self._var_units = {k: v for (k, v) in zip(inputs, input_units)} | {output: output_units}
        self._var_loc = {output: "node"}
        self._grids = output
        self._grid_type = "scalar"
        self.timestep = 0.0
        self._start_time = 0.0
        self._end_time = np.finfo("float").max
        self._time_units = "s"  # required, unfortunately
        self._name = name
        self._input_var_names = inputs
        self._output_var_name = output
        self._input_map = input_map
    
    def initialize(self, model_class, filename):
        """
        Initialize the model.  Filename points to input file.
        """
        self._model = model_class.from_file(filename)
        self._model.initialize_run(0)
    
    def update(self):
        # self._model.step()
        try:
            for k in self._values:
                self._model.set_val(self._input_map[k], self._values[k])
            self._timestep += 3600
            if self._timestep % 86400 < 1:
                self._values[self._output_var_name] = self._model.step()
            # for k in self._values:
            #     if k != self._output_var_name:
            #         self._values[k][0] = self._model.values[self._input_map[k]]
        except Exception as e:
            self._model.log(f"Error in update step: {e}")
    
    def update_until(self, time):
        while self._timestep < time:
            self.update()
    
    def finalize(self):
        self._model.get_history().to_csv("bmi_run_history.csv", index=False)
        self._model = None
    
    def get_component_name(self):
        return self._name
    
    def get_input_item_count(self):
        return len(self._input_var_names)
    
    def get_output_item_count(self):
        return len(self._output_var_names)
    
    def get_input_var_names(self):
        return self._input_var_names
    
    def get_output_var_names(self):
        return self._output_var_names
    
    def get_var_grid(self, name):
        return 0
    
    def get_var_type(self, name):
        return "float"
    
    def get_var_units(self, name):
        return self._var_units[name]
    
    def get_var_itemsize(self, name):
        return 8
    
    def get_var_nbytes(self, name):
        try:
            return self.get_value_ptr(name).nbytes
        except Exception as e:
            self._model.log(f"Error in get_value_ptr: {e}")
    
    def get_var_location(self, name):
        return "node"
    
    def get_current_time(self):
        return self._timestep
    
    def get_start_time(self):
        return 0.0
    
    def get_end_time(self):
        return self._end_time
    
    def get_time_units(self):
        return self._time_units
    
    def get_time_step(self):
        return 3600.0
    
    def get_value_ptr(self, name):
        return self._values[name]
    
    def get_value(self, name, dest):
        dest[:] = np.array(self.get_value_ptr(name))
        return dest
    
    def get_value_at_indices(self, name, dest, inds):
        return self.get_value(name, dest)
    
    def set_value(self, name, src):
        val = src[0]
        self._values[name].append(val)
        self._model.set_val(self._input_map[name], self._values[name][-24:],
                            bmiroll=True)
        
    def set_value_at_indices(self, name, inds, src):
        self.set_value(name, src)
        
    def get_grid_type(self, grid):
        return "scalar"
    
    def get_grid_rank(self, grid):
        return 1
    
    def get_grid_size(self, grid):
        return 1
    
    def get_grid_shape(self, grid, shape):
        shape[:] = np.array([1])
        return np.array([1])
    
    def get_grid_spacing(self, grid, spacing):
        raise NotImplementedError("get_grid_spacing")
    
    def get_grid_origin(self, grid, origin):
        raise NotImplementedError("get_grid_origin")
        
    def get_grid_x(self, grid, x):
        raise NotImplementedError("get_grid_x")
    
    def get_grid_y(self, grid, y):
        raise NotImplementedError("get_grid_y")
    
    def get_grid_z(self, grid, z):
        raise NotImplementedError("get_grid_z")
    
    def get_grid_node_count(self, grid):
        return 1
    
    def get_grid_edge_count(self, grid):
        return 0
    
    def get_grid_face_count(self, grid):
        return 0
    
    def get_grid_edge_nodes(self, grid, edge_nodes):
        raise NotImplementedError("get_grid_edge_nodes")
        
    def get_grid_face_edges(self, grid, face_edges):
        raise NotImplementedError("get_grid_face_edges")
        
    def get_grid_face_nodes(self, grid, face_nodes):
        raise NotImplementedError("get_grid_face_nodes")
        
    def get_grid_nodes_per_face(self, grid, nodes_per_face):
        raise NotImplementedError("get_grid_nodes_per_face")
        
