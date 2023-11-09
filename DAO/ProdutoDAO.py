from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Domain.Produto import Produto
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

class ProdutoInstacia(Base): 
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True) 
    nome = Column(String)
    preco = Column(Float)
    preco_add = Column(Float)
    sku = Column(String)

class ProdutoDAO: 
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def criar_produto(self, nome, preco, preco_add, sku):
        try:
            produto_instancia = ProdutoInstacia(nome=nome, preco=preco, preco_add=preco_add, sku=sku)
            self.session.add(produto_instancia)
            self.session.commit()
            self.session.close()
            return produto_instancia
        except SQLAlchemyError as e:
            print(f"Erro ao criar o produto: {str(e)}")
            self.session.rollback()
        finally:
            self.session.close()

    def buscar_produto_por_id(self, produto_id):
        try:
            return self.session.query(ProdutoInstacia).filter(ProdutoInstacia.id == produto_id).first()
        except SQLAlchemyError as e:
            print(f"Erro ao buscar o produto: {str(e)}")
        finally:
            self.session.close()


    def atualizar_produto(self, produto_id, nome, preco, sku):
        try:
            produto = self.buscar_produto_por_id(produto_id)
            if (produto):
                produto.nome = nome
                produto.preco = preco
                produto.preco_add = preco * 1.1
                produto.sku = sku
                self.session.commit()
                self.session.close()
            return produto
        except SQLAlchemyError as e:
            print(f"Erro ao atualizar o produto: {str(e)}")
            self.session.rollback()
        finally:
            self.session.close()

    def deletar_produto(self, produto_id):
        try:
            produto = self.buscar_produto_por_id(produto_id)
            if (produto):
                self.session.delete(produto)
                self.session.commit()
        except SQLAlchemyError as e:
            print(f"Erro ao deletar o produto: {str(e)}")
            self.session.rollback()
        finally:
            self.session.close()

    def listar_produtos(self):
        try:
            return self.session.query(ProdutoInstacia).all()
        except SQLAlchemyError as e:
            print(f"Erro ao listar os produtos: {str(e)}")
        finally:
            self.session.close()