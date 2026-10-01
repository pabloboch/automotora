from django.test import TestCase
from django.urls import reverse

from .models import Cliente, Usuario


class LoginFlowTests(TestCase):
    def setUp(self):
        self.usuario = Usuario(username='pepe')
        self.usuario.set_password('1234')
        self.usuario.save()

    def test_root_displays_login(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'automotora/login.html')

    def test_protected_page_redirects_to_login(self):
        response = self.client.get(reverse('home_page'))

        self.assertRedirects(response, reverse('login'))

    def test_valid_login_redirects_to_home(self):
        response = self.client.post(
            reverse('validarLogin'),
            {'txt_usuario': 'pepe', 'txt_password': '1234'},
        )

        self.assertRedirects(response, reverse('home_page'))
        self.assertEqual(self.client.session['usuario_id'], self.usuario.id_usuario)

    def test_invalid_password_keeps_login_page(self):
        response = self.client.post(
            reverse('validarLogin'),
            {'txt_usuario': 'pepe', 'txt_password': 'incorrecta'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuario o contraseña incorrectos')

    def test_logout_clears_session_and_protects_home_again(self):
        self.client.post(
            reverse('validarLogin'),
            {'txt_usuario': 'pepe', 'txt_password': '1234'},
        )

        response = self.client.post(reverse('cerrar_sesion'))

        self.assertRedirects(response, reverse('login'))
        self.assertNotIn('usuario_id', self.client.session)
        self.assertRedirects(self.client.get(reverse('home_page')), reverse('login'))


class ClienteRegistrationTests(TestCase):
    def setUp(self):
        session = self.client.session
        session['usuario_id'] = 1
        session.save()

    def test_duplicate_rut_shows_styled_error_instead_of_server_error(self):
        Cliente.objects.create(rut='208323938', nombre='Pepe', apellidos='Prat')

        response = self.client.get(reverse('ingresarCliente'), {
            'txt_rut_cliente': '208323938',
            'txt_nombre_cliente': 'Pepe',
            'txt_apellidos_cliente': 'Prat',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'automotora/resultado_operacion.html')
        self.assertContains(response, 'Ya existe un cliente registrado con ese RUT.')
        self.assertEqual(Cliente.objects.count(), 1)

    def test_new_rut_is_registered_successfully(self):
        response = self.client.get(reverse('ingresarCliente'), {
            'txt_rut_cliente': '208323938',
            'txt_nombre_cliente': 'Pepe',
            'txt_apellidos_cliente': 'Prat',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cliente guardado correctamente.')
        self.assertTrue(Cliente.objects.filter(rut='208323938').exists())
