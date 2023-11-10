import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.simpledialog import askinteger
from DAO.ProdutoDAO import ProdutoDAO
import psycopg2
from Data.config import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class ProdutoView: 
    def __init__(self, tela):
        root = tk.Tk()
        self.dao = ProdutoDAO(db_url)
        self.tela = tela
        self.tela.title("Sistemas Tabajara")
        self.tela.geometry("500x500")

        # Formulário
        self.nome_label = tk.Label(tela, text="Nome do Produto")
        self.nome_label.grid(row=2, column=0, padx=10)
        self.nome_entry = tk.Entry(tela)
        self.nome_entry.grid(row=3, column=0, padx=10, pady=10)

        self.preco_label = tk.Label(tela, text="Preço")
        self.preco_label.grid(row=2, column=1, padx=10)
        self.preco_entry = tk.Entry(tela)
        self.preco_entry.grid(row=3, column=1, padx=10, pady=10)

        self.sku_label = tk.Label(tela, text="SKU")
        self.sku_label.grid(row=2, column=2, padx=10)
        self.sku_entry = tk.Entry(tela)
        self.sku_entry.grid(row=3, column=2, padx=10, pady=10)

        # Botão de envio
        self.botao_cadastro = tk.Button(tela, text="Cadastrar Produto", command=self.cadastrar_produto_view)
        self.botao_cadastro.grid(row=6, column=0, padx=5, pady=10)

        self.botao_limpar = tk.Button(tela, text="Limpar Campos", command=self.limpar_campos_view)
        self.botao_limpar.grid(row=6, column=1, padx=5, pady=10)

        self.botao_atualizar = tk.Button(tela, text="Atualizar Produto", command=self.atualizar_produto_view)
        self.botao_atualizar.grid(row=6, column=2, padx=5, pady=10)

        self.botao_deletar = tk.Button(tela, text="Deletar Produto", command=self.deletar_produto_view)
        self.botao_deletar.grid(row=6, column=3, padx=5, pady=10)
        
        
        #Lista de produto n view
        self.lista_produtos_treeview = ttk.Treeview(tela, columns=("ID", "Nome", "Preço", "Preço com Adicional", "SKU"), show="headings")
        self.lista_produtos_treeview.heading("ID", text="ID")
        self.lista_produtos_treeview.heading("Nome", text="Nome")
        self.lista_produtos_treeview.heading("Preço", text="Preço")
        self.lista_produtos_treeview.heading("Preço com Adicional", text="Preço com Adicional")
        self.lista_produtos_treeview.heading("SKU", text="SKU")
        self.lista_produtos_treeview.grid(row=5, column=0, columnspan=4)

        #Centralizado texto
        for col in ("ID", "Nome", "Preço", "Preço com Adicional", "SKU"):
            self.lista_produtos_treeview.column(col, anchor="center")

        self.atualizar_lista_produtos_view()


    def atualizar_lista_produtos_view(self):
        produtos = self.dao.listar_produtos()
        for item in self.lista_produtos_treeview.get_children():
            self.lista_produtos_treeview.delete(item)
        for produto in produtos:
            self.lista_produtos_treeview.insert("", "end", values=(produto.id, produto.nome, produto.preco, produto.preco_add, produto.sku))

    def limpar_campos_view(self):
        self.nome_entry.delete(0, "end")
        self.preco_entry.delete(0, "end")
        self.sku_entry.delete(0, "end") 
    
    def cadastrar_produto_view(self):
        nome = self.nome_entry.get()
        preco_str = self.preco_entry.get()
        sku = self.sku_entry.get() 

        if not nome or not preco_str or not sku:
            messagebox.showerror("Erro", "Nome, preço e SKU são campos obrigatórios.")
            return
        
        try:
            preco = float(preco_str)
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser um número válido.")
            return
        
        preco_add = preco * 1.1

        produto = self.dao.criar_produto(nome, preco, preco_add, sku)

        if produto:
            self.atualizar_lista_produtos_view()
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar o produto.")

    def deletar_produto_view(self):
        produto_id = askinteger("Excluir Produto", "Digite o ID do produto a ser excluído:")

        exist = self.dao.buscar_produto_por_id(produto_id)
        if (exist is not None):
            self.dao.deletar_produto(produto_id)
            self.atualizar_lista_produtos_view()
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
        else:
            messagebox.showerror("Erro", "Produto não encontrado ou falha ao excluir o produto!")

    def atualizar_produto_view(self):
        produto_id = askinteger("Atualizar Produto", "Digite o ID do produto a ser atualizado:")

        if (produto_id is not None):
            produto = self.dao.buscar_produto_por_id(produto_id)
            if produto is not None:

                janela_atualizacao = tk.Toplevel(self.tela)
                janela_atualizacao.title("Atualizar Produto")

                nome_label = tk.Label(janela_atualizacao, text="Nome do Produto")
                nome_label.grid(row=0, column=1, padx=5)
                nome_entry = tk.Entry(janela_atualizacao)
                nome_entry.insert(0, produto.nome)
                nome_entry.grid(row=1, column=1, padx=5, pady=10)

                preco_label = tk.Label(janela_atualizacao, text="Preço")
                preco_label.grid(row=2, column=1, padx=5)
                preco_entry = tk.Entry(janela_atualizacao)
                preco_entry.insert(0, produto.preco)
                preco_entry.grid(row=3, column=1, padx=5, pady=10)

                sku_label = tk.Label(janela_atualizacao, text="SKU")
                sku_label.grid(row=4, column=1, padx=5)
                sku_entry = tk.Entry(janela_atualizacao)
                sku_entry.insert(0, produto.sku)
                sku_entry.grid(row=5, column=1, padx=5, pady=10)

                def confirmar_atualizacao():
                    novo_nome = nome_entry.get()
                    novo_preco = float(preco_entry.get())
                    novo_sku = sku_entry.get()

                    if not novo_nome or not novo_preco or not novo_sku:
                        messagebox.showerror("Erro", "Nome, preço e SKU são campos obrigatórios.")
                        return

                    self.dao.atualizar_produto(produto_id, novo_nome, novo_preco, novo_sku)
                    self.atualizar_lista_produtos_view()
                    janela_atualizacao.destroy()

                    messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")

                botao_confirmar = tk.Button(janela_atualizacao, text="Confirmar Atualização", command=confirmar_atualizacao)
                botao_confirmar.grid(row=6, column=1, padx=5, pady=10)


                botao_cancelar = tk.Button(janela_atualizacao, text="Cancelar", command=janela_atualizacao.destroy)
                botao_cancelar.grid(row=7, column=1, padx=5, pady=10)

            else:
                messagebox.showerror("Erro", "Produto não encontrado.")



if __name__ == "__main__":
    tela = tk.Tk()
    app = ProdutoView(tela)
    tela.mainloop()