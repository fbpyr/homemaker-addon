#!/usr/bin/python3

import unittest, sys, os

from topologic import Vertex, Face, CellComplex, Graph

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from topologist.helpers import wipe_global_cluster
from fitness import p159_light_on_two_sides_of_every_room


class Tests(unittest.TestCase):
    def setUp(self):

        widgets_text = [
            ["Circulation", [9.42, -1.11, 0.33]],
            ["Circulation", [9.46, -0.82, 3.89]],
            ["Circulation", [9.46, -0.82, 7.15]],
            ["Kitchen", [-3.08, 0.41, 0.73]],
            ["Kitchen", [-3.08, 0.41, 4.63]],
            ["Kitchen", [-3.08, 0.41, 7.88]],
            ["Living", [1.27, 2.35, 0.31]],
            ["Living", [1.27, 2.35, 4.21]],
            ["Living", [10.32, 4.95, 4.21]],
            ["Living", [1.27, 2.35, 7.46]],
            ["Living", [10.32, 4.95, 7.46]],
            ["Outside", [-1.55, -3.24, 0.45]],
            ["Retail", [9.71, 3.62, 0.40]],
            ["Stair", [5.16, -0.74, 0.24]],
            ["Stair", [5.16, -0.74, 4.13]],
            ["Stair", [5.16, -0.74, 7.39]],
            ["Toilet", [5.21, 3.70, 0.20]],
            ["Toilet", [5.21, 3.70, 4.35]],
        ]

        faces_text = [
            [
                [
                    [0.9822620153427124, -5.026822090148926, 0.0],
                    [-3.259223461151123, -6.221540927886963, 0.0],
                    [-4.066977024078369, -3.35385799407959, 0.0],
                    [0.17450830340385437, -2.1591389179229736, 0.0],
                ],
                "default",
            ],
            [
                [
                    [0.9822620153427124, -5.026822090148926, 0.0],
                    [0.9822620153427124, -5.026822090148926, 3.2],
                    [-3.259223461151123, -6.221540927886963, 3.2],
                    [-3.259223461151123, -6.221540927886963, 0.0],
                ],
                "blank",
            ],
            [
                [
                    [0.9822620153427124, -5.026822090148926, 0.0],
                    [0.17450830340385437, -2.1591389179229736, 0.0],
                    [0.17450830340385437, -2.1591389179229736, 3.2],
                    [0.9822620153427124, -5.026822090148926, 3.2],
                ],
                "default",
            ],
            [
                [
                    [-4.066977024078369, -3.35385799407959, 0.0],
                    [-4.066977024078369, -3.35385799407959, 3.2],
                    [0.17450830340385437, -2.1591389179229736, 3.2],
                    [0.17450830340385437, -2.1591389179229736, 0.0],
                ],
                "default",
            ],
            [
                [
                    [-4.066977024078369, -3.35385799407959, 0.0],
                    [-3.259223461151123, -6.221540927886963, 0.0],
                    [-3.259223461151123, -6.221540927886963, 3.2],
                    [-4.066977024078369, -3.35385799407959, 3.2],
                ],
                "default",
            ],
            [
                [
                    [-4.066977024078369, -3.35385799407959, 3.2],
                    [-3.259223461151123, -6.221540927886963, 3.2],
                    [0.9822620153427124, -5.026822090148926, 3.2],
                    [0.17450830340385437, -2.1591389179229736, 3.2],
                ],
                "default",
            ],
            [
                [
                    [-5.92466402053833, 3.2412912845611572, 3.2],
                    [-1.6831783056259155, 4.436010360717773, 3.2],
                    [-0.16507524251937866, -0.9535511136054993, 3.2],
                    [0.17450830340385437, -2.1591389179229736, 3.2],
                    [-4.066977024078369, -3.35385799407959, 3.2],
                ],
                "default",
            ],
            [
                [
                    [4.860907554626465, -3.9343056678771973, 0.0],
                    [3.7135703563690186, 0.1389651894569397, 0.0],
                    [3.7135703563690186, 0.1389651894569397, 3.2],
                    [4.860907554626465, -3.9343056678771973, 3.2],
                ],
                "default",
            ],
            [
                [
                    [-0.16507524251937866, -0.9535511136054993, 3.2],
                    [3.7135703563690186, 0.1389651894569397, 3.2],
                    [3.7135703563690186, 0.1389651894569397, 0.0],
                    [-0.16507524251937866, -0.9535511136054993, 0.0],
                ],
                "default",
            ],
            [
                [
                    [0.17450830340385437, -2.1591389179229736, 0.0],
                    [0.17450830340385437, -2.1591389179229736, 3.2],
                    [-0.16507524251937866, -0.9535511136054993, 3.2],
                    [-0.16507524251937866, -0.9535511136054993, 0.0],
                ],
                "default",
            ],
            [
                [
                    [-4.066977024078369, -3.35385799407959, 0.0],
                    [-5.92466402053833, 3.2412912845611572, 0.0],
                    [-1.6831783056259155, 4.436010360717773, 0.0],
                    [-0.16507524251937866, -0.9535511136054993, 0.0],
                    [0.17450830340385437, -2.1591389179229736, 0.0],
                ],
                "default",
            ],
            [
                [
                    [-4.066977024078369, -3.35385799407959, 0.0],
                    [-4.066977024078369, -3.35385799407959, 3.2],
                    [-5.92466402053833, 3.2412912845611572, 3.2],
                    [-5.92466402053833, 3.2412912845611572, 0.0],
                ],
                "default",
            ],
            [
                [
                    [-1.6831783056259155, 4.436010360717773, 0.0],
                    [-5.92466402053833, 3.2412912845611572, 0.0],
                    [-5.92466402053833, 3.2412912845611572, 3.2],
                    [-1.6831783056259155, 4.436010360717773, 3.2],
                ],
                "blank",
            ],
            [
                [
                    [-0.16507524251937866, -0.9535511136054993, 3.2],
                    [-0.16507524251937866, -0.9535511136054993, 0.0],
                    [-1.6831783056259155, 4.436010360717773, 0.0],
                    [-1.6831783056259155, 4.436010360717773, 3.2],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, -3.4308414459228516, 0.0],
                    [4.860907554626465, -3.9343056678771973, 0.0],
                    [3.7135703563690186, 0.1389651894569397, 0.0],
                    [5.088443279266357, 0.5262321829795837, 0.0],
                    [6.648303508758545, 0.9656053185462952, 0.0],
                    [6.648303508758545, -0.11789550632238388, 0.0],
                ],
                "default",
            ],
            [
                [
                    [4.860907554626465, -3.9343056678771973, 0.0],
                    [6.648303508758545, -3.4308414459228516, 0.0],
                    [6.648303508758545, -3.4308414459228516, 3.2],
                    [4.860907554626465, -3.9343056678771973, 3.2],
                ],
                "blank",
            ],
            [
                [
                    [6.648303508758545, -0.11789550632238388, 3.2],
                    [6.648303508758545, -3.4308414459228516, 3.2],
                    [6.648303508758545, -3.4308414459228516, 0.0],
                    [6.648303508758545, -0.11789550632238388, 0.0],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, 0.9656053185462952, 0.0],
                    [6.648303508758545, 0.9656053185462952, 3.2],
                    [6.648303508758545, -0.11789550632238388, 3.2],
                    [6.648303508758545, -0.11789550632238388, 0.0],
                ],
                "default",
            ],
            [
                [
                    [5.088443279266357, 0.5262321829795837, 3.2],
                    [6.648303508758545, 0.9656053185462952, 3.2],
                    [6.648303508758545, 0.9656053185462952, 0.0],
                    [5.088443279266357, 0.5262321829795837, 0.0],
                ],
                "default",
            ],
            [
                [
                    [3.7135703563690186, 0.1389651894569397, 3.2],
                    [5.088443279266357, 0.5262321829795837, 3.2],
                    [5.088443279266357, 0.5262321829795837, 0.0],
                    [3.7135703563690186, 0.1389651894569397, 0.0],
                ],
                "default",
            ],
            [
                [
                    [-0.16507524251937866, -0.9535511136054993, 0.0],
                    [-1.6831783056259155, 4.436010360717773, 0.0],
                    [3.570340394973755, 5.915793418884277, 0.0],
                    [5.088443279266357, 0.5262321829795837, 0.0],
                    [3.7135703563690186, 0.1389651894569397, 0.0],
                ],
                "default",
            ],
            [
                [
                    [5.088443279266357, 0.5262321829795837, 3.2],
                    [5.088443279266357, 0.5262321829795837, 0.0],
                    [3.570340394973755, 5.915793418884277, 0.0],
                    [3.570340394973755, 5.915793418884277, 3.2],
                ],
                "default",
            ],
            [
                [
                    [3.570340394973755, 5.915793418884277, 0.0],
                    [-1.6831783056259155, 4.436010360717773, 0.0],
                    [-1.6831783056259155, 4.436010360717773, 3.2],
                    [3.570340394973755, 5.915793418884277, 3.2],
                ],
                "blank",
            ],
            [
                [
                    [3.7135703563690186, 0.1389651894569397, 3.2],
                    [5.088443279266357, 0.5262321829795837, 3.2],
                    [3.570340394973755, 5.915793418884277, 3.2],
                    [-1.6831783056259155, 4.436010360717773, 3.2],
                    [-0.16507524251937866, -0.9535511136054993, 3.2],
                ],
                "default",
            ],
            [
                [
                    [11.776132583618164, -1.986461877822876, 0.0],
                    [6.648303508758545, -3.4308414459228516, 0.0],
                    [6.648303508758545, -0.11789550632238388, 0.0],
                    [11.776132583618164, 0.07600060105323792, 0.0],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, -3.4308414459228516, 0.0],
                    [11.776132583618164, -1.986461877822876, 0.0],
                    [11.776132583618164, -1.986461877822876, 3.2],
                    [6.648303508758545, -3.4308414459228516, 3.2],
                ],
                "blank",
            ],
            [
                [
                    [11.776132583618164, 0.07600060105323792, 0.0],
                    [11.776132583618164, 0.07600060105323792, 3.2],
                    [11.776132583618164, -1.986461877822876, 3.2],
                    [11.776132583618164, -1.986461877822876, 0.0],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, -0.11789550632238388, 3.2],
                    [11.776132583618164, 0.07600060105323792, 3.2],
                    [11.776132583618164, 0.07600060105323792, 0.0],
                    [6.648303508758545, -0.11789550632238388, 0.0],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, -3.4308414459228516, 3.2],
                    [11.776132583618164, -1.986461877822876, 3.2],
                    [11.776132583618164, 0.07600060105323792, 3.2],
                    [6.648303508758545, -0.11789550632238388, 3.2],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, -0.11789550632238388, 0.0],
                    [6.648303508758545, 0.9656053185462952, 0.0],
                    [6.648303508758545, 6.782777786254883, 0.0],
                    [11.776132583618164, 8.227157592773438, 0.0],
                    [11.776132583618164, 0.07600060105323792, 0.0],
                ],
                "default",
            ],
            [
                [
                    [11.776132583618164, 0.07600060105323792, 0.0],
                    [11.776132583618164, 8.227157592773438, 0.0],
                    [11.776132583618164, 8.227157592773438, 3.2],
                    [11.776132583618164, 0.07600060105323792, 3.2],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, 6.782777786254883, 0.0],
                    [6.648303508758545, 6.782777786254883, 3.2],
                    [11.776132583618164, 8.227157592773438, 3.2],
                    [11.776132583618164, 8.227157592773438, 0.0],
                ],
                "blank",
            ],
            [
                [
                    [6.648303508758545, 6.782777786254883, 3.2],
                    [6.648303508758545, 6.782777786254883, 0.0],
                    [6.648303508758545, 0.9656053185462952, 0.0],
                    [6.648303508758545, 0.9656053185462952, 3.2],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, -0.11789550632238388, 3.2],
                    [11.776132583618164, 0.07600060105323792, 3.2],
                    [11.776132583618164, 8.227157592773438, 3.2],
                    [6.648303508758545, 6.782777786254883, 3.2],
                ],
                "nonplanar",
            ],
            [
                [
                    [5.088443279266357, 0.5262321829795837, 0.0],
                    [3.570340394973755, 5.915793418884277, 0.0],
                    [6.648303508758545, 6.782777786254883, 0.0],
                    [6.648303508758545, 0.9656053185462952, 0.0],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, 6.782777786254883, 3.2],
                    [6.648303508758545, 6.782777786254883, 0.0],
                    [3.570340394973755, 5.915793418884277, 0.0],
                    [3.570340394973755, 5.915793418884277, 3.2],
                ],
                "blank",
            ],
            [
                [
                    [3.570340394973755, 5.915793418884277, 3.2],
                    [5.088443279266357, 0.5262321829795837, 3.2],
                    [6.648303508758545, 0.9656053185462952, 3.2],
                    [6.648303508758545, 6.782777786254883, 3.2],
                ],
                "default",
            ],
            [
                [
                    [-5.92466402053833, 3.2412912845611572, 6.2],
                    [-4.066977024078369, -3.35385799407959, 6.2],
                    [0.1745082139968872, -2.1591389179229736, 6.2],
                    [-0.16507533192634583, -0.9535511136054993, 6.2],
                    [-1.683178424835205, 4.436010360717773, 6.2],
                ],
                "default",
            ],
            [
                [
                    [-4.066977024078369, -3.35385799407959, 6.2],
                    [-3.259223461151123, -6.221540927886963, 6.2],
                    [0.9822618961334229, -5.026822090148926, 6.2],
                    [0.1745082139968872, -2.1591389179229736, 6.2],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, -3.4308414459228516, 6.2],
                    [11.776132583618164, -1.986461877822876, 6.2],
                    [11.776132583618164, 0.07600060105323792, 6.2],
                    [6.648303508758545, -0.11789550632238388, 6.2],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, -0.11789550632238388, 6.2],
                    [11.776132583618164, 0.07600060105323792, 6.2],
                    [11.776132583618164, 8.227157592773438, 6.2],
                    [6.648303508758545, 6.782777786254883, 6.2],
                ],
                "nonplanar",
            ],
            [
                [
                    [3.570340394973755, 5.915793418884277, 6.2],
                    [5.088443279266357, 0.5262321829795837, 6.2],
                    [6.648303508758545, 0.9656053185462952, 6.2],
                    [6.648303508758545, 6.782777786254883, 6.2],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, -0.11789550632238388, 3.2],
                    [6.648303508758545, 0.9656053185462952, 3.2],
                    [6.648303508758545, 0.9656053185462952, 6.2],
                    [6.648303508758545, -0.11789550632238388, 6.2],
                ],
                "default",
            ],
            [
                [
                    [3.7135703563690186, 0.1389651894569397, 3.2],
                    [5.088443279266357, 0.5262321829795837, 3.2],
                    [5.088443279266357, 0.5262321829795837, 6.2],
                    [3.7135703563690186, 0.1389651894569397, 6.2],
                ],
                "default",
            ],
            [
                [
                    [-4.066977024078369, -3.35385799407959, 3.2],
                    [-3.259223461151123, -6.221540927886963, 3.2],
                    [-3.259223461151123, -6.221540927886963, 6.2],
                    [-4.066977024078369, -3.35385799407959, 6.2],
                ],
                "default",
            ],
            [
                [
                    [3.570340394973755, 5.915793418884277, 3.2],
                    [-1.6831783056259155, 4.436010360717773, 3.2],
                    [-1.683178424835205, 4.436010360717773, 6.2],
                    [3.570340394973755, 5.915793418884277, 6.2],
                ],
                "blank",
            ],
            [
                [
                    [6.648303508758545, 6.782777786254883, 3.2],
                    [3.570340394973755, 5.915793418884277, 3.2],
                    [3.570340394973755, 5.915793418884277, 6.2],
                    [6.648303508758545, 6.782777786254883, 6.2],
                ],
                "blank",
            ],
            [
                [
                    [-0.16507524251937866, -0.9535511136054993, 3.2],
                    [3.7135703563690186, 0.1389651894569397, 3.2],
                    [3.7135703563690186, 0.1389651894569397, 6.2],
                    [-0.16507533192634583, -0.9535511136054993, 6.2],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, 6.782777786254883, 3.2],
                    [6.648303508758545, 0.9656053185462952, 3.2],
                    [6.648303508758545, 0.9656053185462952, 6.2],
                    [6.648303508758545, 6.782777786254883, 6.2],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, 0.9656053185462952, 3.2],
                    [5.088443279266357, 0.5262321829795837, 3.2],
                    [5.088443279266357, 0.5262321829795837, 6.2],
                    [6.648303508758545, 0.9656053185462952, 6.2],
                ],
                "default",
            ],
            [
                [
                    [11.776132583618164, -1.986461877822876, 3.2],
                    [11.776132583618164, 0.07600060105323792, 3.2],
                    [11.776132583618164, 0.07600060105323792, 6.2],
                    [11.776132583618164, -1.986461877822876, 6.2],
                ],
                "default",
            ],
            [
                [
                    [11.776132583618164, 0.07600060105323792, 3.2],
                    [11.776132583618164, 8.227157592773438, 3.2],
                    [11.776132583618164, 8.227157592773438, 6.2],
                    [11.776132583618164, 0.07600060105323792, 6.2],
                ],
                "default",
            ],
            [
                [
                    [3.570340394973755, 5.915793418884277, 3.2],
                    [5.088443279266357, 0.5262321829795837, 3.2],
                    [5.088443279266357, 0.5262321829795837, 6.2],
                    [3.570340394973755, 5.915793418884277, 6.2],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, -3.4308414459228516, 3.2],
                    [6.648303508758545, -0.11789550632238388, 3.2],
                    [6.648303508758545, -0.11789550632238388, 6.2],
                    [6.648303508758545, -3.4308414459228516, 6.2],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, -0.11789550632238388, 3.2],
                    [11.776132583618164, 0.07600060105323792, 3.2],
                    [11.776132583618164, 0.07600060105323792, 6.2],
                    [6.648303508758545, -0.11789550632238388, 6.2],
                ],
                "default",
            ],
            [
                [
                    [3.7135703563690186, 0.1389651894569397, 3.2],
                    [4.860907554626465, -3.9343056678771973, 3.2],
                    [4.860907554626465, -3.9343056678771973, 6.2],
                    [3.7135703563690186, 0.1389651894569397, 6.2],
                ],
                "default",
            ],
            [
                [
                    [11.776132583618164, 8.227157592773438, 3.2],
                    [6.648303508758545, 6.782777786254883, 3.2],
                    [6.648303508758545, 6.782777786254883, 6.2],
                    [11.776132583618164, 8.227157592773438, 6.2],
                ],
                "blank",
            ],
            [
                [
                    [-3.259223461151123, -6.221540927886963, 3.2],
                    [0.9822620153427124, -5.026822090148926, 3.2],
                    [0.9822618961334229, -5.026822090148926, 6.2],
                    [-3.259223461151123, -6.221540927886963, 6.2],
                ],
                "blank",
            ],
            [
                [
                    [-0.16507524251937866, -0.9535511136054993, 3.2],
                    [-1.6831783056259155, 4.436010360717773, 3.2],
                    [-1.683178424835205, 4.436010360717773, 6.2],
                    [-0.16507533192634583, -0.9535511136054993, 6.2],
                ],
                "default",
            ],
            [
                [
                    [0.9822620153427124, -5.026822090148926, 3.2],
                    [0.17450830340385437, -2.1591389179229736, 3.2],
                    [0.1745082139968872, -2.1591389179229736, 6.2],
                    [0.9822618961334229, -5.026822090148926, 6.2],
                ],
                "default",
            ],
            [
                [
                    [-5.92466402053833, 3.2412912845611572, 3.2],
                    [-4.066977024078369, -3.35385799407959, 3.2],
                    [-4.066977024078369, -3.35385799407959, 6.2],
                    [-5.92466402053833, 3.2412912845611572, 6.2],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, -3.4308414459228516, 3.2],
                    [11.776132583618164, -1.986461877822876, 3.2],
                    [11.776132583618164, -1.986461877822876, 6.2],
                    [6.648303508758545, -3.4308414459228516, 6.2],
                ],
                "blank",
            ],
            [
                [
                    [0.17450830340385437, -2.1591389179229736, 3.2],
                    [-0.16507524251937866, -0.9535511136054993, 3.2],
                    [-0.16507533192634583, -0.9535511136054993, 6.2],
                    [0.1745082139968872, -2.1591389179229736, 6.2],
                ],
                "default",
            ],
            [
                [
                    [-1.6831783056259155, 4.436010360717773, 3.2],
                    [-5.92466402053833, 3.2412912845611572, 3.2],
                    [-5.92466402053833, 3.2412912845611572, 6.2],
                    [-1.683178424835205, 4.436010360717773, 6.2],
                ],
                "blank",
            ],
            [
                [
                    [4.860907554626465, -3.9343056678771973, 3.2],
                    [6.648303508758545, -3.4308414459228516, 3.2],
                    [6.648303508758545, -3.4308414459228516, 6.2],
                    [4.860907554626465, -3.9343056678771973, 6.2],
                ],
                "blank",
            ],
            [
                [
                    [3.7135703563690186, 0.1389651894569397, 6.2],
                    [4.860907554626465, -3.9343056678771973, 6.2],
                    [6.648303508758545, -3.4308414459228516, 6.2],
                    [6.648303508758545, -0.11789550632238388, 6.2],
                    [6.648303508758545, 0.9656053185462952, 6.2],
                    [5.088443279266357, 0.5262321829795837, 6.2],
                ],
                "default",
            ],
            [
                [
                    [3.7135703563690186, 0.1389651894569397, 6.2],
                    [5.088443279266357, 0.5262321829795837, 6.2],
                    [3.570340394973755, 5.915793418884277, 6.2],
                    [-1.683178424835205, 4.436010360717773, 6.2],
                    [-0.16507533192634583, -0.9535511136054993, 6.2],
                ],
                "default",
            ],
            [
                [
                    [3.7135703563690186, 0.1389651894569397, 9.2],
                    [5.088443279266357, 0.5262321829795837, 9.2],
                    [3.570340394973755, 5.915793418884277, 9.2],
                    [-1.6831785440444946, 4.436010360717773, 9.2],
                    [-0.1650754064321518, -0.9535511136054993, 9.2],
                ],
                "default",
            ],
            [
                [
                    [3.7135703563690186, 0.1389651894569397, 6.2],
                    [4.860907554626465, -3.9343056678771973, 6.2],
                    [4.860907554626465, -3.9343056678771973, 9.2],
                    [3.7135703563690186, 0.1389651894569397, 9.2],
                ],
                "default",
            ],
            [
                [
                    [5.088443279266357, 0.5262321829795837, 6.2],
                    [3.570340394973755, 5.915793418884277, 6.2],
                    [3.570340394973755, 5.915793418884277, 9.2],
                    [5.088443279266357, 0.5262321829795837, 9.2],
                ],
                "default",
            ],
            [
                [
                    [3.7135703563690186, 0.1389651894569397, 6.2],
                    [5.088443279266357, 0.5262321829795837, 6.2],
                    [5.088443279266357, 0.5262321829795837, 9.2],
                    [3.7135703563690186, 0.1389651894569397, 9.2],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, 0.9656053185462952, 6.2],
                    [5.088443279266357, 0.5262321829795837, 6.2],
                    [5.088443279266357, 0.5262321829795837, 9.2],
                    [6.648303508758545, 0.9656053185462952, 9.2],
                ],
                "default",
            ],
            [
                [
                    [3.570340394973755, 5.915793418884277, 6.2],
                    [-1.683178424835205, 4.436010360717773, 6.2],
                    [-1.6831785440444946, 4.436010360717773, 9.2],
                    [3.570340394973755, 5.915793418884277, 9.2],
                ],
                "blank",
            ],
            [
                [
                    [4.860907554626465, -3.9343056678771973, 6.2],
                    [6.648303508758545, -3.4308414459228516, 6.2],
                    [6.648303508758545, -3.4308414459228516, 9.2],
                    [4.860907554626465, -3.9343056678771973, 9.2],
                ],
                "blank",
            ],
            [
                [
                    [6.648303508758545, -3.4308414459228516, 6.2],
                    [6.648303508758545, -0.11789550632238388, 6.2],
                    [6.648303508758545, -0.11789550632238388, 9.2],
                    [6.648303508758545, -3.4308414459228516, 9.2],
                ],
                "default",
            ],
            [
                [
                    [-0.16507533192634583, -0.9535511136054993, 6.2],
                    [3.7135703563690186, 0.1389651894569397, 6.2],
                    [3.7135703563690186, 0.1389651894569397, 9.2],
                    [-0.1650754064321518, -0.9535511136054993, 9.2],
                ],
                "default",
            ],
            [
                [
                    [-1.683178424835205, 4.436010360717773, 6.2],
                    [-0.16507533192634583, -0.9535511136054993, 6.2],
                    [-0.1650754064321518, -0.9535511136054993, 9.2],
                    [-1.6831785440444946, 4.436010360717773, 9.2],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, -0.11789550632238388, 6.2],
                    [6.648303508758545, 0.9656053185462952, 6.2],
                    [6.648303508758545, 0.9656053185462952, 9.2],
                    [6.648303508758545, -0.11789550632238388, 9.2],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, -3.4308414459228516, 10.2],
                    [9.212218284606934, -2.708651542663574, 11.13025188446045],
                    [9.212218284606934, -0.02094745635986328, 11.13025188446045],
                    [6.648303508758545, -0.11789550632238388, 10.2],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, -0.11789550632238388, 10.2],
                    [9.212218284606934, -0.02094745635986328, 11.13025188446045],
                    [9.212218284606934, 7.50496768951416, 11.13025188446045],
                    [6.648303508758545, 6.782777786254883, 10.2],
                ],
                "default",
            ],
            [
                [
                    [-3.8039212226867676, 3.838650703430176, 11.081135749816895],
                    [-1.9462344646453857, -2.756498336791992, 11.081135749816895],
                    [0.17450807988643646, -2.1591389179229736, 10.2],
                    [-0.16507546603679657, -0.9535511136054993, 10.2],
                    [-1.6831785440444946, 4.436010360717773, 10.2],
                ],
                "default",
            ],
            [
                [
                    [9.212218284606934, -2.708651542663574, 11.13025188446045],
                    [11.776132583618164, -1.986461877822876, 10.2],
                    [11.776132583618164, 0.07600060105323792, 10.2],
                    [9.212218284606934, -0.02094745635986328, 11.13025188446045],
                ],
                "default",
            ],
            [
                [
                    [9.212218284606934, -0.02094745635986328, 11.13025188446045],
                    [11.776132583618164, 0.07600060105323792, 10.2],
                    [11.776132583618164, 8.227157592773438, 10.2],
                    [9.212218284606934, 7.50496768951416, 11.13025188446045],
                ],
                "default",
            ],
            [
                [
                    [-5.92466402053833, 3.2412912845611572, 6.2],
                    [-4.066977024078369, -3.35385799407959, 6.2],
                    [-4.066977024078369, -3.35385799407959, 10.2],
                    [-5.92466402053833, 3.2412912845611572, 10.2],
                ],
                "pantsy",
            ],
            [
                [
                    [0.1745082139968872, -2.1591389179229736, 6.2],
                    [-0.16507533192634583, -0.9535511136054993, 6.2],
                    [-0.16507546603679657, -0.9535511136054993, 10.2],
                    [0.17450807988643646, -2.1591389179229736, 10.2],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, 6.782777786254883, 6.2],
                    [6.648303508758545, 0.9656053185462952, 6.2],
                    [6.648303508758545, 0.9656053185462952, 10.2],
                    [6.648303508758545, 6.782777786254883, 10.2],
                ],
                "default",
            ],
            [
                [
                    [-1.683178424835205, 4.436010360717773, 6.2],
                    [-5.92466402053833, 3.2412912845611572, 6.2],
                    [-5.92466402053833, 3.2412912845611572, 10.2],
                    [-3.8039212226867676, 3.838650703430176, 11.081135749816895],
                    [-1.6831785440444946, 4.436010360717773, 10.2],
                ],
                "blank",
            ],
            [
                [
                    [11.776132583618164, 0.07600060105323792, 6.2],
                    [11.776132583618164, 8.227157592773438, 6.2],
                    [11.776132583618164, 8.227157592773438, 10.2],
                    [11.776132583618164, 0.07600060105323792, 10.2],
                ],
                "pantsy",
            ],
            [
                [
                    [11.776132583618164, -1.986461877822876, 6.2],
                    [11.776132583618164, 0.07600060105323792, 6.2],
                    [11.776132583618164, 0.07600060105323792, 10.2],
                    [11.776132583618164, -1.986461877822876, 10.2],
                ],
                "pantsy",
            ],
            [
                [
                    [6.648303508758545, -0.11789550632238388, 6.2],
                    [6.648303508758545, -3.4308414459228516, 6.2],
                    [6.648303508758545, -3.4308414459228516, 10.2],
                    [6.648303508758545, -0.11789550632238388, 10.2],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, -0.11789550632238388, 6.2],
                    [11.776132583618164, 0.07600060105323792, 6.2],
                    [11.776132583618164, 0.07600060105323792, 10.2],
                    [9.212218284606934, -0.02094745635986328, 11.13025188446045],
                    [6.648303508758545, -0.11789550632238388, 10.2],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, -3.4308414459228516, 6.2],
                    [11.776132583618164, -1.986461877822876, 6.2],
                    [11.776132583618164, -1.986461877822876, 10.2],
                    [9.212218284606934, -2.708651542663574, 11.13025188446045],
                    [6.648303508758545, -3.4308414459228516, 10.2],
                ],
                "blank",
            ],
            [
                [
                    [11.776132583618164, 8.227157592773438, 6.2],
                    [6.648303508758545, 6.782777786254883, 6.2],
                    [6.648303508758545, 6.782777786254883, 10.2],
                    [9.212218284606934, 7.50496768951416, 11.13025188446045],
                    [11.776132583618164, 8.227157592773438, 10.2],
                ],
                "blank",
            ],
            [
                [
                    [-0.16507533192634583, -0.9535511136054993, 6.2],
                    [-1.683178424835205, 4.436010360717773, 6.2],
                    [-1.6831785440444946, 4.436010360717773, 10.2],
                    [-0.16507546603679657, -0.9535511136054993, 10.2],
                ],
                "default",
            ],
            [
                [
                    [6.648303508758545, 0.9656053185462952, 6.2],
                    [6.648303508758545, -0.11789550632238388, 6.2],
                    [6.648303508758545, -0.11789550632238388, 10.2],
                    [6.648303508758545, 0.9656053185462952, 10.2],
                ],
                "default",
            ],
            [
                [
                    [-4.066977024078369, -3.35385799407959, 6.2],
                    [0.1745082139968872, -2.1591389179229736, 6.2],
                    [0.17450807988643646, -2.1591389179229736, 10.2],
                    [-1.9462344646453857, -2.756498336791992, 11.081135749816895],
                    [-4.066977024078369, -3.35385799407959, 10.2],
                ],
                "default",
            ],
            [
                [
                    [-5.92466402053833, 3.2412912845611572, 10.2],
                    [-4.066977024078369, -3.35385799407959, 10.2],
                    [-1.9462344646453857, -2.756498336791992, 11.081135749816895],
                    [-3.8039212226867676, 3.838650703430176, 11.081135749816895],
                ],
                "default",
            ],
            [
                [
                    [3.7135703563690186, 0.1389651894569397, 9.2],
                    [4.860907554626465, -3.9343056678771973, 9.2],
                    [6.648303508758545, -3.4308414459228516, 9.2],
                    [6.648303508758545, 0.9656053185462952, 9.2],
                    [5.088443279266357, 0.5262321829795837, 9.2],
                ],
                "default",
            ],
            [
                [
                    [3.7135703563690186, 0.1389651894569397, 3.2],
                    [5.088443279266357, 0.5262321829795837, 3.2],
                    [6.648303508758545, 0.9656053185462952, 3.2],
                    [6.648303508758545, -3.4308414459228516, 3.2],
                    [4.860907554626465, -3.9343056678771973, 3.2],
                ],
                "nonplanar",
            ],
        ]

        widgets = []
        for widget in widgets_text:
            vertex = Vertex.ByCoordinates(*widget[1])
            widgets.append([widget[0], vertex])

        faces_ptr = []
        for face in faces_text:
            face_ptr = Face.ByVertices([Vertex.ByCoordinates(*v) for v in face[0]])
            face_ptr.Set("stylename", face[1])
            faces_ptr.append(face_ptr)

        # Generate a Topologic CellComplex
        self.cc = CellComplex.ByFaces(faces_ptr, 0.0001)
        # Copy styles from Faces to the CellComplex
        self.cc.ApplyDictionary(faces_ptr)
        wipe_global_cluster([self.cc])
        # Assign Cell usages from widgets
        self.cc.AllocateCells(widgets)
        wipe_global_cluster([self.cc])
        # Generate a circulation Graph
        self.circulation = Graph.Adjacency(self.cc)
        self.circulation.Circulation(self.cc)
        self.shortest_path_table = self.circulation.ShortestPathTable()
        self.circulation.Separation(self.shortest_path_table, self.cc)

    def test_circulation(self):
        cells_ptr = []
        self.cc.Cells(cells_ptr)
        self.assertTrue(self.circulation.IsConnected())

        assessor = p159_light_on_two_sides_of_every_room.Assessor(
            self.cc, self.circulation, self.shortest_path_table
        )
        for cell in cells_ptr:
            assessor.execute(cell)


if __name__ == "__main__":
    unittest.main()
