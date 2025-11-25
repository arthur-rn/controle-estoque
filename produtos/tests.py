from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from .models import Produto

# Create your tests here.
class HomeViewTest(SimpleTestCase):
    def test_home_get(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")


class ProdutoModelTest(TestCase):
    def teste_criar_produto(self):
        produto = Produto.objects.create(nome = 'Mouse', descricao = 'Mouse sem fio', preco = 80, quantidade = 10)

        self.assertEqual(produto.nome, 'Mouse')
        self.assertEqual(produto.preco, 80)
        self.assertEqual(produto.quantidade, 10)

class ProdutoViewTest(TestCase):
    def setUp(self):
        Produto.objects.create(nome = 'Mousepad', descricao = 'Mousepad preto 90x40', preco = 30, quantidade = 5)

    def teste_listar_produtos_view(self):
        response = self.client.get(reverse('listar_produtos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mousepad')

    def teste_criar_produto_view_get(self):
        response = self.client.get(reverse('criar_produto'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Criar produto')

    def teste_criar_produto_view_post(self):
        response = self.client.post(reverse('criar_produto'), {
            'nome': 'Cadeira',
            'descricao': 'Cadeira gamer reclinável',
            'preco': 600,
            'quantidade': 2
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Produto.objects.filter(nome='Cadeira'))

class ProdutoEdicaoExclusaoTest(TestCase):
    def setUp(self):
        self.produto = Produto.objects.create(nome = 'Monitor', descricao = 'Monitor IPS 144hz', preco = 700, quantidade = 5)
    
    def teste_editar_produto_view_get(self):
        url = reverse('editar_produto', args=[self.produto.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Editar')
        self.assertContains(response, 'Monitor')

    def teste_editar_produto_view_post(self):
        url = reverse("editar_produto", args=[self.produto.id])

        response = self.client.post(url, {
            "nome": "Monitor LG",
            "descricao": "Atualizado",
            "preco": 1299,
            "quantidade": 5,
        })

        self.assertEqual(response.status_code, 302)

        self.produto.refresh_from_db()

        self.assertEqual(self.produto.nome, "Monitor LG")
        self.assertEqual(self.produto.quantidade, 5)
        self.assertEqual(self.produto.descricao, "Atualizado")

    def teste_excluir_produto_view_get(self):
        url = reverse("excluir_produto", args=[self.produto.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Excluir")
        self.assertContains(response, "Monitor")

    def teste_excluir_produto_view_post(self):
        url = reverse("excluir_produto", args=[self.produto.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Produto.objects.filter(id=self.produto.id).exists())

class ProdutoValidacaoTest(TestCase):
    def teste_criar_produto_invalido(self):
        response = self.client.post(reverse('criar_produto'), {
            'nome': '',  
            'descricao': 'invalido',
            'preco': 10,
            'quantidade': 1
        })
        self.assertEqual(response.status_code, 200) 
        self.assertFalse(Produto.objects.filter(descricao='invalido').exists())

    def teste_criar_produto_preco_negativo(self):
        response = self.client.post(reverse('criar_produto'), {
            'nome': 'Produto Teste',
            'descricao': 'Descricao',
            'preco': -10,
            'quantidade': 10
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('Preço não pode ser negativo.', form.errors['preco'])

    def teste_criar_produto_quantidade_negativa(self):
        response = self.client.post(reverse('criar_produto'), {
            'nome': 'Produto Teste',
            'descricao': 'Descricao',
            'preco': 10,
            'quantidade': -5
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('Quantidade não pode ser negativa.', form.errors['quantidade'])

class ProdutoPaginasInexistentesTest(TestCase):
    def teste_editar_produto_inexistente(self):
        url = reverse('editar_produto', args=[999]) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def teste_excluir_produto_inexistente(self):
        url = reverse('excluir_produto', args=[999]) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)