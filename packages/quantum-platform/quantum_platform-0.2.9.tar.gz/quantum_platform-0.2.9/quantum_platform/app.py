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
from importlib import resources

# ---------------------- 公共设置 ----------------------
# 修改后的字体配置部分
matplotlib.rcParams['font.family'] = 'Microsoft YaHei'  
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']  # 优先使用微软雅黑
matplotlib.rcParams['axes.unicode_minus'] = False  # 保持负号正常显示
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'sans-serif']  # 简化配置
plt.rcParams['axes.unicode_minus'] = False  # 保持负号正常显示
matplotlib.use('Agg')  # 保持后端设置不变



# 使用一个1x1透明图片的base64数据作为占位符
placeholder_base64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAA"
    "AARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAWSURBVBhXY2AAAAACAAHiIbwzAAAAAElFTkSuQmCC"
)

##############################################################
#              量子力学教学可视化平台（初稿2）模块
##############################################################

# ================== 氢原子径向波函数相关函数 ==================
def numerov_hydrogen(n, l, r_max=20, num_points=1000):
    h = r_max / num_points
    r = np.linspace(h, r_max, num_points)

    def potential(r, l):
        return -1 / r + l * (l + 1) / (2 * r**2)

    def schrodinger_eq(r, y, E):
        psi, dpsi = y
        d2psi = 2 * (potential(r, l) - E) * psi
        return np.vstack((dpsi, d2psi))

    E_guess = -1 / (2 * n**2)

    def boundary_conditions(ya, yb):
        return np.array([ya[0], yb[0]])

    psi_init = np.exp(-r / n) * r**l
    dpsi_init = -psi_init / n
    y_init = np.vstack((psi_init, dpsi_init))

    sol = solve_bvp(lambda r, y: schrodinger_eq(r, y, E_guess), boundary_conditions, r, y_init)
    return r, sol.y[0]

def plot_wavefunction(n, l):
    r, psi = numerov_hydrogen(n, l)
    probability_density = psi**2  # 计算概率密度 |ψ|²

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(f"氢原子: n={n}, l={l}", fontsize=20)  # 原 fontsize=14

    axs[0].plot(r, psi, label=f"R_{n}{l}(r)")
    axs[0].set_xlabel("r")
    axs[0].set_ylabel("波函数 R_{nl}(r)")
    axs[0].set_title("径向波函数")
    axs[0].legend()
    axs[0].grid()

    axs[1].plot(r, probability_density, color='r', label=f"|R_{n}{l}(r)|^2")
    axs[1].set_xlabel("r")
    axs[1].set_ylabel("概率密度")
    axs[1].set_title("径向概率密度")
    axs[1].legend()
    axs[1].grid()

    img_path = f"波函数_{n}_{l}_{int(time.time())}.png"
    plt.savefig(img_path, bbox_inches='tight')
    plt.close(fig)
    return img_path

# ================== 主界面及各子页面 ==================


# 直接使用相对路径加载图片，避免 importlib.resources 的包资源问题
def load_image_base64():
    try:
        # __file__ 指向当前 app.py 的绝对路径
        pkg_dir = os.path.dirname(__file__)
        img_path = os.path.join(pkg_dir, "assets", "量子力学界面图.jpg")
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception as e:
        print(f"加载背景图失败: {e}")
        return None

IMAGE_BASE64 = load_image_base64()

