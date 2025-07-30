# PINN 解法
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