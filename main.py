import flet as ft

def main(page: ft.Page):
    
    page.title = "Calculadora Genérica - Diagrama de Venn"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 550 
    page.window_height = 650
    page.theme_mode = ft.ThemeMode.DARK

    
    def calcular(e):
        try:
            
            universo_val = int(universo.value)
            conjunto_a_val = int(conjunto_a.value)
            conjunto_b_val = int(conjunto_b.value)
            intersecao_val = int(intersecao.value)

            if conjunto_a_val < intersecao_val or conjunto_b_val < intersecao_val:
                resultado_geral.value = "Erro: A interseção não pode ser maior que os conjuntos."

                resultado_apenas_a.value = ""
                resultado_apenas_b.value = ""
                resultado_uniao.value = ""
                resultado_nenhum.value = ""
                page.update()
                return
            
            if (conjunto_a_val + conjunto_b_val - intersecao_val) > universo_val:
                resultado_geral.value = "Erro: A união dos conjuntos é maior que o universo."
                resultado_apenas_a.value = ""
                resultado_apenas_b.value = ""
                resultado_uniao.value = ""
                resultado_nenhum.value = ""
                page.update()
                return

            
            apenas_a = conjunto_a_val - intersecao_val
            apenas_b = conjunto_b_val - intersecao_val
            uniao = conjunto_a_val + conjunto_b_val - intersecao_val
            nenhum = universo_val - uniao

            
            resultado_geral.value = "Resultados Calculados:"
            resultado_apenas_a.value = f"Elementos que pertencem APENAS ao Conjunto A: {apenas_a}"
            resultado_apenas_b.value = f"Elementos que pertencem APENAS ao Conjunto B: {apenas_b}"
            resultado_uniao.value = f"Total de elementos na União (A ∪ B): {uniao}"
            resultado_nenhum.value = f"Elementos fora da união (não pertencem a A nem a B): {nenhum}"

        except (ValueError, TypeError):
            resultado_geral.value = "Erro: Por favor, preencha todos os campos com números válidos."
            resultado_apenas_a.value = ""
            resultado_apenas_b.value = ""
            resultado_uniao.value = ""
            resultado_nenhum.value = ""
        
        page.update()

    universo = ft.TextField(label="Tamanho do Conjunto Universo (Total)", width=450, keyboard_type=ft.KeyboardType.NUMBER)
    conjunto_a = ft.TextField(label="Número de elementos no Conjunto A", width=450, keyboard_type=ft.KeyboardType.NUMBER)
    conjunto_b = ft.TextField(label="Número de elementos no Conjunto B", width=450, keyboard_type=ft.KeyboardType.NUMBER)
    intersecao = ft.TextField(label="Número de elementos na Interseção (A ∩ B)", width=450, keyboard_type=ft.KeyboardType.NUMBER)

    botao_calcular = ft.ElevatedButton(text="Calcular", on_click=calcular)

    resultado_geral = ft.Text("", size=16, weight=ft.FontWeight.BOLD)
    resultado_apenas_a = ft.Text("")
    resultado_apenas_b = ft.Text("")
    resultado_uniao = ft.Text("")
    resultado_nenhum = ft.Text("")

    page.add(
        ft.Text("Calculadora Genérica de Diagrama de Venn", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("Insira os valores para os conjuntos A, B e o Universo:", size=14),
        universo,
        conjunto_a,
        conjunto_b,
        intersecao,
        botao_calcular,
        ft.Divider(), 
        resultado_geral,
        resultado_apenas_a,
        resultado_apenas_b,
        resultado_uniao,
        resultado_nenhum,
    ) 
    
if __name__ == "__main__":
    ft.app(target=main)