class MainPage:
    def __init__(self, page: ft.Page):
        self.page = page
        page.padding = 0
        page.margin = ft.margin.all(0)
        page.scroll = "none"
        page.window_maximized = True
        page.title = "量子力学教学仿真平台"

        self.menu_items = [
            ("等概率密度面-物理视角", ft.Icons.SCIENCE, self.show_physics_orbitals),
            ("等概率密度面-化学视角", ft.Icons.HEXAGON, self.show_chemistry_orbitals),
            ("一维深势阱", ft.Icons.WAVES, self.show_schrodinger),
            ("一维谐振子", ft.Icons.TRENDING_UP, self.show_oscillator),
            ("氢原子R方向波函数", ft.Icons.IMAGE, self.show_hydrogen_radial),
            ("含时薛定谔方程势垒贯穿", ft.Icons.ANALYTICS, self.show_time_dependent),
            ("PINN 求解含时薛定谔方程", ft.Icons.AUTO_GRAPH, self.show_pinn_solver)
        ]
        self.create_main_ui()

    def build_buttons(self):
        buttons = []
        for text, icon, handler in self.menu_items:
            buttons.append(
                ft.ElevatedButton(
                    text=text,
                    icon=icon,
                    on_click=handler,
                    width=300,
                    height=100,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.WHITE54,
                        color=ft.Colors.BLACK,
                        overlay_color=ft.Colors.BLUE_100,
                        text_style=ft.TextStyle(size=20)
                    )
                )
            )
        return buttons

    def create_main_ui(self):
        controls = []
        if IMAGE_BASE64:
            controls.append(
                ft.Image(
                    src_base64=IMAGE_BASE64,
                    expand=True,
                    fit=ft.ImageFit.COVER
                )
            )
            controls.append(
                ft.Container(
                    bgcolor=ft.Colors.BLACK45,
                    expand=True
                )
            )

        title = ft.Text(
            "量子力学教学仿真平台",
            size=80,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE
        )
        divider = ft.Divider(height=30, color=ft.Colors.WHITE70)

        buttons = self.build_buttons()
        left = buttons[0:3]
        center = [buttons[3]]
        right = buttons[4:7]

        ui = ft.Container(
            content=ft.Column(
                [
                    title,
                    divider,
                    ft.Row([
                        ft.Column(left, alignment=ft.MainAxisAlignment.CENTER, spacing=50),
                        ft.Column(center, alignment=ft.MainAxisAlignment.CENTER),
                        ft.Column(right, alignment=ft.MainAxisAlignment.CENTER, spacing=50)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=80),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            expand=True,
            alignment=ft.alignment.center,
            padding=ft.padding.all(20)
        )
        controls.append(ui)
        self.page.add(ft.Stack(controls=controls, expand=True))

    # 跳转逻辑保留
    def show_physics_orbitals(self, e):    self.page.clean(); PhysicsOrbitalsPage(self.page)
    def show_chemistry_orbitals(self, e): self.page.clean(); ChemistryOrbitalsPage(self.page)
    def show_schrodinger(self, e):        self.page.clean(); SchrodingerApp(self.page)
    def show_oscillator(self, e):         self.page.clean(); HarmonicOscillatorPage(self.page)
    def show_hydrogen_radial(self, e):    self.page.clean(); HydrogenRadialPage(self.page)
    def show_time_dependent(self, e):     self.page.clean(); TimeDependentSchrodingerPage(self.page)
    def show_pinn_solver(self, e):        self.page.clean(); pinn_main(self.page)


def combined_main(page: ft.Page):
    page.padding = 0
    page.margin = ft.margin.all(0)
    page.scroll = "none"
    page.theme = ft.Theme(font_family="Microsoft YaHei")
    page.title = "量子力学教学平台（集成版）"
    MainPage(page)






# ---------------- 原子轨道物理视角页面 ----------------
class PhysicsOrbitalsPage:
    def __init__(self, page):
        self.page = page
        self.page.title = "等概率密度面物理视角"
        self.create_ui()

    def create_ui(self):
        self.n_input = ft.TextField(label="主量子数 n", value="2")
        self.l_input = ft.TextField(label="角量子数 l", value="1")
        self.m_input = ft.TextField(label="磁量子数 m", value="0")

        self.page.add(
            ft.Column([
                ft.Text("物理视角等概率密度面 (点击按钮生成交互图形)", size=24, weight=ft.FontWeight.BOLD),  # 原 size=24
                self.n_input,
                self.l_input,
                self.m_input,
                ft.Row([
                    ft.ElevatedButton("生成等概率密度面", on_click=self.update_plot),
                    ft.ElevatedButton("返回", on_click=self.go_back),
                ])
            ])
        )

    def hydrogen_wave_function(self, n, l, m):
        def R(r):
            factor = np.sqrt(2. / n) ** 3 * factorial(n - l - 1) / (2 * n * factorial(n + l))
            rho = 2 * r / n
            return factor * (rho ** l) * np.exp(-rho / 2) * genlaguerre(n - l - 1, 2 * l + 1)(rho)
        def Y(theta, phi):
            return sph_harm(m, l, phi, theta)
        return lambda r, theta, phi: R(r) * Y(theta, phi)

    def generate_plotly_plot(self, n, l, m):
        limit = 8 * (n / 1.5)
        n_points = 160 + 30 * n
        step = 2 * limit / (n_points - 1)
        vec = np.linspace(-limit, limit, n_points)
        X, Y_, Z = np.meshgrid(vec, vec, vec, sparse=True)
        R = np.sqrt(X**2 + Y_**2 + Z**2)
        R[R == 0] = 1e-10
        THETA = np.arccos(np.clip(Z / R, -1, 1))
        PHI = np.arctan2(Y_, X)
        psi = self.hydrogen_wave_function(n, l, m)
        psi_values = psi(R, THETA, PHI)
        prob_dens = np.abs(psi_values) ** 2
        iso_value = np.max(prob_dens) * (0.07 if l == 1 else 0.04)
        verts, faces, _, _ = marching_cubes(
            prob_dens, level=iso_value, spacing=(step, step, step), allow_degenerate=False
        )
        verts = verts - limit
        verts[:, [0, 1]] = verts[:, [1, 0]]
        face_centers = np.mean(verts[faces], axis=1)
        center_indices = np.round((face_centers + limit) / step).astype(int)
        center_indices = np.clip(center_indices, 0, n_points - 1)
        phase_values = np.angle(psi_values[
            center_indices[:, 0],
            center_indices[:, 1],
            center_indices[:, 2]
        ])
        phase_values = np.clip(phase_values, -0.5*np.pi, 0.5*np.pi)
        phase_values = phase_values / (0.5*np.pi)  # 标准化到[-1,1]
        fig = go.Figure(
            data=go.Mesh3d(
                x=verts[:, 0],
                y=verts[:, 1],
                z=verts[:, 2],
                i=faces[:, 0],
                j=faces[:, 1],
                k=faces[:, 2],
                intensity=phase_values,
                colorscale="RdBu_r", 
                cmin=-1,
                cmax=1,
                opacity=0.85,
                intensitymode='cell',
                lighting=dict(
                    ambient=0.45,
                    diffuse=0.85,
                    specular=0.35,
                    roughness=0.3,
                    fresnel=0.25
                ),
                lightposition=dict(x=300, y=300, z=300),
                flatshading=False,
                showscale=False
            )
        )
        fig.update_layout(
            title=dict(
                text=f"物理视角等概率密度面 n={n}, l={l}, m={m}", x=0.5, font_size=24  # 原 font_size=24
            ),
            scene=dict(
                xaxis=dict(title='X', showgrid=True, gridcolor='lightgray', zeroline=True, zerolinecolor='gray', tickfont=dict(size=12)),  # 原 tickfont size=12
                yaxis=dict(title='Y', showgrid=True, gridcolor='lightgray', zeroline=True, zerolinecolor='gray', tickfont=dict(size=12)),
                zaxis=dict(title='Z', showgrid=True, gridcolor='lightgray', zeroline=True, zerolinecolor='gray', tickfont=dict(size=12)),
                aspectmode='data',
                camera=dict(eye=dict(x=1.6, y=1.6, z=1.6))
            ),
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor='white'
        )
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
            fig.write_html(f.name)
            return f.name

    def update_plot(self, e):
        try:
            n = int(self.n_input.value)
            l = int(self.l_input.value)
            m = int(self.m_input.value)
            if l >= n or abs(m) > l:
                raise ValueError
            html_file = self.generate_plotly_plot(n, l, m)
            webbrowser.open("file://" + html_file)
        except:
            self.page.snack_bar = ft.SnackBar(ft.Text("无效的量子数或图形生成失败"))
            self.page.snack_bar.open = True
            self.page.update()

    def go_back(self, e):
        self.page.clean()
        combined_main(self.page)

# ---------------- 原子轨道化学视角页面 ----------------
class ChemistryOrbitalsPage:
    ORBITAL_GROUPS = {
        "s": ["z"],
        "p": ["x", "y", "z"],
        "d": ["z2", "xz", "yz", "xy", "x2y2"],
        "f": ["z3", "xz2", "yz2"]
    }

    def __init__(self, page):
        self.page = page
        self.page.title = "等概率密度面化学视角"
        self.create_ui()

    def create_ui(self):
        self.input_field = ft.TextField(label="输入参量（示例：2p 3d）", width=400)
        self.page.add(
            ft.Column([
                ft.Text("化学视角等概率密度面", size=24, weight=ft.FontWeight.BOLD),  # 原 size=24
                ft.Row([self.input_field, ft.ElevatedButton("生成等概率密度面", on_click=self.generate)]),
                ft.ElevatedButton("返回", on_click=self.go_back)
            ])
        )

    def parse_input(self, input_str):
        pattern = r"(\d+)([spdf])"
        matches = re.findall(pattern, input_str.lower())
        result = []
        for n_str, orb in matches:
            n = int(n_str)
            l = {"s": 0, "p": 1, "d": 2, "f": 3}[orb]
            orbitals = self.get_orbital_functions(n, l)
            for sub in self.ORBITAL_GROUPS[orb]:
                if sub in orbitals:
                    result.append((n, l, sub, orbitals[sub]))
        return result

    def get_orbital_functions(self, n, l):
        if l == 0:
            return {"z": lambda r, t, p: self.hydrogen_wave_function(n, 0, 0)(r, t, p)}
        elif l == 1:
            return {
                "z": self.hydrogen_wave_function(n, 1, 0),
                "x": lambda r, t, p: (self.hydrogen_wave_function(n, 1, 1)(r, t, p) +
                                      self.hydrogen_wave_function(n, 1, -1)(r, t, p)) / np.sqrt(2),
                "y": lambda r, t, p: (self.hydrogen_wave_function(n, 1, 1)(r, t, p) -
                                      self.hydrogen_wave_function(n, 1, -1)(r, t, p)) * 1j / np.sqrt(2)
            }
        elif l == 2:
            return {
                "z2": self.hydrogen_wave_function(n, 2, 0),
                "xz": lambda r, t, p: (self.hydrogen_wave_function(n, 2, 1)(r, t, p) +
                                       self.hydrogen_wave_function(n, 2, -1)(r, t, p)) / np.sqrt(2),
                "yz": lambda r, t, p: (self.hydrogen_wave_function(n, 2, 1)(r, t, p) -
                                       self.hydrogen_wave_function(n, 2, -1)(r, t, p)) * 1j / np.sqrt(2),
                "xy": lambda r, t, p: (self.hydrogen_wave_function(n, 2, 2)(r, t, p) +
                                       self.hydrogen_wave_function(n, 2, -2)(r, t, p)) / np.sqrt(2),
                "x2y2": lambda r, t, p: (self.hydrogen_wave_function(n, 2, 2)(r, t, p) -
                                         self.hydrogen_wave_function(n, 2, -2)(r, t, p)) / np.sqrt(2)
            }
        elif l == 3:
            return {
                "z3": self.hydrogen_wave_function(n, 3, 0),
                "xz2": lambda r, t, p: (self.hydrogen_wave_function(n, 3, 1)(r, t, p) +
                                        self.hydrogen_wave_function(n, 3, -1)(r, t, p)) / np.sqrt(2),
                "yz2": lambda r, t, p: (self.hydrogen_wave_function(n, 3, 1)(r, t, p) -
                                        self.hydrogen_wave_function(n, 3, -1)(r, t, p)) * 1j / np.sqrt(2)
            }
        return {}

    def hydrogen_wave_function(self, n, l, m):
        def R(r):
            factor = np.sqrt(2. / n) ** 3 * factorial(n - l - 1) / (2 * n * factorial(n + l))
            rho = 2 * r / n
            return factor * (rho ** l) * np.exp(-rho / 2) * genlaguerre(n - l - 1, 2 * l + 1)(rho)
        def Y(theta, phi):
            return sph_harm(m, l, phi, theta)
        return lambda r, theta, phi: R(r) * Y(theta, phi)

    def generate_plotly_html(self, n, l, sub, psi_func):
        limit = 6 * n ** 0.7
        n_points = 50 + 8 * n
        x = np.linspace(-limit, limit, n_points)
        X, Y_, Z = np.meshgrid(x, x, x, indexing='ij', sparse=True)
        R = np.sqrt(X**2 + Y_**2 + Z**2) + 1e-10
        theta = np.arccos(Z / R)
        phi = np.arctan2(Y_, X)
        psi_values = psi_func(R, theta, phi)
        prob_dens = np.abs(psi_values) ** 2
        iso_value = np.quantile(prob_dens[prob_dens > 0], 0.985)
        verts, faces, _, _ = marching_cubes(
            prob_dens, level=iso_value, spacing=(2 * limit / (n_points - 1),) * 3, method='lewiner'
        )
        verts -= limit
        verts[:, [0, 1]] = verts[:, [1, 0]]
        step = 2 * limit / (n_points - 1)
        face_centers = np.mean(verts[faces], axis=1)
        center_indices = np.round((face_centers + limit) / step).astype(int)
        center_indices = np.clip(center_indices, 0, n_points - 1)
        phase_values = np.angle(psi_values[
            center_indices[:, 0],
            center_indices[:, 1],
            center_indices[:, 2]
        ])
        phase_values = np.clip(phase_values, -0.5*np.pi, 0.5*np.pi)
        phase_values = phase_values / (0.5*np.pi)  # 标准化到[-1,1]
        fig = go.Figure(
            data=go.Mesh3d(
                x=verts[:, 0],
                y=verts[:, 1],
                z=verts[:, 2],
                i=faces[:, 0],
                j=faces[:, 1],
                k=faces[:, 2],
                intensity=phase_values,
                colorscale="RdBu_r", 
                cmin=-1,
                cmax=1,
                opacity=0.85,
                intensitymode='cell',
                lighting=dict(
                    ambient=0.45,
                    diffuse=0.85,
                    specular=0.35,
                    roughness=0.3,
                    fresnel=0.25
                ),
                lightposition=dict(x=300, y=300, z=300),
                flatshading=False,
                showscale=False
            )
        )
        fig.update_layout(
            title=dict(
                text=f"{n}{'spdf'[l]}-{sub} 等概率密度面", x=0.5, font_size=24  # 原 font_size=24
            ),
            scene=dict(
                xaxis=dict(title='X', showgrid=True, gridcolor='lightgray'),
                yaxis=dict(title='Y', showgrid=True, gridcolor='lightgray'),
                zaxis=dict(title='Z', showgrid=True, gridcolor='lightgray'),
                aspectmode='data',
                camera=dict(eye=dict(x=1.6, y=1.6, z=1.6))
            ),
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor='white'
        )
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
            fig.write_html(f.name)
            return f.name

    def generate(self, e):
        try:
            self.page.snack_bar = None
            parsed = self.parse_input(self.input_field.value.strip())
            if not parsed:
                raise ValueError("输入格式不正确")
            for n, l, sub, psi_func in parsed:
                html_file = self.generate_plotly_html(n, l, sub, psi_func)
                webbrowser.open("file://" + html_file)
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text("等概率密度面生成失败，请检查输入！"))
            self.page.snack_bar.open = True
            self.page.update()

    def go_back(self, e):
        self.page.clean()
        combined_main(self.page)

# ---------------- 薛定谔方程（深势阱）页面 ----------------
class SchrodingerApp:
    def __init__(self, page):
        self.page = page
        self.page.title = "薛定谔方程数值解"
        self.page.window_width = 1800
        self.page.window_height = 1600
        self.x = None
        self.V = None
        self.psi = None
        self.energies = None
        self.create_controls()
        self.create_plot()
        self.create_plot2()
        self.wavefunction_text = ft.Text("", selectable=True)
        self.probability_text = ft.Text("", selectable=True)
        self.page.add(
            ft.Row(
                [
                    ft.Column(self.controls + [self.wavefunction_text, self.probability_text], width=300, scroll=True),
                    ft.Column([self.plot_container, self.plot2_container], scroll=True)
                ],
                expand=True
            )
        )
    
    def create_controls(self):
        self.controls = []
        self.center = ft.TextField(label="势阱中心", value="-1.0")
        self.width = ft.TextField(label="势阱宽度", value="3.0")
        self.depth = ft.TextField(label="势阱深度", value="-5.0")
        self.x_range = ft.TextField(label="x范围", value="10")
        self.num_points = ft.TextField(label="网格点数", value="500")
        self.n_level = ft.Slider(
            min=1, 
            max=5, 
            divisions=4,
            label="能级选择",
            value=1
        )
        self.btn_calculate = ft.ElevatedButton(
            "计算",
            on_click=self.update_plot
        )
        self.btn_back = ft.ElevatedButton("返回主界面", on_click=self.go_back)
        self.controls.extend([
            ft.Text("势场参数", size=20),  # 原 size=20
            self.center,
            self.width,
            self.depth,
            self.x_range,
            self.num_points,
            ft.Text("选择能级"),
            self.n_level,
            self.btn_calculate,
            self.btn_back
        ])
    
    def create_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(16, 12))
        self.plot_container = ft.Image(src=placeholder_base64, width=1200, height=900)
    
    def create_plot2(self):
        self.fig2, self.ax2 = plt.subplots(figsize=(16, 12))
        self.plot2_container = ft.Image(src=placeholder_base64, width=1200, height=900)
    
    def temp_plot(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
            self.fig.savefig(f.name, dpi=100)
            return f.name
    
    def temp_plot2(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
            self.fig2.savefig(f.name, dpi=100)
            return f.name

    def potential(self, x, center, width, depth):
        return np.where((x >= center - width/2) & (x <= center + width/2), depth, 0)
    
    def solve_schrodinger(self, V, num_points):
        N = num_points
        dx = self.x[1] - self.x[0]
        main_diag = np.ones(N) / dx**2
        off_diag = -np.ones(N-1) / (2*dx**2)
        K = diags([main_diag, off_diag, off_diag], [0, -1, 1], shape=(N, N))
        U = diags(V, 0)
        H = K + U
        eigenvalues, eigenvectors = eigs(H, k=5, which='SR')
        eigenvalues = np.real(eigenvalues)
        eigenvectors = np.real(eigenvectors.T)
        idx = eigenvalues.argsort()
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[idx]
        for i in range(len(eigenvectors)):
            norm = np.sqrt(np.trapz(eigenvectors[i]**2, self.x))
            eigenvectors[i] /= norm
        return eigenvalues, eigenvectors
    
    def update_plot(self, e=None):
        try:
            center = float(self.center.value)
            width = float(self.width.value)
            depth = float(self.depth.value)
            x_range = float(self.x_range.value)
            num_points = int(self.num_points.value)
            n = int(self.n_level.value) - 1
        except ValueError:
            return
        self.x = np.linspace(-x_range/2, x_range/2, num_points)
        self.V = self.potential(self.x, center, width, depth)
        try:
            self.energies, self.psi = self.solve_schrodinger(self.V, num_points)
        except Exception as ex:
            print(f"求解薛定谔方程出错: {ex}")
            return
        self.ax.clear()
        self.ax.plot(self.x, self.V, 'k-', lw=2, label='Potential')
        if n < len(self.psi):
            psi = self.psi[n]
            energy = self.energies[n]
            self.ax.plot(self.x, psi + energy, 'r-', label=f'n={n+1}')
            self.ax.axhline(energy, color='gray', linestyle='--')
            indices = np.linspace(0, len(self.x)-1, 10, dtype=int)
            wavefunction_values = "\n".join(
                [f"x={self.x[i]:.2f}, ψ={psi[i]:.3f}" for i in indices]
            )
            self.wavefunction_text.value = f"波函数数值 (部分点):\n{wavefunction_values}"
            probability_values = "\n".join(
                [f"x={self.x[i]:.2f}, |ψ|²={psi[i]**2:.3f}" for i in indices]
            )
            self.probability_text.value = f"概率密度值 (部分点):\n{probability_values}"
        else:
            energy = 0
            self.wavefunction_text.value = "选定能级不存在"
            self.probability_text.value = "选定能级不存在"
        self.ax.set_xlabel('Position (x)', fontsize=18)  # 原 18
        self.ax.set_ylabel('Energy / Wavefunction', fontsize=18)  # 原 18
        self.ax.set_title(f'能级 E_{n+1} = {energy:.2f}', fontsize=18)  # 原 18
        self.ax.legend(fontsize=16)  # 原 16
        self.plot_container.src = self.temp_plot()
        self.ax2.clear()
        self.ax2.plot(self.x, self.V, 'k-', lw=2, label='Potential')
        if n < len(self.psi):
            psi = self.psi[n]
            self.ax2.plot(self.x, psi**2, 'b-', label=f'|ψ|², n={n+1}')
            self.ax2.set_title(f'能级 n={n+1} 的波函数模的平方', fontsize=18)  # 原 18
        self.ax2.set_xlabel('Position (x)', fontsize=18)  # 原 18
        self.ax2.set_ylabel('Probability Density', fontsize=18)  # 原 18
        self.ax2.legend(fontsize=16)  # 原 16
        self.plot2_container.src = self.temp_plot2()
        self.page.update()
    
    def go_back(self, e):
        self.page.clean()
        combined_main(self.page)

# ---------------- 谐振子页面 ----------------
class HarmonicOscillatorPage:
    def __init__(self, page):
        self.page = page
        self.page.title = "一维线性谐振子"
        self.n_slider = ft.Slider(min=0, max=10, divisions=10, label="量子数 n={value}")
        self.k_input = ft.TextField(label="势场强度 k", value="1.0")
        self.btn_calculate = ft.ElevatedButton("计算", on_click=self.update_plot)
        self.btn_back = ft.ElevatedButton("返回主界面", on_click=self.go_back)
        self.img = ft.Image(src=placeholder_base64, width=1000, height=700)
        self.img2 = ft.Image(src=placeholder_base64, width=1000, height=700)
        self.probability_text = ft.Text("", selectable=True)
        self.page.add(
            ft.Row([ 
                ft.Column(
                    [
                        ft.Text("量子谐振子波函数可视化", size=24, weight=ft.FontWeight.BOLD),  # 原 size=24
                        ft.Text("量子数 n"),
                        self.n_slider,
                        ft.Text("势场强度 k"),
                        self.k_input,
                        self.btn_calculate,
                        self.btn_back,
                        self.probability_text
                    ],
                    scroll=True,
                    width=300
                ),
                ft.Column(
                    [
                        self.img,
                        self.img2
                    ],
                    scroll=True
                )
            ], expand=True)
        )
    
    def psi_n(self, n, x, k):
        m = 1.0
        hbar = 1.0
        omega = np.sqrt(k / m)
        alpha = m * omega / hbar
        H_n = hermite(n)
        normalization = (alpha / np.pi)**0.25 / np.sqrt(2**n * math.factorial(n))
        return normalization * H_n(np.sqrt(alpha) * x) * np.exp(-alpha * x**2 / 2)
    
    def create_figure(self, n, k):
        plt.figure(figsize=(12, 6))
        omega = np.sqrt(k / 1.0)
        alpha = omega
        x_max = 6 / np.sqrt(alpha)
        x = np.linspace(-x_max, x_max, 1000)
        psi = self.psi_n(n, x, k)
        potential = 0.5 * k * x**2
        ax1 = plt.gca()
        ax1.plot(x, psi, color='blue', label=f'ψ_{n}(x)')
        ax1.set_xlabel("位置 x", fontsize=18)  # 原 18
        ax1.set_ylabel("波函数", color='blue', fontsize=18)  # 原 18
        ax1.tick_params(axis='y', labelcolor='blue', labelsize=16)  # 原 16
        ax1.tick_params(axis='x', labelsize=16)  # 原 16
        ax1.set_ylim(-0.8, 0.8)
        ax2 = ax1.twinx()
        ax2.plot(x, potential, color='red', linestyle='--', alpha=0.7, label='势能 V(x)')
        ax2.set_ylabel("势能", color='red', fontsize=18)  # 原 18
        ax2.tick_params(axis='y', labelcolor='red', labelsize=16)  # 原 16
        ax2.set_ylim(0, 1.2*k*x_max**2)
        plt.title(f"量子谐振子 (n={n}, k={k:.1f})", fontsize=16)  # 原 16
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=16)  # 原 16
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=150)
        plt.close()
        buf.seek(0)
        return buf, x, psi
    
    def create_figure2(self, n, k, x, psi):
        plt.figure(figsize=(12, 6))
        potential = 0.5 * k * x**2
        ax1 = plt.gca()
        ax1.plot(x, psi**2, color='green', label=f'|ψ_{n}(x)|²')
        ax1.set_xlabel("位置 x", fontsize=18)  # 原 18
        ax1.set_ylabel("概率密度", color='green', fontsize=18)  # 原 18
        ax1.tick_params(axis='y', labelcolor='green', labelsize=16)  # 原 16
        ax1.tick_params(axis='x', labelsize=16)  # 原 16
        ax1.set_ylim(0, np.max(psi**2)*1.2)
        ax2 = ax1.twinx()
        ax2.plot(x, potential, color='red', linestyle='--', alpha=0.7, label='势能 V(x)')
        ax2.set_ylabel("势能", color='red', fontsize=18)  # 原 18
        ax2.tick_params(axis='y', labelcolor='red', labelsize=16)  # 原 16
        ax2.set_ylim(0, 1.2*k*np.max(x)**2)
        plt.title(f"量子谐振子 |ψ|^2 (n={n}, k={k:.1f})", fontsize=16)  # 原 16
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=16)  # 原 16
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=150)
        plt.close()
        buf.seek(0)
        return buf

    def update_plot(self, e):
        n = int(self.n_slider.value)
        try:
            k = float(self.k_input.value)
        except ValueError:
            k = 1.0
        buf1, x, psi = self.create_figure(n, k)
        self.img.src_base64 = base64.b64encode(buf1.getvalue()).decode("utf-8")
        indices = np.linspace(0, len(x)-1, 10, dtype=int)
        prob_values = "\n".join([f"x={x[i]:.2f}, |ψ|²={psi[i]**2:.3f}" for i in indices])
        self.probability_text.value = f"概率密度值 (部分点):\n{prob_values}"
        buf2 = self.create_figure2(n, k, x, psi)
        self.img2.src_base64 = base64.b64encode(buf2.getvalue()).decode("utf-8")
        self.page.update()
    
    def go_back(self, e):
        self.page.clean()
        MainPage(self.page)

