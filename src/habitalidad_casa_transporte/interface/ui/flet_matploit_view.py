from datetime import datetime
 
import flet as ft
import flet_charts as fch  
 
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import networkx as nx
 

BG = "#0b0720"
PANEL = "#150d33"
MORADO = "#8b5cf6"
CIAN = "#22d3ee"
VERDE = "#4ade80"
MAGENTA = "#e879f9"
TEXTO = "#e9e5ff"
TENUE = "#a78bfa"
 
 
def _borde(ancho, color):
    B = getattr(ft, "Border", None)
    if B is not None and hasattr(B, "all"):
        return B.all(ancho, color)
    return ft.border.all(ancho, color)
 
 
def _panel(contenido, color=MORADO, expand=False):
    return ft.Container(
        content=contenido,
        bgcolor=PANEL,
        border=_borde(1.5, color),
        border_radius=14,
        padding=16,
        expand=expand,
        shadow=ft.BoxShadow(blur_radius=18, color=ft.Colors.with_opacity(0.35, color)),
    )
 
 
def _boton(texto, icono, on_click, color=MORADO):
    return ft.Container(
        content=ft.Row(
            [ft.Icon(icono, color=TEXTO, size=22),
             ft.Text(texto, color=TEXTO, size=15, weight=ft.FontWeight.W_600)],
            tight=True, spacing=10,
        ),
        bgcolor=ft.Colors.with_opacity(0.25, color),
        border=_borde(1.5, color),
        border_radius=10,
        padding=ft.Padding.symmetric(horizontal=22, vertical=12)
        if hasattr(ft, "Padding") and hasattr(ft.Padding, "symmetric") else 12,
        ink=True,
        on_click=on_click,
        shadow=ft.BoxShadow(blur_radius=14, color=ft.Colors.with_opacity(0.4, color)),
    )
 
 
def _etiqueta(texto):
    return ft.Text(texto, size=11, color=TENUE, weight=ft.FontWeight.W_600)
 
 
