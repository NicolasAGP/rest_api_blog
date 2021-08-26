from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

from core import models


def sample_user(email='test@gmail.com', password='testpass'):
    """ Crear usuario ejemplo """
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
        def test_create_user_with_email_successful(self):
            """ Probar creando un nuevo usuario con un email correctamente """
            email = 'test@gmail.com'
            password = 'Testpass123'
            user = get_user_model().objects.create_user(
                email=email,
                password=password
            )

            self.assertEqual(user.email, email)
            self.assertTrue(user.check_password(password))

        def test_new_user_email_normalized(self):
            """ Testea email para nuevo usuario normalizados """
            email = 'test@GMAIL.COM'
            user = get_user_model().objects.create_user(email, 'Testpass123')

            self.assertEqual(user.email, email.lower())

        def test_new_user_invalid_email(self):
            """ Nuevo usuario email invalido """
            with self.assertRaises(ValueError):
                get_user_model().objects.create_user(None, 'Testpass123')

        def test_create_new_superuser(self):
            """ Probar super usuario creado """
            email = 'test@gmail.com'
            password = 'Testpass123'
            user = get_user_model().objects.create_superuser(
                email=email,
                password=password
            )

            self.assertTrue(user.is_superuser)
            self.assertTrue(user.is_staff)

        def test_tag_str(self):
            """ Probar representacion en cadena de texto del tag """
            tag = models.Tag.objects.create(
                user=sample_user(),
                name='Meat'
            )

            self.assertEqual(str(tag), tag.name)

        def test_ingredient_str(self):
            """ Probar representacion en cadena de texto del ingrediente """
            ingredient = models.Ingredient.objects.create(
                user=sample_user(),
                name='Banana'
            )

            self.assertEqual(str(ingredient), ingredient.name)

        def test_recipe_str(self):
            """Probar representacion en cadena de texto de las recetas"""
            recipe = models.Recipe.objects.create(
                user=sample_user(),
                title='Steak and mushroom sauce',
                time_minutes=5,
                price=5.00
            )

            self.assertEqual(str(recipe), recipe.title)

        @patch('uuid.uuid4')
        def test_recipe_file_name_uuid(self, mock_uuid):
            """ Probar que imagen ha sido guardado en lugar correcto """
            uuid = 'test-uuid'
            mock_uuid.return_value = uuid
            file_path = models.recipe_image_file_path(None, 'myimage.jpg')

            exp_path = f'uploads/recipe/{uuid}.jpg'
            self.assertEqual(file_path, exp_path)
