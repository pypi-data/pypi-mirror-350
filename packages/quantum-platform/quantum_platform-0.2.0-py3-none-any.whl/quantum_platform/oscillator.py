# 一维谐振子
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