class InterfazGrafo:
    def __init__(self, page, G, pos=None, usuario="NEO",
                 on_calcular=None, on_mapa_calor=None, on_seleccion=None):
        self.page = page
        self.G = G
        self.on_calcular = on_calcular
        self.on_mapa_calor = on_mapa_calor
        self.on_seleccion = on_seleccion
        self.seleccionados = []  
 
        if pos is None:
            if all("x" in d and "y" in d for _, d in G.nodes(data=True)):
                pos = {n: (d["x"], d["y"]) for n, d in G.nodes(data=True)}
            else:
                pos = nx.spring_layout(G, seed=7)
        self.ids = list(G.nodes)
        self.coords = np.array([pos[n] for n in self.ids], dtype=float)
 
        self._construir_mapa()
        self._construir_trafico()
        self._construir_ui(usuario)
        self.set_trafico([20, 25, 22, 35, 30, 45, 40, 55, 50, 70, 74],
                         [10, 15, 18, 20, 28, 25, 35, 38, 45, 50, 60])
 
    # ------------------------------------------------------------------
    # Mapa (Matplotlib)
    # ------------------------------------------------------------------
    def _construir_mapa(self):
        self.fig, self.ax = plt.subplots()
        self.fig.patch.set_facecolor(PANEL)
        self.fig.subplots_adjust(0, 0, 1, 1)
        self.ax.set_facecolor(PANEL)
        self.ax.axis("off")
 
        pos = {n: self.coords[i] for i, n in enumerate(self.ids)}
        segmentos = [(pos[u], pos[v]) for u, v in self.G.edges()]
        self.calles = LineCollection(segmentos, linewidths=0.6, colors="#6d4bc4",
                                     rasterized=True)
        self.ax.add_collection(self.calles)
        self.ax.autoscale()
        self.ax.set_aspect("equal")
        self.ax.margins(0.05)
        self._lim_inicial = (self.ax.get_xlim(), self.ax.get_ylim())
 
        self.sel_scatter = self.ax.scatter([], [], s=140, zorder=5,
                                           edgecolors="white", linewidths=1.2)
 
        self.fig.canvas.mpl_connect("button_press_event", self._al_clic)
        self.fig.canvas.mpl_connect("scroll_event", self._al_scroll)
 
        Clase = getattr(fch, "MatplotlibChartWithToolbar", fch.MatplotlibChart)
        self.chart = fch.MatplotlibChart(figure=self.fig, expand=True)
 
    def zoom(self, factor, cx=None, cy=None):
        x0, x1 = self.ax.get_xlim()
        y0, y1 = self.ax.get_ylim()
        cx = (x0 + x1) / 2 if cx is None else cx
        cy = (y0 + y1) / 2 if cy is None else cy
        self.ax.set_xlim(cx - (cx - x0) * factor, cx + (x1 - cx) * factor)
        self.ax.set_ylim(cy - (cy - y0) * factor, cy + (y1 - cy) * factor)
        self.fig.canvas.draw_idle()
 
    def reset_vista(self):
        self.ax.set_xlim(self._lim_inicial[0])
        self.ax.set_ylim(self._lim_inicial[1])
        self.fig.canvas.draw_idle()
 
    def _al_scroll(self, event):
        if event.inaxes is self.ax:
            self.zoom(0.8 if event.button == "up" else 1.25, event.xdata, event.ydata)
 
    def _al_clic(self, event):
        if event.inaxes is not self.ax or event.button != 1:
            return
        d = np.hypot(self.coords[:, 0] - event.xdata, self.coords[:, 1] - event.ydata)
        i = int(np.argmin(d))
        rango = self.ax.get_xlim()[1] - self.ax.get_xlim()[0]
        if d[i] > rango * 0.03:  
            return
        nodo = self.ids[i]
 
        self.txt_aviso.value = ""
        if nodo in self.seleccionados:
            self.seleccionados.remove(nodo)
        elif len(self.seleccionados) < 2:
            self.seleccionados.append(nodo)
        else:
            self.txt_aviso.value = "Máximo 2 nodos: deselecciona uno primero"
        self._refrescar_seleccion()
 
    def _refrescar_seleccion(self):
        if self.seleccionados:
            idx = [self.ids.index(n) for n in self.seleccionados]
            self.sel_scatter.set_offsets(self.coords[idx])
            self.sel_scatter.set_facecolors([CIAN, MAGENTA][: len(idx)])
        else:
            self.sel_scatter.set_offsets(np.empty((0, 2)))
        self.fig.canvas.draw_idle()
 
        inicio = str(self.seleccionados[0]) if len(self.seleccionados) > 0 else "--"
        fin = str(self.seleccionados[1]) if len(self.seleccionados) > 1 else "--"
        self.v_inicio.value = inicio
        self.v_fin.value = fin
        self.btn_calcular.opacity = 1.0 if len(self.seleccionados) == 2 else 0.4
        self.btn_calcular.disabled = len(self.seleccionados) != 2
        self.page.update()
 
        if self.on_seleccion:
            self.on_seleccion(list(self.seleccionados))
 
    # ------------------------------------------------------------------
    # Gráfica de tráfico (Matplotlib, estilo oscuro)
    # ------------------------------------------------------------------
    def _construir_trafico(self):
        self.fig_t, self.ax_t = plt.subplots()
        self.fig_t.patch.set_facecolor(PANEL)
        self.chart_t = fch.MatplotlibChart(figure=self.fig_t, expand=True)
 
    def set_trafico(self, serie_a, serie_b=None):
        ax = self.ax_t
        ax.clear()
        ax.set_facecolor(PANEL)
        x = np.arange(len(serie_a))
        ax.fill_between(x, serie_a, color=MORADO, alpha=0.45)
        ax.plot(x, serie_a, color=MORADO, linewidth=1.8)
        if serie_b is not None:
            ax.fill_between(x, serie_b, color=CIAN, alpha=0.35)
            ax.plot(x, serie_b, color=CIAN, linewidth=1.8)
        ax.set_ylim(0, 100)
        ax.set_yticks([0, 20, 40, 60, 80])
        ax.set_yticklabels([f"{t}%" for t in [0, 20, 40, 60, 80]])
        ax.tick_params(colors=TENUE, labelsize=8)
        ax.grid(axis="y", color=TENUE, alpha=0.15)
        for s in ax.spines.values():
            s.set_visible(False)
        self.fig_t.subplots_adjust(left=0.1, right=0.98, top=0.95, bottom=0.12)
        self.fig_t.canvas.draw_idle()
 
    # ------------------------------------------------------------------
    # Interfaz Flet
    # ------------------------------------------------------------------
    def _construir_ui(self, usuario):
        page = self.page
        page.title = "Habitalidad de Transporte"
        page.bgcolor = BG
        page.padding = 20
        page.window.width = 1200
        page.window.height = 720
 
        # --- Encabezado ---
        encabezado = ft.Row(
            [
                ft.Row([ft.Icon(ft.Icons.HEXAGON_OUTLINED, color=MORADO, size=20),
                        ft.Text("UI", color=TEXTO, size=16)]),
                ft.Text(f"Test 0.1  |  User: {usuario}  |  Tiempo: "
                        f"{datetime.now().strftime('%H:%M')}",
                        color=TENUE, size=12),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
 
        # --- Panel de métricas ---
        self.txt_estado = ft.Text("ONLINE", size=26, color=VERDE, weight=ft.FontWeight.BOLD)
        self.txt_trafico = ft.Text("74%", size=30, color=VERDE, weight=ft.FontWeight.BOLD)
        self.txt_footer = ft.Text("TRAFICO: 1.2  |  NODOS: 2134531",
                                  size=12, color=VERDE)
        boton_power = ft.Container(
            content=ft.Icon(ft.Icons.POWER_SETTINGS_NEW, color=VERDE, size=22),
            width=44, height=44, border_radius=22,
            bgcolor=ft.Colors.with_opacity(0.2, VERDE),
            border=_borde(1, VERDE),
            alignment=ft.Alignment.CENTER if hasattr(ft, "Alignment") else None,
        )
 
        panel_metricas = _panel(
            ft.Column(
                [
                    ft.Text("DATOS DE NODOS Y METRICAS DE TRAFICO", size=15, color=TEXTO,
                            weight=ft.FontWeight.W_600),
                    ft.Row([ft.Column([_etiqueta("ESTADO"), self.txt_estado], spacing=0),
                            boton_power],
                           alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(color=ft.Colors.with_opacity(0.3, MORADO), height=1),
                    _etiqueta("RED DE TRAFICO"),
                    self.txt_trafico,
                    ft.Container(self.chart_t, expand=True),
                    self.txt_footer,
                ],
                spacing=8, expand=True,
            ),
            expand=True,
        )
 
        # --- Panel de la ruta ---
        def fila(label, valor_ctrl):
            return ft.Row([ft.Text(label, size=13, color=TEXTO), valor_ctrl],
                          spacing=6, tight=True)
 
        def valor(texto="--"):
            return ft.Text(texto, size=13, color=VERDE)
 
        self.v_inicio, self.v_fin, self.v_dist = valor(), valor(), valor()
        self.v_tiempo, self.v_paradas, self.v_giro = valor(), valor(), valor()
        self.txt_aviso = ft.Text("", size=12, color=MAGENTA)
 
        panel_ruta = _panel(
            ft.Column(
                [
                    ft.Text("DETALLES DE LA RUTA SELECCIONADA", size=15, color=TEXTO,
                            weight=ft.FontWeight.W_600),
                    ft.Row(
                        [
                            ft.Column([fila("PUNTO DE INICIO:", self.v_inicio),
                                       fila("PUNTO DE FIN:", self.v_fin),
                                       fila("DISTANCIA:", self.v_dist)],
                                      spacing=8, expand=True),
                            ft.Column([fila("TIEMPO ESTIMADO:", self.v_tiempo),
                                       fila("PARADAS:", self.v_paradas),
                                       fila("SIGUIENTE GIRO:", self.v_giro)],
                                      spacing=8, expand=True),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                    self.txt_aviso,
                ],
                spacing=10, tight=True,
            ),
        )
 
        # --- Panel del mapa ---
        botones_zoom = ft.Row(
            [
                _boton("AGRANDAR", ft.Icons.ADD, lambda e: self.zoom(0.7), CIAN),
                _boton("ACHICAR", ft.Icons.REMOVE, lambda e: self.zoom(1 / 0.7), CIAN),
                ft.IconButton(ft.Icons.HOME, icon_color=CIAN, tooltip="Restablecer vista",
                              on_click=lambda e: self.reset_vista()),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        panel_mapa = _panel(
            ft.Column(
                [botones_zoom,
                 ft.Container(self.chart, expand=True, border_radius=10,
                              border=_borde(1, ft.Colors.with_opacity(0.4, CIAN)))],
                spacing=12, expand=True,
            ),
            color=CIAN, expand=True,
        )
 
        # --- Botones inferiores ---
        self.btn_calcular = _boton("CALCULAR RUTA", ft.Icons.ALT_ROUTE, self._calcular)
        self.btn_calcular.opacity = 0.4
        self.btn_calcular.disabled = True  # se activa con 2 nodos
        btn_calor = _boton("MIRAR MAPA DE CALOR", ft.Icons.THERMOSTAT, self._calor)
 
        inferior = ft.Row([self.btn_calcular, btn_calor],
                          alignment=ft.MainAxisAlignment.CENTER, spacing=20)
 
        marco = ft.Container(
            content=ft.Column(
                [
                    encabezado,
                    ft.Row(
                        [ft.Column([panel_metricas, panel_ruta], expand=1, spacing=14),
                         ft.Container(panel_mapa, expand=1)],
                        spacing=18, expand=True,
                    ),
                    inferior,
                ],
                spacing=14, expand=True,
            ),
            border=_borde(1.5, ft.Colors.with_opacity(0.6, MORADO)),
            border_radius=24, padding=20, expand=True,
        )
        page.add(marco)
 
    def _calcular(self, e):
        if self.on_calcular and len(self.seleccionados) == 2:
            self.on_calcular(*self.seleccionados)
 
    def _calor(self, e):
        if self.on_mapa_calor:
            self.on_mapa_calor()
 
    # ------------------------------------------------------------------
    # API para tu lógica: actualiza los textos de la interfaz
    # ------------------------------------------------------------------
    def set_metricas(self, estado=None, trafico=None, ping=None, ancho_banda=None, nodos=None):
        if estado is not None:
            self.txt_estado.value = estado
        if trafico is not None:
            self.txt_trafico.value = f"{trafico}%"
        self.txt_footer.value = (f"PING: {ping}  |  BANDWIDTH: {ancho_banda}  |  NODES: {nodos}")
        self.page.update()
 
    def set_ruta(self, distancia=None, tiempo=None, paradas=None, giro=None):
        for ctrl, v in [(self.v_dist, distancia), (self.v_tiempo, tiempo),
                        (self.v_paradas, paradas), (self.v_giro, giro)]:
            if v is not None:
                ctrl.value = str(v)
        self.page.update()
 
 
def mostrar_interfaz(G, pos=None, usuario="NEO",
                     on_calcular=None, on_mapa_calor=None, on_seleccion=None):
    """Abre la interfaz y devuelve la lista [inicio, fin] seleccionada al cerrar."""
    resultado = []
 
    def main(page: ft.Page):
        ui = InterfazGrafo(page, G, pos, usuario, on_calcular, on_mapa_calor, on_seleccion)
        resultado.append(ui)
 
    ft.run(main)
    return list(resultado[0].seleccionados) if resultado else []
 
 
# ---------- Demo ----------

 
