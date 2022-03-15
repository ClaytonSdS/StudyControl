def gerar_relatorio_materias():
    data = pickle.load((open("data_timeline.p", "rb")))
    materias = pickle.load((open("data_subjects_topics.p", "rb")))
    todas_materias = list(materias.keys())


    import matplotlib.pyplot as plt
    from fpdf import FPDF

    def grafico_1_dados(materia):
        taxa_acerto = []
        data = pickle.load((open("data_timeline.p", "rb")))
        data_to_plot = {}

        for x in range(len(data)):
            if data[x][2] == 'Exercicios':
                if data[x][3] == str(materia):
                    data_to_plot[changeData(str(data[x][0]))] = float(splitPercent(data[x][9]))
        return data_to_plot
    def grafico_2_dados(materia):
        taxa_acerto = []
        data = pickle.load((open("data_timeline.p", "rb")))
        data_to_plot = {}

        def calcularHoras(string):
            horas = string.split(':')[0]
            minutos = string.split(':')[1]
            return float(round(float(horas) + float(minutos) / 60, 2))

        for x in range(len(data)):
            if data[x][2] == 'Exercicios' or data[x][2] == 'Teoria':
                if data[x][3] == str(materia):
                    if data[x][6][2] == 'Estudado':
                        data_to_plot[changeData(str(data[x][0]))] = calcularHoras(data[x][5][0:5])

        return data_to_plot
    def grafico_3_dados(materia):
        taxa_acerto = []
        data = pickle.load((open("data_timeline.p", "rb")))
        data_to_plot = {}

        for x in range(len(data)):
            if data[x][2] == 'Exercicios':
                if data[x][3] == str(materia):
                    data_to_plot[changeData(str(data[x][0]))] = float(data[x][7]) + float(data[x][8])
        return data_to_plot
    def grafico_4_dados(materia):
        taxa_acerto = []
        data = pickle.load((open("data_timeline.p", "rb")))
        data_to_plot = {}

        for x in range(len(data)):
            if data[x][2] == 'Exercicios':
                if data[x][3] == str(materia):
                    data_to_plot[changeData(str(data[x][0]))] = float(data[x][7])

        return data_to_plot
    def grafico_5_dados(materia):
        taxa_acerto = []
        data = pickle.load((open("data_timeline.p", "rb")))
        data_to_plot = {}

        for x in range(len(data)):
            if data[x][2] == 'Exercicios':
                if data[x][3] == str(materia):
                    data_to_plot[changeData(str(data[x][0]))] = float(data[x][8])

        return data_to_plot


    def plotar_grafico1(materia):
        cor = 'eef2fe'
        cor_escura = '686fa3'

        fig, ax1 = plt.subplots(nrows=1, ncols=1)
        fig = plt.figure(facecolor=f'#{cor}', dpi=200)
        ax1 = fig.add_subplot(1, 1, 1)

        x = list(grafico_1_dados(materia).keys())
        y = list(grafico_1_dados(materia).values())

        plt.rcParams.update({'figure.max_open_warning': 0})
        plt.plot(x,y, color=f'#{cor_escura}', marker='o')
        plt.xticks(rotation=20)
        plt.grid(True, alpha=0.2)

        ax1 = plt.axes()
        ax1.set_facecolor(f'#{cor}')
        ax1.spines['bottom'].set_color('#{}'.format(cor_escura))
        ax1.spines['top'].set_color('#{}'.format(cor_escura))
        ax1.spines['left'].set_color('#{}'.format(cor_escura))
        ax1.spines['right'].set_color('#{}'.format(cor_escura))

        ax1.xaxis.label.set_color(f'#{cor_escura}')
        ax1.yaxis.label.set_color(f'#{cor_escura}')
        ax1.tick_params(axis='x', colors=f'#{cor_escura}')
        ax1.tick_params(axis='y', colors=f'#{cor_escura}')
        ax1.xaxis.set_tick_params(labelsize=10)
        ax1.yaxis.set_tick_params(labelsize=10)

        #plt.close(fig)
        #plt.close('all')
        plt.savefig(f'graphs/grafico1_{str(materia)}.png', facecolor=(1,1,1,0))

    def plotar_grafico2(materia):
        cor = 'eef2fe'
        cor_escura = '686fa3'

        fig2, ax2 = plt.subplots(nrows=1, ncols=1)
        fig2 = plt.figure(facecolor=f'#{cor}', dpi=200)
        ax2 = fig2.add_subplot(1, 1, 1)

        x = list(grafico_2_dados(materia).keys())
        y = list(grafico_2_dados(materia).values())

        plt.rcParams.update({'figure.max_open_warning': 0})
        plt.plot(x,y, color=f'#{cor_escura}', marker='o')
        plt.xticks(rotation=20)
        plt.xlabel('Horas')
        plt.grid(True, alpha=0.2)

        ax2 = plt.axes()
        ax2.set_facecolor(f'#{cor}')
        ax2.spines['bottom'].set_color('#{}'.format(cor_escura))
        ax2.spines['top'].set_color('#{}'.format(cor_escura))
        ax2.spines['left'].set_color('#{}'.format(cor_escura))
        ax2.spines['right'].set_color('#{}'.format(cor_escura))

        ax2.xaxis.label.set_color(f'#{cor_escura}')
        ax2.yaxis.label.set_color(f'#{cor_escura}')
        ax2.tick_params(axis='x', colors=f'#{cor_escura}')
        ax2.tick_params(axis='y', colors=f'#{cor_escura}')
        ax2.xaxis.set_tick_params(labelsize=10)
        ax2.yaxis.set_tick_params(labelsize=10)

        #plt.close(fig2)
        #plt.close('all')
        plt.savefig(f'graphs/grafico2_{str(materia)}.png', facecolor=(1,1,1,0))

    def plotar_grafico3(materia):
        cor = 'eef2fe'
        cor_escura = '686fa3'

        fig3, ax3 = plt.subplots(nrows=1, ncols=1)
        fig3 = plt.figure(facecolor=f'#{cor}', dpi=200)
        ax3 = fig3.add_subplot(1, 1, 1)

        x = list(grafico_3_dados(materia).keys())
        y = list(grafico_3_dados(materia).values())

        plt.rcParams.update({'figure.max_open_warning': 0})
        plt.plot(x,y, color=f'#{cor_escura}', marker='o')
        plt.xticks(rotation=20)
        #plt.xlabel('Horas')
        plt.grid(True, alpha=0.2)

        ax3 = plt.axes()
        ax3.set_facecolor(f'#{cor}')
        ax3.spines['bottom'].set_color('#{}'.format(cor_escura))
        ax3.spines['top'].set_color('#{}'.format(cor_escura))
        ax3.spines['left'].set_color('#{}'.format(cor_escura))
        ax3.spines['right'].set_color('#{}'.format(cor_escura))

        ax3.xaxis.label.set_color(f'#{cor_escura}')
        ax3.yaxis.label.set_color(f'#{cor_escura}')
        ax3.tick_params(axis='x', colors=f'#{cor_escura}')
        ax3.tick_params(axis='y', colors=f'#{cor_escura}')
        ax3.xaxis.set_tick_params(labelsize=10)
        ax3.yaxis.set_tick_params(labelsize=10)

        #plt.close(fig2)
        #plt.close('all')
        plt.savefig(f'graphs/grafico3_{str(materia)}.png', facecolor=(1,1,1,0))

    def plotar_grafico4(materia):
        cor = 'eef2fe'
        cor_escura = '686fa3'

        fig4, ax4 = plt.subplots(nrows=1, ncols=1)
        fig4 = plt.figure(facecolor=f'#{cor}', dpi=200)
        ax4 = fig4.add_subplot(1, 1, 1)

        x = list(grafico_4_dados(materia).keys())
        y = list(grafico_4_dados(materia).values())

        plt.rcParams.update({'figure.max_open_warning': 0})
        plt.bar(x,y, color=f'#{cor_escura}')
        plt.xticks(rotation=20)
        plt.grid(True, alpha=0.2)

        ax4 = plt.axes()
        ax4.set_facecolor(f'#{cor}')
        ax4.spines['bottom'].set_color('#{}'.format(cor_escura))
        ax4.spines['top'].set_color('#{}'.format(cor_escura))
        ax4.spines['left'].set_color('#{}'.format(cor_escura))
        ax4.spines['right'].set_color('#{}'.format(cor_escura))

        ax4.xaxis.label.set_color(f'#{cor_escura}')
        ax4.yaxis.label.set_color(f'#{cor_escura}')
        ax4.tick_params(axis='x', colors=f'#{cor_escura}')
        ax4.tick_params(axis='y', colors=f'#{cor_escura}')
        ax4.xaxis.set_tick_params(labelsize=10)
        ax4.yaxis.set_tick_params(labelsize=10)

        plt.savefig(f'graphs/grafico4_{str(materia)}.png', facecolor=(1,1,1,0))

    def plotar_grafico5(materia):
        cor = 'eef2fe'
        cor_escura = '686fa3'

        fig5, ax5 = plt.subplots(nrows=1, ncols=1)
        fig5 = plt.figure(facecolor=f'#{cor}', dpi=200)
        ax5 = fig5.add_subplot(1, 1, 1)

        x = list(grafico_5_dados(materia).keys())
        y = list(grafico_5_dados(materia).values())

        plt.rcParams.update({'figure.max_open_warning': 0})
        plt.bar(x,y, color=f'#{cor_escura}')
        plt.xticks(rotation=20)
        plt.grid(True, alpha=0.2)

        ax5 = plt.axes()
        ax5.set_facecolor(f'#{cor}')
        ax5.spines['bottom'].set_color('#{}'.format(cor_escura))
        ax5.spines['top'].set_color('#{}'.format(cor_escura))
        ax5.spines['left'].set_color('#{}'.format(cor_escura))
        ax5.spines['right'].set_color('#{}'.format(cor_escura))

        ax5.xaxis.label.set_color(f'#{cor_escura}')
        ax5.yaxis.label.set_color(f'#{cor_escura}')
        ax5.tick_params(axis='x', colors=f'#{cor_escura}')
        ax5.tick_params(axis='y', colors=f'#{cor_escura}')
        ax5.xaxis.set_tick_params(labelsize=10)
        ax5.yaxis.set_tick_params(labelsize=10)

        plt.savefig(f'graphs/grafico5_{str(materia)}.png', facecolor=(1,1,1,0))

    for x in range(len(todas_materias)):
        plotar_grafico1(todas_materias[x])
        plotar_grafico2(todas_materias[x])
        plotar_grafico3(todas_materias[x])
        plotar_grafico4(todas_materias[x])
        plotar_grafico5(todas_materias[x])


    class PDF(FPDF):

        def header(self):
            self.image('graphs/fundo_relatorio.png', x=0, y=0, w=1000, h=1000)
            self.set_font('helvetica', 'B', 15)
            title_w = self.get_string_width('Relatório - Invision Study') + 6
            doc_w = self.w
            self.set_x((doc_w - title_w) / 2)
            self.set_draw_color(230, 235, 251)
            self.set_fill_color(230, 235, 251)
            self.set_text_color(86, 93, 144)
            self.set_line_width(1)
            self.cell(title_w, 10, 'Relatório - Invision Study', border=1, ln=1, align='C', fill=1)
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('helvetica', 'I', 8)
            self.set_text_color(86, 93, 144)
            self.cell(0, 10, f'Página {self.page_no()}', align='C')

        def chapter_title(self, ch_num, ch_title, link):
            self.set_link(link)
            self.set_font('helvetica', 'B', 12)
            self.set_fill_color(230, 235, 251)
            self.set_text_color(86, 93, 144)
            chapter_title = f'{ch_num} - {ch_title}'
            self.cell(0, 10, chapter_title, ln=1, fill=1)
            self.ln()

        def graph_body(self, name, id_number):
            # set font
            self.set_font('helvetica', 'B', 14)
            self.set_draw_color(230, 235, 251)

            # GRAFICO 1
            self.cell(98, 10, 'Taxa de Acerto (%)', border=1, ln=0, align='C', fill=1)
            self.cell(98, 10, 'Horas Estudadas (Horas)', border=1, ln=1, align='C', fill=1)

            # GRAFICO 1
            self.cell(98, 70, '', border=1, ln=0, align='C', fill=1)

            # GRAFICO 2
            self.cell(98, 70, '', border=1, ln=1, align='C', fill=1)

            # TEXTOS
            self.cell(98, 10, 'Questões Realizadas (%)', border=1, ln=0, align='C', fill=1)
            self.cell(98, 10, 'Acertos', border=1, ln=1, align='C', fill=1)

            # GRAFICO 3
            self.cell(98, 100, '', border=1, ln=0, align='C', fill=1)
            # GRAFICO 4
            self.cell(98, 45, '', border=1, ln=2, align='C', fill=1)

            # TEXTOS
            self.cell(98, 24, 'Erros', border=1, ln=2, align='C', fill=1)
            # GRAFICO 5
            self.cell(98, 45, '', border=1, ln=2, align='C', fill=1)

            # GRÁFICO 1
            self.image(f'graphs/grafico1_{str(name)}.png', x=10, y=52, w=98, h=72)

            # GRÁFICO 2
            self.image(f'graphs/grafico2_{str(name)}.png', x=107, y=52, w=98, h=72)

            # GRÁFICO 3
            self.image(f'graphs/grafico3_{str(name)}.png', x=10, y=135, w=98, h=72)

            # GRÁFICO 4
            self.image(f'graphs/grafico4_{str(name)}.png', x=107, y=135, w=98, h=55)

            # GRÁFICO 5
            self.image(f'graphs/grafico5_{str(name)}.png', x=107, y=198, w=98, h=55)
            #plotar_grafico1(self, name, id_number)
            self.image(f'logo_relat.png', x=30, y=220, w=60, h=30)

        def graph_generator(self, ch_num, ch_title, name, link, id_number):
            self.add_page()
            self.chapter_title(ch_num, ch_title, link)
            self.graph_body(name, id_number)


    # CRIANDO UM OBJETO PDF
    pdf = PDF('P', 'mm', 'Letter')

    # COLOCAR AUTOR E TITULO DO PDF
    pdf.set_title('Relatório - Invision Study')
    pdf.set_author('Invision Code')

    # COLOCAR QUEBRA DE LINHA AUTOMATICA
    pdf.set_auto_page_break(auto=True, margin=15)

    # ADICIONAR PÁGINA
    pdf.add_page()

    pdf.set_text_color(86, 93, 144)

    # CRIAR LINKS
    links = {}
    for x in range(len(todas_materias)):
        links[todas_materias[x]] = pdf.add_link()

    # LINKAR OS ITEMS DO SUMÁRIO COM AS RESPECTIVAS PÁGINAS
    for x in range(len(todas_materias)):
        pdf.cell(0, 10, str(x+1)+'-' + todas_materias[x], ln=1, link=links[todas_materias[x]])
        pdf.image(f'logo_relat.png', x=142, y=230, w=60, h=30)
        pdf.image(f'graphs/text_materias.png', x=173, y=0, w=40, h=250)

    # CRIAR PÁGINAS
    for x in range(len(todas_materias)):
        pdf.graph_generator(x+1, todas_materias[x], todas_materias[x], links[todas_materias[x]], x+1)

    try:
        pdf.output('Relatório_InvisionStudy.pdf')
    except PermissionError:
        print('Não Foi Possivel Salvar o Arquivo')
