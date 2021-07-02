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
        category_list = [
            '選択してください',
            '文学・エッセイ',
            'ビジネス・経済',
            '漫画ラノベ',
            '趣味・実用',
            '学門・資格・教育',
            '絵本・児童書',
            'エンタメ',
            '雑誌・ムック',
            'その他',
        ]
        for idx in range(len(category_list)):
            Category.objects.create(id=idx, name=category_list[idx])


def get_temporary_image():
    im = Image.new(mode='RGB', size=(200, 200))
    im_io = BytesIO()
    im.save(im_io, 'JPEG')
    im_io.seek(0)
    value = InMemoryUploadedFile(im_io, None, 'random-name.jpg', 'image/jpeg', None, None)
    return value


class TestItemCreateView(LoggedInTestCase):

    def test_create_item_success(self):
        params = {
            'image_set-TOTAL_FORMS': '3',
            'image_set-INITIAL_FORMS': '0',
            'image_set-MIN_NUM_FORMS': '1',
            'image_set-MAX_NUM_FORMS': '3',
            'image_set-0-image': get_temporary_image(),
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
            'category': '1',
            'shipping_area': '1',
            'shipping_day': '1',
        }
        response = self.client.post(reverse_lazy('sell'), data=params, follow=True)
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
            'image_set-0-image': get_temporary_image(),
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
            'category': "0",
            'shipping_area': '1',
            'shipping_day': '1',
        }
        response = self.client.post(reverse_lazy('sell'), data=params, follow=True)
        self.assertFormError(response, 'form', field='state', errors='選択してください')
        self.assertFormError(response, 'form', field='category', errors='選択してください')
