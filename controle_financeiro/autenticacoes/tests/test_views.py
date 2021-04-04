from django.test import Client, TestCase


class ViewTest(TestCase):
    def test_registrar_template(self):
        response = self.client.get("/autenticacoes/registrar/")
        self.assertEqual(response.status_code, 200)

    def test_registrar_sucesso(self):
        c = Client()
        response = c.post(
            "/autenticacoes/registrar/",
            {
                "username": "teste-um",
                "password1": "123456",
                "password2": "123456",
                "first_name": "TesteUm",
                "last_name": "Da Silva",
                "email": "teste.um@teste.com.br",
            },
        )
        self.assertEqual(response.status_code, 200)

    # def test_registrar_erro(self):
    #     c = Client()
    #     response = c.post(
    #         "/autenticacoes/registrar/",
    #         {
    #             "username": "T *%¨&%& Acc",
    #             "password1": "123456",
    #             "password2": "",
    #             "first_name": "TesteUm",
    #             "last_name": "Da Silva",
    #             "email": "teste.com.br",
    #         },
    #     )
    #     print(response)
    #     self.assertEqual(response.status_code, 200)