# ---------------- 氢原子径向波函数页面 ----------------
class HydrogenRadialPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "氢原子径向波函数求解器"
        self.create_ui()

    def create_ui(self):
        # — 输入框 —
        self.n_input = ft.TextField(
            label="主量子数 (n)",
            value="1",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=120
        )
        self.l_input = ft.TextField(
            label="角量子数 (l)",
            value="0",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=120
        )

        # 把输入行整体下移 40px
        input_row = ft.Container(
            content=ft.Row(
                [self.n_input, self.l_input],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ),
            margin=ft.Margin(0, 40, 0, 0)  # left=0, top=40, right=0, bottom=0
        )

        # — 占位图 —
        self.image = ft.Image(
            src=placeholder_base64,
            width=800, height=500,
            fit=ft.ImageFit.CONTAIN
        )

        # — 错误提示 —
        self.error_text = ft.Text("", color="red", visible=False)

        # — 大按钮 —
        self.calc_button = ft.ElevatedButton(
            "计算波函数",
            on_click=self.update_plot,
            width=200, height=60,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=24))
        )
        self.back_button = ft.ElevatedButton(
            "返回",
            on_click=self.go_back,
            width=200, height=60,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=24))
        )

        # — 按钮行，向下推 40px —
        button_row = ft.Container(
            content=ft.Row(
                [self.calc_button, self.back_button],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=40
            ),
            margin=ft.Margin(0, 40, 0, 0)
        )

        # — 图片外层容器，同样向下推 40px —
        image_container = ft.Container(
            self.image,
            alignment=ft.alignment.center,
            margin=ft.Margin(0, 40, 0, 0)
        )

        # — 主布局，不使用滚动 —
        self.page.add(
            ft.Column(
                [
                    input_row,        # 输入行（已下移）
                    button_row,       # 按钮行
                    self.error_text,  # 错误提示
                    image_container   # 图像展示
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

    def update_plot(self, e):
        try:
            n = int(self.n_input.value)
            l = int(self.l_input.value)
            if l >= n:
                raise ValueError("角量子数 l 必须小于主量子数 n")
            if n < 1 or l < 0:
                raise ValueError("n 必须≥1，l 必须≥0")
            img_path = plot_wavefunction(n, l)
            # 强制刷新图像
            self.image.src = ""
            self.page.update()
            self.image.src = img_path
            self.error_text.visible = False
        except Exception as ex:
            self.error_text.value = f"错误: {ex}"
            self.error_text.visible = True
        self.page.update()

    def go_back(self, e):
        self.page.clean()
        combined_main(self.page)


# ---------------- 含时薛定谔方程求解（势垒贯穿）页面 ----------------
class TimeDependentSchrodingerPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.resume_event = threading.Event()
        self.stop_event = threading.Event()
        self.simulation_thread = None
        self.build_ui()

    def build_ui(self):
        p = self.page
        p.title = "含时薛定谔方程求解 - 势垒贯穿"

        # —— 参数输入框实例化 —— #
        self.txtV0    = ft.TextField(label="势垒高度 V₀", value="1.0", width=120)
        self.txtW     = ft.TextField(label="势垒宽度 w",  value="1.0", width=120)
        self.txtX0    = ft.TextField(label="波包中心 x₀", value="-5.0", width=120)
        self.txtSigma = ft.TextField(label="波包宽度 σ", value="1.0", width=120)
        self.txtP0    = ft.TextField(label="初始动量 p₀", value="5.0", width=120)
        self.txtdx    = ft.TextField(label="空间步长 dx", value="0.1", width=120)
        self.txtdt    = ft.TextField(label="时间步长 dt", value="0.005", width=120)
        self.txtL     = ft.TextField(label="空间区间长度 L", value="20.0", width=120)
        self.txtT     = ft.TextField(label="总模拟时间 T", value="2.0", width=120)

        # 用 Container 包裹 Column 来设置内边距
        inputs = ft.Container(
            content=ft.Column([
                ft.Row([self.txtV0,    self.txtW,    self.txtX0   ], spacing=20),
                ft.Row([self.txtSigma, self.txtP0                ], spacing=20),
                ft.Row([self.txtdx,    self.txtdt               ], spacing=20),
                ft.Row([self.txtL,     self.txtT                ], spacing=20),
            ], spacing=15),
            padding=20
        )

        # 信息显示
        self.txtMsg  = ft.Text("", color="red")
        self.txtNorm = ft.Text("归一化：", size=16)

        # 按钮区
        self.btnStart = ft.ElevatedButton(
            "开始模拟", on_click=self.start_click,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=18))
        )
        self.btnPause = ft.ElevatedButton(
            "暂停", disabled=True, on_click=self.pause_click,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=18))
        )
        self.btnReset = ft.ElevatedButton(
            "重置", disabled=True, on_click=self.reset_click,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=18))
        )
        button_row = ft.Row(
            [self.btnStart, self.btnPause, self.btnReset],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=40
        )

        # 返回主界面按钮
        back_button = ft.ElevatedButton("返回主界面", on_click=self.go_back)

        # 初始化空白图像
        self.blank_image_base64 = (
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=="
        )
        self.imgPlot = ft.Image(
            src_base64=self.blank_image_base64,
            width=800, height=600
        )

        # 用 ListView 作为可滚动主容器
        main_view = ft.ListView(
            expand=True,
            padding=20,
            spacing=20,
            auto_scroll=False,  # 自动滚到底部可根据需求开关
            controls=[
                inputs,
                self.txtMsg,
                self.txtNorm,
                button_row,
                self.imgPlot,
                back_button
            ]
        )

        p.add(main_view)

    def simulation_run(self):
        try:
            V0    = float(self.txtV0.value)
            w     = float(self.txtW.value)
            x0    = float(self.txtX0.value)
            sigma = float(self.txtSigma.value)
            p0    = float(self.txtP0.value)
            dx    = float(self.txtdx.value)
            dt    = float(self.txtdt.value)
            L     = float(self.txtL.value)
            T     = float(self.txtT.value)
        except Exception as e:
            self.txtMsg.value = f"参数输入错误：{e}"
            self.page.update()
            return

        self.txtMsg.value = ""
        self.page.update()

        N    = int(L / dx)
        x    = np.linspace(-L/2, L/2, N)
        k    = fft.fftfreq(N, d=dx) * 2 * np.pi
        norm = (1/(np.pi * sigma**2))**0.25
        psi  = norm * np.exp(- (x - x0)**2 / (2 * sigma**2)) * np.exp(1j * p0 * x)
        V    = V0 * (np.abs(x) < (w/2)).astype(float)
        expV = np.exp(-1j * V * dt/2)
        expK = np.exp(-1j * (k**2) * dt/2)
        steps = int(T / dt)

        for i in range(steps):
            if self.stop_event.is_set():
                break
            self.resume_event.wait()

            # Strang 分裂步
            psi = expV * psi
            psi = fft.ifft(expK * fft.fft(psi))
            psi = expV * psi

            # 保持归一化
            norm_val = np.sqrt(np.sum(np.abs(psi)**2) * dx)
            if np.abs(norm_val - 1.0) > 1e-3:
                psi = psi / norm_val

            # 每隔若干步更新图像
            if i % 10 == 0:
                plt.clf()
                plt.figure(figsize=(10, 6))
                plt.plot(x, np.abs(psi)**2, label=r"$|\psi(x)|^2$")
                plt.plot(x, V, label="V(x)")
                plt.xlabel("x")
                plt.ylabel("概率密度")
                plt.title(f"Time = {i*dt:.3f}")
                plt.legend()
                buf = io.BytesIO()
                plt.savefig(buf, format="png", bbox_inches="tight")
                buf.seek(0)
                img_data = base64.b64encode(buf.getvalue()).decode("utf-8")
                self.imgPlot.src_base64 = img_data
                self.txtNorm.value = f"归一化：{norm_val:.4f}"
                self.page.update()
                time.sleep(0.01)

        # 恢复按钮状态
        self.btnPause.disabled = True
        self.btnReset.disabled = True
        self.btnStart.disabled = False
        self.page.update()

    def start_click(self, e):
        self.stop_event.clear()
        self.resume_event.set()
        self.btnStart.disabled = True
        self.btnPause.disabled = False
        self.btnReset.disabled = False
        self.page.update()
        threading.Thread(target=self.simulation_run, daemon=True).start()

    def pause_click(self, e):
        if self.resume_event.is_set():
            self.resume_event.clear()
            self.btnPause.text = "恢复"
        else:
            self.resume_event.set()
            self.btnPause.text = "暂停"
        self.page.update()

    def reset_click(self, e):
        self.stop_event.set()
        self.resume_event.set()
        time.sleep(0.1)
        self.imgPlot.src_base64 = self.blank_image_base64
        self.txtNorm.value = "归一化："
        self.btnStart.disabled = False
        self.btnPause.disabled = True
        self.btnPause.text = "暂停"
        self.btnReset.disabled = True
        self.page.update()

    def go_back(self, e):
        self.page.clean()
        combined_main(self.page)









