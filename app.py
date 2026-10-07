import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from decimal import Decimal, InvalidOperation
import pyodbc


# ============================================================
# CONFIGURAÇÃO DO SQL SERVER
# ============================================================

CONNECTION_STRING = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=SQL-01;"
    "DATABASE=CrossDockingDB;"
    "UID=crossdock_app;"
    "PWD=CrossDock@2026!;"
    "TrustServerCertificate=yes;"
)


def conectar():
    return pyodbc.connect(CONNECTION_STRING)


def gerar_codigo(cursor):
    cursor.execute("SELECT NEXT VALUE FOR dbo.SeqOperacaoForaCD")
    sequencia = cursor.fetchone()[0]
    ano = datetime.now().year
    return f"FCD-{ano}-{sequencia:06d}"


def parse_valor(valor):
    texto = valor.strip().replace("R$", "").replace(" ", "")

    if "," in texto and "." in texto:
        texto = texto.replace(".", "").replace(",", ".")
    else:
        texto = texto.replace(",", ".")

    return Decimal(texto)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Operações Fora de CD")
        self.root.geometry("1380x820")
        self.root.minsize(1180, 700)

        self.id_selecionado = None

        self.criar_estilo()
        self.criar_dashboard()
        self.criar_formulario()
        self.criar_pesquisa()
        self.criar_tabela()

        self.limpar_formulario()
        self.carregar_dados()
        self.atualizar_dashboard()

    def criar_estilo(self):
        style = ttk.Style()
        style.configure("Titulo.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("CardTitulo.TLabel", font=("Segoe UI", 10))
        style.configure("CardValor.TLabel", font=("Segoe UI", 22, "bold"))
        style.configure("Treeview", rowheight=28)

    def criar_dashboard(self):
        topo = ttk.Frame(self.root, padding=12)
        topo.pack(fill="x")

        ttk.Label(
            topo,
            text="Controle de Operações Fora de CD",
            style="Titulo.TLabel"
        ).pack(anchor="w")

        cards = ttk.Frame(topo)
        cards.pack(fill="x", pady=(12, 0))

        self.lbl_total = self.criar_card(cards, "Total de operações", 0)
        self.lbl_transito = self.criar_card(cards, "Em trânsito", 1)
        self.lbl_entregues = self.criar_card(cards, "Entregues", 2)

    def criar_card(self, parent, titulo, coluna):
        frame = ttk.LabelFrame(parent, text=titulo, padding=12)
        frame.grid(row=0, column=coluna, padx=6, sticky="nsew")
        parent.columnconfigure(coluna, weight=1)

        valor = ttk.Label(frame, text="0", style="CardValor.TLabel")
        valor.pack()
        return valor

    def criar_formulario(self):
        area = ttk.LabelFrame(self.root, text="Cadastro / edição", padding=12)
        area.pack(fill="x", padx=12, pady=6)

        self.var_nota = tk.StringVar()
        self.var_valor = tk.StringVar()
        self.var_cliente = tk.StringVar()
        self.var_origem = tk.StringVar()
        self.var_destino = tk.StringVar()
        self.var_tipo = tk.StringVar()
        self.var_data_recebimento = tk.StringVar()
        self.var_status = tk.StringVar()
        self.var_placa = tk.StringVar()
        self.var_motorista = tk.StringVar()
        self.var_data_entrega = tk.StringVar()

        campos = [
            ("Número da nota", self.var_nota, 0, 0),
            ("Valor da nota", self.var_valor, 0, 2),
            ("Cliente", self.var_cliente, 0, 4),
            ("Origem", self.var_origem, 2, 0),
            ("Destino", self.var_destino, 2, 2),
            ("Placa", self.var_placa, 2, 4),
            ("Motorista", self.var_motorista, 4, 0),
            ("Data recebimento", self.var_data_recebimento, 4, 2),
            ("Data entrega", self.var_data_entrega, 4, 4),
        ]

        for label, var, linha, coluna in campos:
            ttk.Label(area, text=label).grid(
                row=linha, column=coluna, sticky="w", padx=5, pady=(3, 0)
            )
            ttk.Entry(area, textvariable=var, width=28).grid(
                row=linha + 1, column=coluna, sticky="ew", padx=5, pady=(0, 8)
            )

        ttk.Label(area, text="Tipo de operação").grid(
            row=6, column=0, sticky="w", padx=5
        )
        self.cmb_tipo = ttk.Combobox(
            area,
            textvariable=self.var_tipo,
            values=[
                "Operação fora de CD",
                "Coleta",
                "Transferência",
                "Entrega direta",
                "Outro"
            ],
            state="readonly",
            width=25
        )
        self.cmb_tipo.grid(row=7, column=0, sticky="ew", padx=5, pady=(0, 8))

        ttk.Label(area, text="Status").grid(
            row=6, column=2, sticky="w", padx=5
        )
        self.cmb_status = ttk.Combobox(
            area,
            textvariable=self.var_status,
            values=["Em trânsito", "Entregue"],
            state="readonly",
            width=25
        )
        self.cmb_status.grid(row=7, column=2, sticky="ew", padx=5, pady=(0, 8))
        self.cmb_status.bind("<<ComboboxSelected>>", self.status_alterado)

        botoes = ttk.Frame(area)
        botoes.grid(row=7, column=4, sticky="e", padx=5)

        ttk.Button(botoes, text="Novo", command=self.limpar_formulario).pack(side="left", padx=4)
        ttk.Button(botoes, text="Salvar", command=self.salvar).pack(side="left", padx=4)
        ttk.Button(
            botoes,
            text="Marcar como entregue",
            command=self.marcar_entregue
        ).pack(side="left", padx=4)

        for col in range(6):
            area.columnconfigure(col, weight=1)

    def criar_pesquisa(self):
        area = ttk.LabelFrame(self.root, text="Pesquisa / filtros", padding=10)
        area.pack(fill="x", padx=12, pady=6)

        self.var_pesquisa = tk.StringVar()
        self.var_filtro_status = tk.StringVar(value="Todos")

        ttk.Label(area, text="NF, ID ou Placa:").pack(side="left")

        campo_pesquisa = ttk.Entry(area, textvariable=self.var_pesquisa, width=35)
        campo_pesquisa.pack(side="left", padx=8)
        campo_pesquisa.bind("<Return>", lambda event: self.pesquisar())

        ttk.Label(area, text="Status:").pack(side="left", padx=(15, 5))

        combo_status = ttk.Combobox(
            area,
            textvariable=self.var_filtro_status,
            values=["Todos", "Em trânsito", "Entregue"],
            state="readonly",
            width=15
        )
        combo_status.pack(side="left")
        combo_status.bind("<<ComboboxSelected>>", lambda event: self.pesquisar())

        ttk.Button(area, text="Pesquisar", command=self.pesquisar).pack(side="left", padx=8)
        ttk.Button(area, text="Limpar filtros", command=self.limpar_pesquisa).pack(side="left")

    def criar_tabela(self):
        frame = ttk.Frame(self.root, padding=(12, 6, 12, 12))
        frame.pack(fill="both", expand=True)

        colunas = (
            "Codigo", "Nota", "Valor", "Cliente", "Origem", "Destino",
            "Tipo", "Recebimento", "Status", "Entrega", "Placa", "Motorista"
        )

        self.tabela = ttk.Treeview(
            frame,
            columns=colunas,
            show="headings",
            selectmode="browse"
        )

        larguras = {
            "Codigo": 145,
            "Nota": 100,
            "Valor": 100,
            "Cliente": 160,
            "Origem": 110,
            "Destino": 110,
            "Tipo": 130,
            "Recebimento": 105,
            "Status": 90,
            "Entrega": 145,
            "Placa": 90,
            "Motorista": 150,
        }

        for coluna in colunas:
            self.tabela.heading(coluna, text=coluna)
            self.tabela.column(coluna, width=larguras[coluna], anchor="center")

        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=self.tabela.yview)
        scroll_x = ttk.Scrollbar(frame, orient="horizontal", command=self.tabela.xview)

        self.tabela.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        self.tabela.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.tabela.bind("<<TreeviewSelect>>", self.selecionar_registro)

    def status_alterado(self, event=None):
        if self.var_status.get() == "Entregue" and not self.var_data_entrega.get():
            self.var_data_entrega.set(datetime.now().strftime("%d/%m/%Y %H:%M"))

    def validar(self):
        obrigatorios = [
            ("Número da nota", self.var_nota.get()),
            ("Valor da nota", self.var_valor.get()),
            ("Cliente", self.var_cliente.get()),
            ("Origem", self.var_origem.get()),
            ("Destino", self.var_destino.get()),
            ("Tipo de operação", self.var_tipo.get()),
            ("Data de recebimento", self.var_data_recebimento.get()),
            ("Status", self.var_status.get()),
        ]

        faltando = [nome for nome, valor in obrigatorios if not valor.strip()]
        if faltando:
            messagebox.showwarning(
                "Campos obrigatórios",
                "Preencha: " + ", ".join(faltando)
            )
            return False

        try:
            parse_valor(self.var_valor.get())
        except InvalidOperation:
            messagebox.showerror("Valor inválido", "Informe um valor válido.")
            return False

        try:
            datetime.strptime(self.var_data_recebimento.get(), "%d/%m/%Y")
        except ValueError:
            messagebox.showerror(
                "Data inválida",
                "Use DD/MM/AAAA na data de recebimento."
            )
            return False

        if self.var_data_entrega.get().strip():
            try:
                datetime.strptime(self.var_data_entrega.get(), "%d/%m/%Y %H:%M")
            except ValueError:
                messagebox.showerror(
                    "Data inválida",
                    "Use DD/MM/AAAA HH:MM na data de entrega."
                )
                return False

        return True

    def salvar(self):
        if not self.validar():
            return

        valor = parse_valor(self.var_valor.get())
        data_recebimento = datetime.strptime(
            self.var_data_recebimento.get(),
            "%d/%m/%Y"
        ).date()

        data_entrega = None
        if self.var_data_entrega.get().strip():
            data_entrega = datetime.strptime(
                self.var_data_entrega.get(),
                "%d/%m/%Y %H:%M"
            )

        try:
            with conectar() as conn:
                cur = conn.cursor()

                if self.id_selecionado is None:
                    codigo = gerar_codigo(cur)

                    cur.execute("""
                        INSERT INTO dbo.OperacoesForaCD (
                            Codigo,
                            NumeroNota,
                            ValorNota,
                            Cliente,
                            Origem,
                            Destino,
                            TipoOperacao,
                            DataRecebimento,
                            StatusOperacao,
                            Placa,
                            Motorista,
                            DataEntrega
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        codigo,
                        self.var_nota.get().strip(),
                        valor,
                        self.var_cliente.get().strip(),
                        self.var_origem.get().strip(),
                        self.var_destino.get().strip(),
                        self.var_tipo.get().strip(),
                        data_recebimento,
                        self.var_status.get().strip(),
                        self.var_placa.get().strip().upper() or None,
                        self.var_motorista.get().strip() or None,
                        data_entrega
                    ))

                    conn.commit()
                    messagebox.showinfo(
                        "Sucesso",
                        f"Operação cadastrada.\n\nID: {codigo}"
                    )

                else:
                    cur.execute("""
                        UPDATE dbo.OperacoesForaCD
                        SET
                            NumeroNota = ?,
                            ValorNota = ?,
                            Cliente = ?,
                            Origem = ?,
                            Destino = ?,
                            TipoOperacao = ?,
                            DataRecebimento = ?,
                            StatusOperacao = ?,
                            Placa = ?,
                            Motorista = ?,
                            DataEntrega = ?,
                            DataAtualizacao = SYSDATETIME()
                        WHERE Id = ?
                    """, (
                        self.var_nota.get().strip(),
                        valor,
                        self.var_cliente.get().strip(),
                        self.var_origem.get().strip(),
                        self.var_destino.get().strip(),
                        self.var_tipo.get().strip(),
                        data_recebimento,
                        self.var_status.get().strip(),
                        self.var_placa.get().strip().upper() or None,
                        self.var_motorista.get().strip() or None,
                        data_entrega,
                        self.id_selecionado
                    ))

                    conn.commit()
                    messagebox.showinfo("Sucesso", "Registro atualizado.")

            self.limpar_formulario()
            self.carregar_dados()
            self.atualizar_dashboard()

        except pyodbc.Error as erro:
            messagebox.showerror("Erro no SQL Server", str(erro))

    def marcar_entregue(self):
        if self.id_selecionado is None:
            messagebox.showwarning(
                "Seleção",
                "Selecione uma operação na tabela."
            )
            return

        agora = datetime.now()

        try:
            with conectar() as conn:
                cur = conn.cursor()
                cur.execute("""
                    UPDATE dbo.OperacoesForaCD
                    SET
                        StatusOperacao = 'Entregue',
                        DataEntrega = ?,
                        DataAtualizacao = SYSDATETIME()
                    WHERE Id = ?
                """, (agora, self.id_selecionado))
                conn.commit()

            messagebox.showinfo(
                "Sucesso",
                "Operação marcada como entregue."
            )
            self.limpar_formulario()
            self.carregar_dados()
            self.atualizar_dashboard()

        except pyodbc.Error as erro:
            messagebox.showerror("Erro no SQL Server", str(erro))

    def buscar_registros(self, termo=None, status="Todos"):
        sql = """
            SELECT
                Id,
                Codigo,
                NumeroNota,
                ValorNota,
                Cliente,
                Origem,
                Destino,
                TipoOperacao,
                DataRecebimento,
                StatusOperacao,
                DataEntrega,
                Placa,
                Motorista
            FROM dbo.OperacoesForaCD
            WHERE 1 = 1
        """

        params = []

        if termo:
            sql += """
                AND (
                    Codigo LIKE ?
                    OR NumeroNota LIKE ?
                    OR Placa LIKE ?
                )
            """
            curinga = f"%{termo}%"
            params.extend([curinga, curinga, curinga])

        if status != "Todos":
            sql += """
                AND StatusOperacao = ?
            """
            params.append(status)

        sql += """
            ORDER BY Id DESC
        """

        with conectar() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            return cur.fetchall()

    def preencher_tabela(self, registros):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for r in registros:
            data_receb = (
                r.DataRecebimento.strftime("%d/%m/%Y")
                if r.DataRecebimento else ""
            )
            data_entrega = (
                r.DataEntrega.strftime("%d/%m/%Y %H:%M")
                if r.DataEntrega else ""
            )
            valor = (
                f"R$ {r.ValorNota:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

            self.tabela.insert(
                "",
                "end",
                iid=str(r.Id),
                values=(
                    r.Codigo,
                    r.NumeroNota,
                    valor,
                    r.Cliente,
                    r.Origem,
                    r.Destino,
                    r.TipoOperacao,
                    data_receb,
                    r.StatusOperacao,
                    data_entrega,
                    r.Placa or "",
                    r.Motorista or ""
                )
            )

    def carregar_dados(self):
        try:
            registros = self.buscar_registros(None, "Todos")
            self.preencher_tabela(registros)
        except pyodbc.Error as erro:
            messagebox.showerror("Erro no SQL Server", str(erro))

    def pesquisar(self):
        termo = self.var_pesquisa.get().strip()
        status = self.var_filtro_status.get()

        try:
            registros = self.buscar_registros(termo, status)
            self.preencher_tabela(registros)
        except pyodbc.Error as erro:
            messagebox.showerror("Erro no SQL Server", str(erro))

    def limpar_pesquisa(self):
        self.var_pesquisa.set("")
        self.var_filtro_status.set("Todos")
        self.carregar_dados()

    def selecionar_registro(self, event=None):
        selecionados = self.tabela.selection()
        if not selecionados:
            return

        registro_id = int(selecionados[0])

        try:
            with conectar() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT
                        Id,
                        NumeroNota,
                        ValorNota,
                        Cliente,
                        Origem,
                        Destino,
                        TipoOperacao,
                        DataRecebimento,
                        StatusOperacao,
                        Placa,
                        Motorista,
                        DataEntrega
                    FROM dbo.OperacoesForaCD
                    WHERE Id = ?
                """, (registro_id,))
                r = cur.fetchone()

            if not r:
                return

            self.id_selecionado = r.Id
            self.var_nota.set(r.NumeroNota)
            self.var_valor.set(str(r.ValorNota).replace(".", ","))
            self.var_cliente.set(r.Cliente)
            self.var_origem.set(r.Origem)
            self.var_destino.set(r.Destino)
            self.var_tipo.set(r.TipoOperacao)
            self.var_data_recebimento.set(r.DataRecebimento.strftime("%d/%m/%Y"))
            self.var_status.set(r.StatusOperacao)
            self.var_placa.set(r.Placa or "")
            self.var_motorista.set(r.Motorista or "")
            self.var_data_entrega.set(
                r.DataEntrega.strftime("%d/%m/%Y %H:%M")
                if r.DataEntrega else ""
            )

        except pyodbc.Error as erro:
            messagebox.showerror("Erro no SQL Server", str(erro))

    def limpar_formulario(self):
        self.id_selecionado = None
        self.var_nota.set("")
        self.var_valor.set("")
        self.var_cliente.set("")
        self.var_origem.set("")
        self.var_destino.set("")
        self.var_tipo.set("Operação fora de CD")
        self.var_data_recebimento.set(datetime.now().strftime("%d/%m/%Y"))
        self.var_status.set("Em trânsito")
        self.var_placa.set("")
        self.var_motorista.set("")
        self.var_data_entrega.set("")

        if hasattr(self, "tabela"):
            for item in self.tabela.selection():
                self.tabela.selection_remove(item)

    def atualizar_dashboard(self):
        try:
            with conectar() as conn:
                cur = conn.cursor()

                cur.execute("SELECT COUNT(*) FROM dbo.OperacoesForaCD")
                total = cur.fetchone()[0]

                cur.execute("""
                    SELECT COUNT(*)
                    FROM dbo.OperacoesForaCD
                    WHERE StatusOperacao = 'Em trânsito'
                """)
                transito = cur.fetchone()[0]

                cur.execute("""
                    SELECT COUNT(*)
                    FROM dbo.OperacoesForaCD
                    WHERE StatusOperacao = 'Entregue'
                """)
                entregues = cur.fetchone()[0]

            self.lbl_total.config(text=str(total))
            self.lbl_transito.config(text=str(transito))
            self.lbl_entregues.config(text=str(entregues))

        except pyodbc.Error as erro:
            messagebox.showerror("Erro no SQL Server", str(erro))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
