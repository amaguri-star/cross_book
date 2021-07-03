from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from django.urls import reverse_lazy, reverse

from ..models import *
from PIL import Image as PIL_Image
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
    im = PIL_Image.new(mode='RGB', size=(200, 200))
    im_io = BytesIO()
    im.save(im_io, 'JPEG')
    im_io.seek(0)
    value = InMemoryUploadedFile(im_io, None, 'random-name.jpg', 'image/jpeg', None, None)
    return value


def get_params(name="テストネーム", explanation="これはテスト用の説明です。",
               state='1', category='1', shipping_area='1', shipping_day='1'):
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
        'name': name,
        'explanation': explanation,
        'state': state,
        'category': category,
        'shipping_area': shipping_area,
        'shipping_day': shipping_day,
    }
    return params


class TestItemCreateView(LoggedInTestCase):

    def test_create_item_success(self):
        response = self.client.post(reverse_lazy('sell'), data=get_params(), follow=True)
        self.assertRedirects(response, expected_url='/mypage/{}/'.format(self.test_user.id))
        self.assertEqual(Item.objects.filter(name="テストネーム").count(), 1)

    def test_create_item_failure(self):
        response = self.client.post(reverse_lazy('sell'), data=get_params(state='0', category='0'), follow=True)
        self.assertFormError(response, 'form', field='state', errors='選択してください')
        self.assertFormError(response, 'form', field='category', errors='選択してください')


class TestItemEditView(LoggedInTestCase):

    def test_edit_item_success(self):
        item = Item.objects.create(
            user=self.test_user,
            name="タイトル編集前",
            explanation="これはテスト用の説明です。",
            state=1,
            category=Category.objects.get(id=1),
            shipping_area=1,
            shipping_day=1,
        )
        Image.objects.create(item=item, image=get_temporary_image())
        self.assertEqual(Item.objects.filter(name="タイトル編集前").count(), 1)
        response = self.client.post(reverse_lazy('edit_item', kwargs={'pk': item.pk}),
                                    data=get_params(name='タイトル編集後'), follow=True)
        self.assertRedirects(response, expected_url='/item/{}/'.format(item.id))
        self.assertEqual(Item.objects.filter(name="タイトル編集後").count(), 1)

    def test_edit_item_failure(self):
        response = self.client.post(reverse_lazy('edit_item', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)


class TestItemDeleteView(LoggedInTestCase):

    def test_delete_item_success(self):
        item = Item.objects.create(
            user=self.test_user,
            name="アイテム削除前",
            explanation="これはテスト用の説明です。",
            state=1,
            category=Category.objects.get(id=1),
            shipping_area=1,
            shipping_day=1,
        )
        response = self.client.post(reverse_lazy('delete_item', kwargs={'pk': item.pk}), follow=True)
        self.assertRedirects(response, reverse_lazy('my_page', kwargs={'pk': self.test_user.id}))
        self.assertEqual(Item.objects.filter(pk=item.pk).count(), 0)

    def test_delete_item_failure(self):
        response = self.client.post(reverse_lazy('delete_item', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)