##############################################################
#                  PINN 含时薛定谔方程模块
##############################################################

# ---------------------- 势能函数 ----------------------
def get_potential(x, potential_type):
    if potential_type == "harmonic":
        return 0.5 * x ** 2
    elif potential_type == "square_well":
        return torch.where(torch.abs(x) <= 1.0, torch.zeros_like(x), 50.0 * torch.ones_like(x))
    elif potential_type == "barrier":
        return torch.where(torch.abs(x) <= 0.5, 20.0 * torch.ones_like(x), torch.zeros_like(x))
    else:
        return 0.5 * x ** 2

# ---------------------- PINN 模型 ----------------------
class PINN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 64),
            nn.Tanh(),
            nn.Linear(64, 64),
            nn.Tanh(),
            nn.Linear(64, 2)
        )
    
    def forward(self, xt):
        return self.net(xt)

# ---------------------- PINN 求解器 ----------------------
class SchrodingerSolver:
    def __init__(self, potential_type="harmonic", T=1.0):
        self.potential_type = potential_type
        self.T = T
        self.reset_model()

    def reset_model(self):
        self.model = PINN()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        self.loss_history = []
        self.running = False

    def physics_loss(self, collocation_points):
        collocation_points.requires_grad_(True)
        output = self.model(collocation_points)
        u = output[:, 0]
        v = output[:, 1]
        grads_u = torch.autograd.grad(u.sum(), collocation_points, create_graph=True)[0]
        u_x = grads_u[:, 0]
        u_t = grads_u[:, 1]
        grads_v = torch.autograd.grad(v.sum(), collocation_points, create_graph=True)[0]
        v_x = grads_v[:, 0]
        v_t = grads_v[:, 1]
        u_xx = torch.autograd.grad(u_x.sum(), collocation_points, create_graph=True)[0][:, 0]
        v_xx = torch.autograd.grad(v_x.sum(), collocation_points, create_graph=True)[0][:, 0]
        x = collocation_points[:, 0:1]
        V = get_potential(x, self.potential_type).squeeze()
        residual1 = v_t - (0.5 * u_xx - V * u)
        residual2 = u_t + (0.5 * v_xx - V * v)
        return torch.mean(residual1**2 + residual2**2)

    def initial_loss(self, initial_points):
        output = self.model(initial_points)
        u = output[:, 0]
        v = output[:, 1]
        x = initial_points[:, 0]
        psi0 = torch.exp(-x**2)
        loss_ic = torch.mean((u - psi0)**2 + v**2)
        return loss_ic

    def boundary_loss(self, boundary_points):
        output = self.model(boundary_points)
        u = output[:, 0]
        v = output[:, 1]
        loss_bound = torch.mean(u**2 + v**2)
        return loss_bound

    def train(self, epochs, progress_callback):
        self.running = True
        N_coll = 200
        N_ic = 50
        N_bound = 50
        for epoch in range(epochs):
            if not self.running:
                break
            x_coll = -5 + 10 * torch.rand(N_coll, 1)
            t_coll = self.T * torch.rand(N_coll, 1)
            collocation = torch.cat([x_coll, t_coll], dim=1)
            x_ic = -5 + 10 * torch.rand(N_ic, 1)
            t_ic = torch.zeros_like(x_ic)
            initial = torch.cat([x_ic, t_ic], dim=1)
            t_bound = self.T * torch.rand(N_bound, 1)
            x_bound_left = -5 * torch.ones(N_bound, 1)
            x_bound_right = 5 * torch.ones(N_bound, 1)
            boundary = torch.cat([torch.cat([x_bound_left, t_bound], dim=1),
                                  torch.cat([x_bound_right, t_bound], dim=1)], dim=0)
            loss_pde = self.physics_loss(collocation)
            loss_ic = self.initial_loss(initial)
            loss_bound = self.boundary_loss(boundary)
            total_loss = loss_pde + loss_ic + loss_bound
            self.optimizer.zero_grad()
            total_loss.backward()
            self.optimizer.step()
            self.loss_history.append(total_loss.item())
            progress_callback(epoch + 1, total_loss.item())
        self.running = False

