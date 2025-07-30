import numpy as np
import re
import math
import flet as ft
import matplotlib
import base64
from scipy.special import factorial, genlaguerre, sph_harm, hermite
from scipy.sparse import diags
from scipy.sparse.linalg import eigs
from skimage.measure import marching_cubes
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from io import BytesIO
import tempfile
import webbrowser
import plotly.graph_objects as go
from scipy.integrate import solve_bvp
import os
import time
import numpy.fft as fft
import io
import threading
import torch
import torch.nn as nn
from quantum_platform.main_page import MainPage

def main(page: ft.Page):
    app = MainPage(page)
    app.build()

if __name__ == "__main__":
    ft.app(target=main)
