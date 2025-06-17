import flet as ft
from itertools import combinations

def main(page: ft.Page):
    
    page.title = "Calculadora de Venn - Múltiplos Conjuntos"
    page.vertical_alignment = ft.MainAxisAlignment.START # Mudei para START para lidar com o scroll
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 600
    page.window_height = 750
    page.theme_mode = ft.ThemeMode.DARK

    
    # As chaves serão tuplas, ex: ('A',) para o conjunto A, ('A', 'B') para a interseção A e B.
    campos_input = {}

    # Coluna que abrigará os campos de entrada gerados, com scroll.
    coluna_campos = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, spacing=10, height=350)
    
    # --- Controles de Resultado ---
    resultado_geral = ft.Text("", size=16, weight=ft.FontWeight.BOLD)
    resultado_uniao = ft.Text("")
    resultado_nenhum = ft.Text("")
    
    def gerar_campos(e):
        """Cria dinamicamente os campos de texto para os conjuntos e suas interseções."""
        try:
            num_conjuntos = int(num_conjuntos_input.value)
            if not 2 <= num_conjuntos <= 6: # Limite prático para não sobrecarregar a UI
                resultado_geral.value = "Erro: Por favor, insira um número de conjuntos entre 2 e 6."
                resultado_uniao.value = ""
                resultado_nenhum.value = ""
                page.update()
                return
        except (ValueError, TypeError):
            resultado_geral.value = "Erro: Número de conjuntos inválido."
            resultado_uniao.value = ""
            resultado_nenhum.value = ""
            page.update()
            return

        # Limpa os campos e resultados anteriores
        coluna_campos.controls.clear()
        campos_input.clear()
        resultado_geral.value = ""
        resultado_uniao.value = ""
        resultado_nenhum.value = ""
        
        # Gera nomes para os conjuntos
        nomes_conjuntos = [chr(65 + i) for i in range(num_conjuntos)] 

        # Gerar campos para conjuntos individuais
        for nome in nomes_conjuntos:
            key = (nome,)
            field = ft.TextField(label=f"Total de elementos no Conjunto {nome}", keyboard_type=ft.KeyboardType.NUMBER, width=450)
            campos_input[key] = field
            coluna_campos.controls.append(field)
            
        # Gerar campos para todas as interseções (de 2 em 2, de 3 em 3, etc.)
        for i in range(2, num_conjuntos + 1):
            for combo in combinations(nomes_conjuntos, i):
                key = tuple(sorted(combo))
                label_intersecao = " ∩ ".join(key)
                field = ft.TextField(label=f"Interseção ({label_intersecao})", keyboard_type=ft.KeyboardType.NUMBER, width=450)
                campos_input[key] = field
                coluna_campos.controls.append(field)
        
        page.update()

    def calcular(e):
        """Calcula a união total e os elementos externos usando o Princípio da Inclusão-Exclusão."""
        try:
            # Pega todos os valores dos campos de texto
            valores = {key: int(field.value) for key, field in campos_input.items()}
            universo_val = int(universo_input.value)
            
            num_conjuntos = int(num_conjuntos_input.value)
            nomes_conjuntos = [chr(65 + i) for i in range(num_conjuntos)]
            
            uniao_total = 0
            
            # Aplica o Princípio da Inclusão-Exclusão
            for i in range(1, num_conjuntos + 1):
                soma_intersecoes_nivel_i = 0
                for combo in combinations(nomes_conjuntos, i):
                    key = tuple(sorted(combo))
                    soma_intersecoes_nivel_i += valores[key]
                
                # Alterna entre soma e subtração
                # Nível 1 (individuais): Soma
                # Nível 2 (pares): Subtrai
                # Nível 3 (trios): Soma
                if (i - 1) % 2 == 0:
                    uniao_total += soma_intersecoes_nivel_i
                else:
                    uniao_total -= soma_intersecoes_nivel_i

            nenhum = universo_val - uniao_total
            
            # Validações Finais
            if uniao_total > universo_val:
                resultado_geral.value = "Erro: A união dos conjuntos é maior que o universo."
                resultado_uniao.value = ""
                resultado_nenhum.value = ""
            elif nenhum < 0: # Checagem de consistência
                resultado_geral.value = "Erro: Os dados inseridos são inconsistentes (resultam em união > universo)."
                resultado_uniao.value = ""
                resultado_nenhum.value = ""
            else:
                resultado_geral.value = "Resultados Calculados:"
                resultado_uniao.value = f"Total de elementos na União (A ∪ B ∪ ...): {uniao_total}"
                resultado_nenhum.value = f"Elementos fora da união: {nenhum}"

        except (ValueError, TypeError):
            resultado_geral.value = "Erro: Preencha TODOS os campos com números válidos."
            resultado_uniao.value = ""
            resultado_nenhum.value = ""
        except KeyError:
            resultado_geral.value = "Erro: Parece que alguns campos não foram gerados. Clique em 'Gerar Campos'."
            resultado_uniao.value = ""
            resultado_nenhum.value = ""

        page.update()


    
    num_conjuntos_input = ft.TextField(label="Quantos conjuntos deseja analisar? (2-6)", value="2", width=350, keyboard_type=ft.KeyboardType.NUMBER)
    botao_gerar = ft.ElevatedButton("Gerar Campos", on_click=gerar_campos)
    
    universo_input = ft.TextField(label="Tamanho do Conjunto Universo (Total)", width=450, keyboard_type=ft.KeyboardType.NUMBER)
    botao_calcular = ft.ElevatedButton("Calcular União", on_click=calcular)

    page.add(
        ft.Text("Calculadora Avançada de Diagrama de Venn", size=24, weight=ft.FontWeight.BOLD),
        ft.Row([num_conjuntos_input, botao_gerar], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        universo_input,
        coluna_campos, # A coluna que será preenchida dinamicamente
        ft.Divider(),
        botao_calcular,
        resultado_geral,
        resultado_uniao,
        resultado_nenhum,
    )
    
    # Gera os campos iniciais para 2 conjuntos ao iniciar a aplicação
    page.on_load = gerar_campos(None)
    page.update()
    
if __name__ == "__main__":
    ft.app(target=main)