# ---------------- PINN UI 部分 ----------------
def pinn_main(page: ft.Page):
    page.title = "PINN 含时薛定谔方程求解器"
    page.scroll = "auto"
    solver = SchrodingerSolver(potential_type="harmonic", T=1.0)
    epochs = ft.TextField(label="训练周期数", value="1000")
    potential_selector = ft.Dropdown(
        label="选择势能",
        value="harmonic",
        options=[
            ft.dropdown.Option("harmonic", "谐振子势"),
            ft.dropdown.Option("square_well", "方势阱"),
            ft.dropdown.Option("barrier", "势垒")
        ]
    )
    start_btn = ft.ElevatedButton("开始训练")
    stop_btn = ft.ElevatedButton("停止训练", disabled=True)
    reset_btn = ft.ElevatedButton("重置模型")
    progress_bar = ft.ProgressBar(width=600)
    status = ft.Text("准备就绪")
    loss_chart = ft.Image(src_base64=placeholder_base64, width=800, height=300)
    wave_chart = ft.Image(src_base64=placeholder_base64, width=800, height=300)
    psi_mod_chart = ft.Image(src_base64=placeholder_base64, width=800, height=300)

    def fig_to_base64(fig):
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        plt.close(fig)
        return base64.b64encode(buf.getvalue()).decode("utf-8")

    def update_plots():
        fig1, ax1 = plt.subplots(figsize=(8, 3))
        ax1.plot(solver.loss_history, label="Loss")
        ax1.set_title("训练损失")
        ax1.set_xlabel("周期")
        ax1.set_ylabel("Loss")
        ax1.legend()
        loss_chart.src_base64 = fig_to_base64(fig1)
        loss_chart.update()
        t_fixed = solver.T
        x_plot = torch.linspace(-5, 5, 200).view(-1, 1)
        t_plot = t_fixed * torch.ones_like(x_plot)
        xt_plot = torch.cat([x_plot, t_plot], dim=1)
        with torch.no_grad():
            output = solver.model(xt_plot)
        u = output[:, 0].numpy()
        v = output[:, 1].numpy()
        psi_mod = (output[:, 0]**2 + output[:, 1]**2).numpy()
        fig2, ax2 = plt.subplots(figsize=(8, 3))
        ax2.plot(x_plot.numpy(), u, label="Re(ψ)")
        ax2.plot(x_plot.numpy(), v, label="Im(ψ)")
        ax2.set_title(f"波函数 ψ(x, t={t_fixed:.2f})")
        ax2.set_xlabel("x")
        ax2.legend()
        wave_chart.src_base64 = fig_to_base64(fig2)
        wave_chart.update()
        fig3, ax3 = plt.subplots(figsize=(8, 3))
        ax3.plot(x_plot.numpy(), psi_mod, label="|ψ|^2", color="red")
        ax3.set_title(f"波函数模平方 |ψ(x, t={t_fixed:.2f})|^2")
        ax3.set_xlabel("x")
        ax3.legend()
        psi_mod_chart.src_base64 = fig_to_base64(fig3)
        psi_mod_chart.update()

    def update_progress(epoch, loss):
        def main_thread_update():
            progress_bar.value = epoch / int(epochs.value)
            status.value = f"周期: {epoch}/{epochs.value}  Loss: {loss:.4e}"
            update_plots()
            page.update()
        if hasattr(page, "call_from_main_thread"):
            page.call_from_main_thread(main_thread_update)
        else:
            main_thread_update()

    def start_train(e):
        try:
            epoch_count = int(epochs.value)
        except ValueError:
            status.value = "请输入有效的训练周期数！"
            page.update()
            return
        solver.potential_type = potential_selector.value
        start_btn.disabled = True
        stop_btn.disabled = False
        reset_btn.disabled = True
        status.value = "训练中..."
        page.update()
        threading.Thread(target=solver.train, args=(epoch_count, update_progress), daemon=True).start()

    def stop_train(e):
        solver.running = False
        start_btn.disabled = False
        stop_btn.disabled = True
        reset_btn.disabled = False
        status.value = "训练已停止"
        page.update()

    def reset_model(e):
        solver.reset_model()
        solver.potential_type = potential_selector.value
        status.value = "模型已重置"
        progress_bar.value = 0
        loss_chart.src_base64 = placeholder_base64
        wave_chart.src_base64 = placeholder_base64
        psi_mod_chart.src_base64 = placeholder_base64
        loss_chart.update()
        wave_chart.update()
        psi_mod_chart.update()
        page.update()

    # 添加“返回主界面”的按钮
    back_button = ft.ElevatedButton("返回主界面", on_click=lambda e: [page.clean(), combined_main(page)])
    
    start_btn.on_click = start_train
    stop_btn.on_click = stop_train
    reset_btn.on_click = reset_model

    page.add(
        ft.Row([epochs, potential_selector, start_btn, stop_btn, reset_btn], alignment="center"),
        progress_bar,
        status,
        ft.Text("训练损失", size=20, weight="bold"),  # 原 size=20
        ft.Row([loss_chart], alignment="center"),
        ft.Text("波函数 (Re & Im)", size=20, weight="bold"),  # 原 size=20
        ft.Row([wave_chart], alignment="center"),
        ft.Text("波函数模平方 |ψ|^2", size=20, weight="bold"),  # 原 size=20
        ft.Row([psi_mod_chart], alignment="center"),
        back_button
    )

##############################################################
#                    整合后的主程序入口
##############################################################
def combined_main(page: ft.Page):
    # —— 全局字体设置为微软雅黑 ——
    page.theme = ft.Theme(font_family="Microsoft YaHei")
    page.title = "量子力学教学仿真平台（集成版）"
    MainPage(page)

if __name__ == "__main__":
    ft.app(target=combined_main)


