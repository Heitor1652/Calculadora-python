import tkinter as tk

# ── Paleta de cores (estilo iOS/Android) ──────────────────────────────────────
BG          = "#1c1c1e"
DISPLAY_BG  = "#1c1c1e"
DISPLAY_FG  = "#ffffff"
BTN_NUM     = "#333335"
BTN_OP      = "#ff9f0a"
BTN_FUNC    = "#636366"
BTN_EQUAL   = "#ff9f0a"
BTN_PRESS   = "#e08800"
TEXT_DARK   = "#000000"
TEXT_LIGHT  = "#ffffff"

class Calculadora(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora")
        self.resizable(False, False)
        self.configure(bg=BG)

        # ── Estado interno ──────────────────────────────────────────────────
        self._expressao   = ""   # expressão completa acumulada
        self._display_val = "0"  # o que aparece no visor principal
        self._ultimo_op   = None
        self._novo_num    = True # próximo dígito começa número novo

        self._build_ui()
        self._bind_teclado()

    # ─────────────────────────────────────────────────────────────────────────
    # Interface
    # ─────────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Visor superior (expressão)
        self._var_expr = tk.StringVar(value="")
        tk.Label(
            self, textvariable=self._var_expr,
            bg=DISPLAY_BG, fg="#888888",
            font=("SF Pro Display", 16), anchor="e",
            padx=18, pady=0
        ).grid(row=0, column=0, columnspan=4, sticky="ew")

        # Visor principal
        self._var_main = tk.StringVar(value="0")
        tk.Label(
            self, textvariable=self._var_main,
            bg=DISPLAY_BG, fg=DISPLAY_FG,
            font=("SF Pro Display", 52, "bold"), anchor="e",
            padx=18, pady=8
        ).grid(row=1, column=0, columnspan=4, sticky="ew")

        # Layout dos botões: (texto, linha, coluna, colspan, tipo)
        botoes = [
            ("AC",  2, 0, 1, "func"),  ("%",   2, 1, 1, "func"),
            ("⌫",   2, 2, 1, "func"),  ("÷",   2, 3, 1, "op"),

            ("7",   3, 0, 1, "num"),   ("8",   3, 1, 1, "num"),
            ("9",   3, 2, 1, "num"),   ("×",   3, 3, 1, "op"),

            ("4",   4, 0, 1, "num"),   ("5",   4, 1, 1, "num"),
            ("6",   4, 2, 1, "num"),   ("−",   4, 3, 1, "op"),

            ("1",   5, 0, 1, "num"),   ("2",   5, 1, 1, "num"),
            ("3",   5, 2, 1, "num"),   ("+",   5, 3, 1, "op"),

            ("+/−", 6, 0, 1, "func"),  ("0",   6, 1, 1, "num"),
            (",",   6, 2, 1, "num"),   ("=",   6, 3, 1, "eq"),
        ]

        for (txt, row, col, span, tipo) in botoes:
            self._make_btn(txt, row, col, span, tipo)

        # Espaçamento uniforme nas colunas
        for c in range(4):
            self.columnconfigure(c, weight=1, minsize=80)

    def _make_btn(self, texto, row, col, span, tipo):
        cores = {
            "num":  (BTN_NUM,  TEXT_LIGHT),
            "op":   (BTN_OP,   TEXT_DARK),
            "func": (BTN_FUNC, TEXT_LIGHT),
            "eq":   (BTN_EQUAL, TEXT_DARK),
        }
        bg, fg = cores[tipo]

        btn = tk.Button(
            self, text=texto,
            bg=bg, fg=fg, activebackground=BTN_PRESS,
            font=("SF Pro Display", 22),
            relief="flat", bd=0, cursor="hand2",
            width=3, height=1,
            command=lambda t=texto: self._clicar(t)
        )
        btn.grid(row=row, column=col, columnspan=span,
                 padx=5, pady=5, sticky="nsew")
        self.rowconfigure(row, weight=1, minsize=72)

    # ─────────────────────────────────────────────────────────────────────────
    # Lógica dos botões
    # ─────────────────────────────────────────────────────────────────────────
    def _clicar(self, val):
        if val.isdigit() or val == "0":
            self._digito(val)
        elif val == ",":
            self._virgula()
        elif val in ("÷", "×", "−", "+"):
            self._operador(val)
        elif val == "=":
            self._igual()
        elif val == "AC":
            self._limpar()
        elif val == "⌫":
            self._backspace()
        elif val == "%":
            self._porcentagem()
        elif val == "+/−":
            self._inverter_sinal()

    def _digito(self, d):
        if self._novo_num:
            self._display_val = d
            self._novo_num = False
        else:
            if self._display_val == "0":
                self._display_val = d
            else:
                self._display_val += d
        self._atualizar()

    def _virgula(self):
        if self._novo_num:
            self._display_val = "0,"
            self._novo_num = False
        elif "," not in self._display_val:
            self._display_val += ","
        self._atualizar()

    def _operador(self, op):
        # Se há operador pendente, calcula antes
        if not self._novo_num and self._expressao:
            self._calcular_parcial()

        self._expressao   = self._formatar_num(self._display_val) + " " + op
        self._ultimo_op   = op
        self._novo_num    = True
        self._atualizar()

    def _igual(self):
        if not self._expressao or self._ultimo_op is None:
            return
        expr_completa = self._expressao + " " + self._formatar_num(self._display_val)
        self._var_expr.set(expr_completa + " =")
        self._calcular_parcial()
        self._expressao  = ""
        self._ultimo_op  = None
        self._novo_num   = True
        self._atualizar()

    def _calcular_parcial(self):
        try:
            # Converte símbolos para Python
            expr = self._expressao + self._display_val.replace(",", ".")
            expr = expr.replace("÷", "/").replace("×", "*").replace("−", "-")
            resultado = eval(expr)   # noqa: S307 – entrada controlada internamente
            # Formata resultado
            if isinstance(resultado, float) and resultado.is_integer():
                resultado = int(resultado)
            self._display_val = str(resultado).replace(".", ",")
        except ZeroDivisionError:
            self._display_val = "Erro"
        except Exception:
            self._display_val = "Erro"

    def _limpar(self):
        self._display_val = "0"
        self._expressao   = ""
        self._ultimo_op   = None
        self._novo_num    = True
        self._atualizar()

    def _backspace(self):
        if self._display_val in ("0", "Erro"):
            return
        self._display_val = self._display_val[:-1] or "0"
        self._novo_num = self._display_val == "0"
        self._atualizar()

    def _porcentagem(self):
        try:
            val = float(self._display_val.replace(",", ".")) / 100
            self._display_val = self._formatar_num(str(val))
        except Exception:
            pass
        self._atualizar()

    def _inverter_sinal(self):
        try:
            val = float(self._display_val.replace(",", ".")) * -1
            self._display_val = self._formatar_num(str(val))
        except Exception:
            pass
        self._atualizar()

    # ─────────────────────────────────────────────────────────────────────────
    # Utilitários
    # ─────────────────────────────────────────────────────────────────────────
    def _formatar_num(self, s: str) -> str:
        """Remove zeros decimais desnecessários."""
        try:
            v = float(s.replace(",", "."))
            if v == int(v):
                return str(int(v))
            return s
        except Exception:
            return s

    def _atualizar(self):
        # Reduz fonte se o número for grande
        n = len(self._display_val)
        tamanho = 52 if n <= 9 else 38 if n <= 13 else 28
        for widget in self.grid_slaves(row=1):
            widget.configure(font=("SF Pro Display", tamanho, "bold"))

        self._var_main.set(self._display_val)
        if not self._expressao:
            self._var_expr.set("")
        else:
            self._var_expr.set(self._expressao)

    def _bind_teclado(self):
        # Usa apenas _teclado_geral para evitar duplo disparo
        self.bind("<Key>", self._teclado_geral)
        self.bind("<BackSpace>", lambda e: self._clicar("⌫"))
        self.bind("<Escape>",    lambda e: self._clicar("AC"))
        self.bind("<Return>",    lambda e: self._clicar("="))
        self.bind("<KP_Enter>",  lambda e: self._clicar("="))

    def _teclado_geral(self, event):
        # Ignora teclas especiais já tratadas acima
        if event.keysym in ("BackSpace", "Escape", "Return", "KP_Enter"):
            return
        c = event.char
        if c.isdigit():
            self._clicar(c)
        elif c in ("+",):
            self._clicar("+")
        elif c == "-":
            self._clicar("−")
        elif c == "*":
            self._clicar("×")
        elif c == "/":
            self._clicar("÷")
        elif c in (".", ","):
            self._clicar(",")


if __name__ == "__main__":
    app = Calculadora()
    app.mainloop()
