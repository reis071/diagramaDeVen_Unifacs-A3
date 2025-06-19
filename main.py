import flet as ft
from itertools import combinations
import time 
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

from matplotlib_venn import venn2, venn3


def main(page: ft.Page):
    
    page.title = "Calculadora de Venn com Diagramas"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 650
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.DARK

    
    campos_input = {}
    coluna_campos = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, spacing=10, height=350, width=500)
    resultado_geral = ft.Text("", size=16, weight=ft.FontWeight.BOLD)
    resultado_uniao = ft.Text("")
    resultado_nenhum = ft.Text("")
    
    # Controle para exibir a imagem do diagrama
    imagem_diagrama = ft.Image(visible=False) 

    def gerar_campos(e):
        """Cria dinamicamente os campos de texto."""
        try:
            num_conjuntos = int(num_conjuntos_input.value)
            if not 2 <= num_conjuntos <= 6:
                resultado_geral.value = "Erro: Insira um número de conjuntos entre 2 e 6."
                page.update()
                return
        except (ValueError, TypeError):
            resultado_geral.value = "Erro: Número de conjuntos inválido."
            page.update()
            return

        # Limpa tudo
        coluna_campos.controls.clear()
        campos_input.clear()
        resultado_geral.value = ""
        resultado_uniao.value = ""
        resultado_nenhum.value = ""
        imagem_diagrama.visible = False # Esconde a imagem antiga
        
        nomes_conjuntos = [chr(65 + i) for i in range(num_conjuntos)] 

        for nome in nomes_conjuntos:
            key = (nome,)
            field = ft.TextField(label=f"Total no Conjunto {nome}", keyboard_type=ft.KeyboardType.NUMBER, width=450)
            campos_input[key] = field
            coluna_campos.controls.append(field)
            
        for i in range(2, num_conjuntos + 1):
            for combo in combinations(nomes_conjuntos, i):
                key = tuple(sorted(combo))
                label_intersecao = " ∩ ".join(key)
                field = ft.TextField(label=f"Interseção ({label_intersecao})", keyboard_type=ft.KeyboardType.NUMBER, width=450)
                campos_input[key] = field
                coluna_campos.controls.append(field)
        
        page.update()

    def calcular_regioes_exclusivas(valores, nomes_conjuntos):
        """Calcula o valor de cada região 'pura' do diagrama."""
        num_conjuntos = len(nomes_conjuntos)
        regioes = {}

        if num_conjuntos == 2:
            A, B = nomes_conjuntos[0], nomes_conjuntos[1]
            total_A = valores.get((A,), 0)
            total_B = valores.get((B,), 0)
            inter_AB = valores.get((A, B), 0)
            
            regioes['A_only'] = total_A - inter_AB
            regioes['B_only'] = total_B - inter_AB
            regioes['AB'] = inter_AB

        elif num_conjuntos == 3:
            A, B, C = nomes_conjuntos[0], nomes_conjuntos[1], nomes_conjuntos[2]
            total_A = valores.get((A,), 0)
            total_B = valores.get((B,), 0)
            total_C = valores.get((C,), 0)
            inter_AB = valores.get((A, B), 0)
            inter_AC = valores.get((A, C), 0)
            inter_BC = valores.get((B, C), 0)
            inter_ABC = valores.get((A, B, C), 0)
            
            regioes['ABC'] = inter_ABC
            regioes['AB_only'] = inter_AB - inter_ABC
            regioes['AC_only'] = inter_AC - inter_ABC
            regioes['BC_only'] = inter_BC - inter_ABC
            regioes['A_only'] = total_A - (regioes['AB_only'] + regioes['AC_only'] + regioes['ABC'])
            regioes['B_only'] = total_B - (regioes['AB_only'] + regioes['BC_only'] + regioes['ABC'])
            regioes['C_only'] = total_C - (regioes['AC_only'] + regioes['BC_only'] + regioes['ABC'])
        
        # Validação: nenhuma região pode ser negativa
        if any(v < 0 for v in regioes.values()):
            raise ValueError("Dados inconsistentes. Uma ou mais regiões resultaram em um valor negativo.")

        return regioes

    def gerar_e_exibir_diagrama(regioes, nomes_conjuntos):
        """Usa matplotlib-venn para criar e salvar o diagrama."""
        num_conjuntos = len(nomes_conjuntos)
        plt.figure(figsize=(8, 8)) # Cria uma nova figura para o plot

        if num_conjuntos == 2:
            # A ordem para venn2 é (Apenas A, Apenas B, A e B)
            subset_vals = (regioes['A_only'], regioes['B_only'], regioes['AB'])
            venn2(subsets=subset_vals, set_labels=nomes_conjuntos)
        
        elif num_conjuntos == 3:
                        
            subset_vals = (
                regioes['A_only'], regioes['B_only'], regioes['AB_only'], regioes['C_only'],
                regioes['AC_only'], regioes['BC_only'], regioes['ABC']
            )
            venn3(subsets=subset_vals, set_labels=nomes_conjuntos)
        else:
            return 


        caminho_imagem = "diagrama_venn.png"
        plt.savefig(caminho_imagem, bbox_inches='tight')
        plt.close() # Fecha a figura para liberar memória
        
    
        imagem_diagrama.src = f"{caminho_imagem}?{time.time()}"
        imagem_diagrama.visible = True

    def calcular(e):
        """Calcula a união, elementos externos e gera o diagrama."""
        
        imagem_diagrama.visible = False
        page.update()
        
        try:
            valores = {key: int(field.value) for key, field in campos_input.items() if field.value}
            universo_val = int(universo_input.value)
            num_conjuntos = int(num_conjuntos_input.value)
            nomes_conjuntos = [chr(65 + i) for i in range(num_conjuntos)]
            
            # --- Cálculo da União (Princípio da Inclusão-Exclusão) ---
            uniao_total = 0
            for i in range(1, num_conjuntos + 1):
                soma_intersecoes_nivel_i = 0
                for combo in combinations(nomes_conjuntos, i):
                    key = tuple(sorted(combo))
                    soma_intersecoes_nivel_i += valores.get(key, 0)
                
                if (i - 1) % 2 == 0:
                    uniao_total += soma_intersecoes_nivel_i
                else:
                    uniao_total -= soma_intersecoes_nivel_i

            nenhum = universo_val - uniao_total
            
            if uniao_total > universo_val:
                raise ValueError("A união dos conjuntos é maior que o universo.")
            
            # --- Geração do Diagrama ---
            if num_conjuntos in [2, 3]:
                regioes_exclusivas = calcular_regioes_exclusivas(valores, nomes_conjuntos)
                gerar_e_exibir_diagrama(regioes_exclusivas, nomes_conjuntos)
                resultado_geral.value = "Resultados e Diagrama:"
            else:
                resultado_geral.value = "Resultados (Diagrama não suportado para > 3 conjuntos):"

            resultado_uniao.value = f"Total de elementos na União (A ∪ B ∪ ...): {uniao_total}"
            resultado_nenhum.value = f"Elementos fora da união (Universo - União): {nenhum}"

        except ValueError as ex:
            resultado_geral.value = f"Erro: {ex}"
            resultado_uniao.value = ""
            resultado_nenhum.value = ""
        except (TypeError):
            resultado_geral.value = "Erro: Preencha TODOS os campos com números válidos."
            resultado_uniao.value = ""
            resultado_nenhum.value = ""
        except KeyError:
            resultado_geral.value = "Erro: Campos não gerados. Clique em 'Gerar Campos'."
            resultado_uniao.value = ""
            resultado_nenhum.value = ""

        page.update()

    
    num_conjuntos_input = ft.TextField(label="Quantos conjuntos? (2-6)", value="2", width=350, on_submit=gerar_campos)
    botao_gerar = ft.ElevatedButton("Gerar Campos", on_click=gerar_campos)
    universo_input = ft.TextField(label="Tamanho do Conjunto Universo (Total)", width=450, keyboard_type=ft.KeyboardType.NUMBER)
    botao_calcular = ft.ElevatedButton("Calcular e Gerar Diagrama", on_click=calcular, icon=ft.Icons.INSIGHTS)

    page.add(
        ft.Column(
            [
                ft.Text("Calculadora Avançada de Diagrama de Venn", size=24, weight=ft.FontWeight.BOLD),
                ft.Row([num_conjuntos_input, botao_gerar], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(),
                universo_input,
                coluna_campos,
                ft.Divider(),
                botao_calcular,
                resultado_geral,
                resultado_uniao,
                resultado_nenhum,
                ft.Container(content=imagem_diagrama, padding=10) # Container para a imagem
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
    )
    
    # Gera os campos iniciais para 2 conjuntos ao iniciar
    gerar_campos(None)
    page.update()
    
if __name__ == "__main__":
    ft.app(target=main)