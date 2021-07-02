from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse_lazy, reverse

from ..models import *
from PIL import Image
from io import BytesIO


class LoggedInTestCase(TestCase):

    def setUp(self):
        self.password = 'testuserpassword'
        self.test_user = get_user_model().objects.create_user(
            username="test_user",
            email="test@gmail.com",
            password=self.password,
        )
        self.client.login(
            email=self.test_user.email,
            password=self.password,
        )


# def get_temporary_image():


class TestItemCreateView(LoggedInTestCase):

    def test_create_item_success(self):
        im = Image.new(mode='RGB', size=(200, 200))
        im_io = BytesIO()
        im.save(im_io, 'JPEG')
        im_io.seek(0)

        params = {
            'image_set-TOTAL_FORMS': '3',
            'image_set-INITIAL_FORMS': '0',
            'image_set-MIN_NUM_FORMS': '1',
            'image_set-MAX_NUM_FORMS': '3',
            'image_set-0-image': InMemoryUploadedFile(im_io, None, 'random-name.jpg', 'image/jpeg', None, None),
            'image_set-0-id': '',
            'image_set-0-item': '',
            'image_set-1-image': '',
            'image_set-1-id': '',
            'image_set-1-item': '',
            'image_set-2-image': '',
            'image_set-2-id': '',
            'image_set-2-item': '',
            'name': 'テストネーム',
            'explanation': 'これはテスト用の説明です。',
            'state': '1',
            'category': '0',
            'shipping_area': '1',
            'shipping_day': '1',
        }
        response = self.client.post(reverse_lazy('sell'), data=params)
        print(response.context['form'].errors)
        self.assertRedirects(response, expected_url='/mypage/{}/'.format(self.test_user.id))
        self.assertEqual(Item.objects.filter(name="テストネーム").count(), 1)

    def test_create_item_failure(self):
        im = Image.new(mode='RGB', size=(200, 200))
        im_io = BytesIO()
        im.save(im_io, 'JPEG')
        im_io.seek(0)

        params = {
            'image_set-TOTAL_FORMS': '3',
            'image_set-INITIAL_FORMS': '0',
            'image_set-MIN_NUM_FORMS': '1',
            'image_set-MAX_NUM_FORMS': '3',
            'image_set-0-image': InMemoryUploadedFile(im_io, None, 'random-name.jpg', 'image/jpeg', None, None),
            'image_set-0-id': '',
            'image_set-0-item': '',
            'image_set-1-image': '',
            'image_set-1-id': '',
            'image_set-1-item': '',
            'image_set-2-image': '',
            'image_set-2-id': '',
            'image_set-2-item': '',
            'name': 'テストネーム',
            'explanation': 'これはテスト用の説明です。',
            'state': '0',
            'category': "1",
            'shipping_area': '1',
            'shipping_day': '1',
        }
        response = self.client.post(reverse('sell'), data=params)
        self.assertFormError(response, 'form', 'state', '選択してください')
