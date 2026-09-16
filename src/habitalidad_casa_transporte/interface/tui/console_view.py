import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

console = Console()

def clear_terminal():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")


def start_menu(): 
    clear_terminal()


    start_text = (
        "[bold white] Bienvenido al calculador de habitabilidad del transporte[/bold white]"
    )

    console.print(
        Panel(
            start_text,
            title="[bold violet] HABITALIDAD DE TRANSPORTE [bold violet]",
            title_align="center",
            border_style="bold violet",
            padding=(1,1)
        )
    )
    console.print("")


    table = Table(show_header=False, box=False, padding=(0,2))
    table.add_row("[bold green]1.[/bold green]", "[bold white]Calcular Factibilidad[/bold white]", "[dim white]--Ejecutar con parametros definidos o predefinidos[/dim white]")
    table.add_row("[bold green]2.[/bold green]", "[bold white]Entrar a configuraciones[/bold white]" , "[dim white]--Modificar parametros[/dim white]")
    table.add_row("[bold green]3.[/bold green]", "[bold white]Salir del programa[/bold white]" , "[dim white]--Cerrar programa[/dim white]")

    console.print(table)

    console.print("\n" + "[bold violet]──" * 50 + "[bold violet]\n")


    option = Prompt.ask(
        "[bold yellow]Selecciona una de las opciones[/bold yellow]", 
        choices=["1", "2", "3"]
    )

    return option