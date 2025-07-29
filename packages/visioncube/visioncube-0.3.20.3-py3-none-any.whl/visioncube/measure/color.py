#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
author：yannan1
since：2024-03-22
"""
from typing import List

import cv2 as cv
import numpy as np

from ..common import AbstractTransform

__all__ = [
    "ColorMeasurement",
]


class ColorMeasurement(AbstractTransform):

    def __init__(self, poly_vertices=None):
        """ColorMeasurement, 颜色测量, 测量

        Args:
            poly_vertices: Polygon vertices, 候选区点集, [], []
        """
        super().__init__(use_gpu=False)
        if poly_vertices is None:
            poly_vertices = []
        self.poly_vertices = np.array(poly_vertices, np.int32)

    def _apply(self, sample):
        if sample.image is None:
            return sample
        image = sample.image

        if self.poly_vertices:
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            mask = cv.fillPoly(mask, pts=[self.poly_vertices], color=1)

            non_zero_indices = np.nonzero(mask)
            candidate = image[non_zero_indices]
        else:
            candidate = image

        sample.color_measure = {
            "mean": np.mean(candidate),
            "median": np.median(candidate),
            "max": np.max(candidate),
            "min": np.min(candidate),
            "std": np.std(candidate),
        }

        return sample
