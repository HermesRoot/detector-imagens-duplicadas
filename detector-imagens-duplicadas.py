import wx
import os
import datetime
from PIL import Image
import imagehash


class DuplicatedImageFinder(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Detector de Imagens Duplicadas', size=(700, 500))
        self.report_folder = ''
        self.duplicates_list = []
        self.hash_threshold = 5  # Limite inicial de sensibilidade
        self.last_report_path = None  # Caminho do último relatório salvo
        panel = wx.Panel(self)

        menubar = wx.MenuBar()

        # Menu "Arquivo" com atalhos
        file_menu = wx.Menu()
        select_report_folder = file_menu.Append(wx.ID_ANY, '&Salvar relatório...\tAlt+S')
        open_folder = file_menu.Append(wx.ID_ANY, 'Abrir &imagens\tAlt+I')
        open_report_folder = file_menu.Append(wx.ID_ANY, 'Abrir &relatórios\tAlt+R')
        open_last_report = file_menu.Append(wx.ID_ANY, 'Último &relatório\tAlt+L')
        clear_log = file_menu.Append(wx.ID_ANY, 'Limpar &log\tAlt+C')
        exit_item = file_menu.Append(wx.ID_EXIT, '&Sair\tCtrl+Q')
        menubar.Append(file_menu, '&Arquivo')

        # Menu "Ferramentas"
        tools_menu = wx.Menu()
        config_sensitivity = tools_menu.Append(wx.ID_ANY, 'Configurar sensibilidade')
        recheck_folder = tools_menu.Append(wx.ID_ANY, 'Verificar pasta novamente')
        menubar.Append(tools_menu, '&Ferramentas')

        # Menu "Ajuda"
        help_menu = wx.Menu()
        usage_item = help_menu.Append(wx.ID_ANY, 'Como Usar')
        about_item = help_menu.Append(wx.ID_ABOUT, 'Sobre')
        menubar.Append(help_menu, '&Ajuda')

        self.SetMenuBar(menubar)

        # Vincular eventos do menu "Arquivo"
        self.Bind(wx.EVT_MENU, self.on_select_report_folder, select_report_folder)
        self.Bind(wx.EVT_MENU, self.on_open_folder, open_folder)
        self.Bind(wx.EVT_MENU, self.on_open_report_folder, open_report_folder)
        self.Bind(wx.EVT_MENU, self.on_open_last_report, open_last_report)
        self.Bind(wx.EVT_MENU, self.on_clear_log, clear_log)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

        # Vincular eventos do menu "Ferramentas"
        self.Bind(wx.EVT_MENU, self.on_config_sensitivity, config_sensitivity)
        self.Bind(wx.EVT_MENU, self.on_recheck_folder, recheck_folder)

        # Vincular eventos do menu "Ajuda"
        self.Bind(wx.EVT_MENU, self.on_about, about_item)
        self.Bind(wx.EVT_MENU, self.on_usage, usage_item)

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.folder_path = wx.TextCtrl(panel, style=wx.TE_READONLY)
        btn_select_folder = wx.Button(panel, label='Selecionar Pasta', size=(150, 30))
        btn_select_folder.Bind(wx.EVT_BUTTON, self.on_select_folder)

        self.chk_delete = wx.CheckBox(panel, label='Excluir automaticamente duplicadas')

        btn_start = wx.Button(panel, label='Iniciar Verificação', size=(180, 30))
        btn_start.Bind(wx.EVT_BUTTON, self.on_start)

        self.log = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

        vbox.Add(self.folder_path, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(btn_select_folder, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        vbox.Add(self.chk_delete, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        vbox.Add(btn_start, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        vbox.Add(self.log, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Pronto')

        self.Show()

    def on_select_folder(self, event):
        with wx.DirDialog(self, "Escolha a pasta com imagens") as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                self.folder_path.SetValue(path)
                if not self.report_folder:
                    self.report_folder = path

    def on_select_report_folder(self, event):
        with wx.DirDialog(self, "Escolha a pasta para salvar o relatório") as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.report_folder = dlg.GetPath()
                self.log.AppendText(f"Pasta de relatório definida: {self.report_folder}\n")

    def on_open_folder(self, event):
        folder = self.folder_path.GetValue()
        if folder and os.path.exists(folder):
            os.startfile(folder)  # Para Windows; use `open` no macOS ou `xdg-open` no Linux
        else:
            wx.MessageBox("Selecione uma pasta válida primeiro.", "Aviso", wx.OK | wx.ICON_WARNING)

    def on_open_report_folder(self, event):
        if self.report_folder and os.path.exists(self.report_folder):
            os.startfile(self.report_folder)
        else:
            wx.MessageBox("Nenhuma pasta de relatório definida.", "Aviso", wx.OK | wx.ICON_WARNING)

    def on_open_last_report(self, event):
        if self.last_report_path and os.path.exists(self.last_report_path):
            os.startfile(self.last_report_path)
        else:
            wx.MessageBox("Nenhum relatório salvo ainda.", "Aviso", wx.OK | wx.ICON_WARNING)

    def on_clear_log(self, event):
        self.log.Clear()
        self.log.AppendText("Log limpo.\n")

    def on_exit(self, event):
        self.Close()

    def on_config_sensitivity(self, event):
        dlg = wx.NumberEntryDialog(self, "Defina o limite de sensibilidade (0-20):", "Sensibilidade", "Configurar", self.hash_threshold, 0, 20)
        if dlg.ShowModal() == wx.ID_OK:
            self.hash_threshold = dlg.GetValue()
            self.log.AppendText(f"Sensibilidade definida para: {self.hash_threshold}\n")
        dlg.Destroy()

    def on_recheck_folder(self, event):
        self.on_start(event)

    def on_about(self, event):
        wx.MessageBox('Detector de Imagens Duplicadas\npor HermesRoot\nLicença MIT\nVersão 0.1.0', 'Sobre', wx.OK | wx.ICON_INFORMATION)

    def on_usage(self, event):
        wx.MessageBox('1. Selecione a pasta com imagens.\n2. Configure se deseja excluir duplicadas.\n3. Defina a pasta do relatório no menu Arquivo (opcional).\n4. Clique em Iniciar Verificação.\n5. O relatório será salvo na pasta definida.', 'Como Usar', wx.OK | wx.ICON_INFORMATION)

    def on_start(self, event):
        folder = self.folder_path.GetValue()
        if not folder:
            wx.MessageBox('Selecione a pasta de imagens.', 'Aviso', wx.OK | wx.ICON_WARNING)
            return
        self.log.Clear()  # Limpa o log sem adicionar "Log limpo."
        self.log.AppendText(f"Iniciando verificação na pasta: {folder}\n")
        self.find_duplicates(folder, self.report_folder)
        if self.duplicates_list:
            self.show_duplicates_list()
        self.save_report()

    def find_duplicates(self, folder, report_folder):
        self.duplicates_list.clear()
        hashes = {}
        total_imagens = sum(1 for root, _, files in os.walk(folder) for filename in files if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')))
        contador = 0

        for root, _, files in os.walk(folder):
            for filename in files:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    path = os.path.join(root, filename)
                    try:
                        img = Image.open(path)
                        hash_img = imagehash.phash(img)
                        for h, orig_path in hashes.items():
                            if hash_img - h <= self.hash_threshold:  # Usa o limite configurável
                                self.duplicates_list.append((path, orig_path))
                                if self.chk_delete.IsChecked():
                                    os.remove(path)
                                    self.log.AppendText(f"{path} excluída (duplicada de {orig_path})\n")
                                else:
                                    self.log.AppendText(f"{path} é duplicada de {orig_path}\n")
                                break
                        else:
                            hashes[hash_img] = path
                    except Exception as e:
                        self.log.AppendText(f"Erro com {path}: {e}\n")
                    contador += 1
                    progresso = (contador / total_imagens) * 100
                    self.statusbar.SetStatusText(f'Progresso: {contador}/{total_imagens} ({progresso:.2f}%)')

        self.log.AppendText("Verificação concluída.\n")
        self.statusbar.SetStatusText('Verificação concluída')

    def save_report(self):
        if not self.report_folder:
            self.report_folder = self.folder_path.GetValue()
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.report_folder, f"relatorio_duplicatas_{timestamp}.txt")
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(f"Relatório de Imagens Duplicadas - {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Pasta analisada: {self.folder_path.GetValue()}\n")
                f.write(f"Exclusão automática: {'Sim' if self.chk_delete.IsChecked() else 'Não'}\n\n")
                
                if not self.duplicates_list:
                    f.write("Nenhuma duplicata encontrada.\n")
                else:
                    f.write(f"Total de duplicatas encontradas: {len(self.duplicates_list)}\n\n")
                    for dup, orig in self.duplicates_list:
                        f.write(f"Duplicata: {dup}\nOriginal: {orig}\n")
                        if self.chk_delete.IsChecked():
                            f.write("Status: Duplicata excluída\n")
                        f.write("\n")
            
            self.last_report_path = report_path  # Armazena o caminho do último relatório
            self.log.AppendText(f"Relatório salvo em: {report_path}\n")
        except Exception as e:
            self.log.AppendText(f"Erro ao salvar relatório: {e}\n")
            wx.MessageBox(f"Erro ao salvar o relatório: {e}", 'Erro', wx.OK | wx.ICON_ERROR)

    def show_duplicates_list(self):
        dlg = wx.Dialog(self, title="Duplicatas Encontradas", size=(500, 400))
        vbox = wx.BoxSizer(wx.VERTICAL)
        listbox = wx.ListBox(dlg, choices=[f"{os.path.basename(dup)} <-> {os.path.basename(orig)}" for dup, orig in self.duplicates_list])
        btn_view = wx.Button(dlg, label="Visualizar")

        def on_view(event):
            selection = listbox.GetSelection()
            if selection != wx.NOT_FOUND:
                dup, orig = self.duplicates_list[selection]
                os.startfile(dup) if os.path.exists(dup) else None
                os.startfile(orig) if os.path.exists(orig) else None

        btn_view.Bind(wx.EVT_BUTTON, on_view)

        vbox.Add(listbox, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(btn_view, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        dlg.SetSizer(vbox)
        dlg.ShowModal()
        dlg.Destroy()


if __name__ == '__main__':
    app = wx.App(False)
    frame = DuplicatedImageFinder()
    app.MainLoop()