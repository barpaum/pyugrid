#!/usr/bin/env python

"""
Tests for writing and reading back in via netcdf-format

i.e. making sure round trip works.

This is, of course, totally incomplete, but a it is start.

"""

from __future__ import (absolute_import, division, print_function)

from .utilities import chdir

import numpy as np

from pyugrid.ugrid import UGrid, UVar
from pyugrid.test_examples import two_triangles


def test_with_faces():
    """
    Test with faces, edges, but no `face_coordintates` or `edge_coordinates`.

    """

    with chdir('files'):
        grid = two_triangles()
        grid.save_as_netcdf('2_triangles.nc')
        # Read it back in and check it out.
        grid2 = UGrid.from_ncfile('2_triangles.nc')

    assert np.array_equal(grid.nodes, grid2.nodes)
    assert np.array_equal(grid.faces, grid2.faces)
    print(grid2.edges)
    assert np.array_equal(grid.edges, grid2.edges)


def test_without_faces():
    grid = two_triangles()
    del grid.faces
    assert grid.faces is None

    with chdir('files'):
        grid.save_as_netcdf('2_triangles.nc')
        # Read it back in and check it out.
        grid2 = UGrid.from_ncfile('2_triangles.nc')

    assert grid2.faces is None
    assert np.array_equal(grid.faces, grid2.faces)
    assert np.array_equal(grid.edges, grid2.edges)


def test_with_just_nodes_and_depths():
    filename = '2_triangles_depth.nc'
    grid = two_triangles()
    del grid.faces
    del grid.edges

    depth_array = [1.0, 2.0, 3.0, 4.0]
    depth = UVar('depth',
                 'node',
                 np.array([1.0, 2.0, 3.0, 4.0]),
                 {'units': 'm',
                  'positive': 'down',
                  'standard_name': 'sea_floor_depth_below_geoid'})
    grid.add_data(depth)

    with chdir('files'):
        grid.save_as_netcdf(filename)
        # Read it back in and check it out.
        grid2 = UGrid.from_ncfile(filename, load_data=True)

    assert grid2.faces is None
    assert grid2.edges is None
    assert np.array_equal(grid2.nodes, grid.nodes)

    assert np.array_equal(grid2.data['depth'].data, depth_array)
    assert grid2.data['depth'].attributes == depth.attributes


if __name__ == "__main__":
    test_with_faces()
    test_without_faces()
