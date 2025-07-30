# 📦 FlowViewFt - Enrutador dinámico para Flet

**FlowViewFt** es una librería modular diseñada para simplificar la creación, organización y navegación entre vistas en proyectos desarrollados con [Flet](https://flet.dev). Su enfoque está basado en el concepto de **"flujo" (Flow)**, permitiendo transiciones naturales y estructuradas entre páginas, lo que facilita el mantenimiento y la escalabilidad del código.

---

## 🚀 Instalación

```bash
pip install FlowViewFt
```

---

## 🧠 Conceptos Clave

- `FlowViewFtParams`: Encapsula los parámetros que se pueden pasar entre rutas.
- `FlowViewFtState`: Maneja el estado de una vista o componente de forma organizada.
- `FlowViewFtView`: Clase base para construir vistas reutilizables e independientes.

---

## ⚙️ Uso básico

### `main.py`

```python
import flet as ft
from FlowViewFt import FlowViewFt, route
from view.home_view import HomeView
from view.counter_view import CounterView

def main(page: ft.Page):
    page.title = "Counter App"

    FlowViewFt(
        page=page,
        routes=[
            route("/", HomeView),
            route("/counter", CounterView),
        ],
        init_route="/",
    )

ft.app(target=main)
```

---
### `state/CounterState.py`
```python
from FlowViewFt import FlowViewFtState
import flet as ft
class counter_state(FlowViewFtState):
    def __init__(self, page):
        super().__init__(page)
        self.txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(self,e):
        if self.txt_number.value is not None:
            self.txt_number.value = str(int(self.txt_number.value) - 1)
        self.update()

    def plus_click(self,e):
        if self.txt_number.value is not None:
            self.txt_number.value = str(int(self.txt_number.value) + 1)
        self.update()

```

### `view/home_view.py`

```python
import flet as ft
from FlowViewFt import FlowViewFtView

class HomeView(FlowViewFtView):
    def build(self):
        return ft.View(
            controls=[
                ft.Text("Welcome to CounterApp", size=30),
                ft.ElevatedButton(
                    "Go to Counter", 
                    on_click=lambda _: self.page.go("/counter")
                ),
            ]
        )
```

---

### `view/counter_view.py`

```python
import flet as ft
from FlowViewFt import FlowViewFtView
from state.CounterState import counter_state

class CounterView(FlowViewFtView):
    def __init__(self, page):
        super().__init__(page)
        self.state = counter_state(self.page)

    def build(self):
        return ft.View(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(ft.Icons.REMOVE, on_click=self.state.minus_click),
                        self.state.txt_number,
                        ft.IconButton(ft.Icons.ADD, on_click=self.state.plus_click),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.ElevatedButton(
                    "Go to Home",
                    on_click=lambda _: self.pop_go("/"),
                ),
            ]
        )
```

---


## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Puedes enviar pull requests o sugerencias abriendo un issue en el [repositorio de GitHub](https://github.com/Hector3269/FlowViewFt.git).

---