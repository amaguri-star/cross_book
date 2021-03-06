from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
# from django.conf import settings
from django.template.defaultfilters import slugify
import uuid


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('Users must have an name')
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """"カスタムユーザーモデル"""

    username = models.CharField(_('username'), max_length=30, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    image = models.ImageField(default='/profile_pics/default.png', upload_to='profile_pics')
    profile_text = models.TextField(verbose_name="プロフィール文", max_length=250, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last_name'), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.')
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designate whether this user should be treated as active.'
                    'Unselect this instead of deleting accounts.')
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


LOCATION = (
    (0, "選択してください"),
    (1, "北海道"),
    (2, "青森県"),
    (3, "岩手県"),
    (4, "宮城県"),
    (5, "秋田県"),
    (6, "山形県"),
    (7, "福島県"),
    (8, "茨城県"),
    (9, "栃木県"),
    (10, "群馬県"),
    (11, "埼玉県"),
    (12, "千葉県"),
    (13, "東京都"),
    (14, "神奈川県"),
    (15, "新潟県"),
    (16, "富山県"),
    (17, "石川県"),
    (18, "福井県"),
    (19, "山梨県"),
    (20, "長野県"),
    (21, "岐阜県"),
    (22, "静岡県"),
    (23, "愛知県"),
    (24, "三重県"),
    (25, "滋賀県"),
    (26, "京都府"),
    (27, "大阪府"),
    (28, "兵庫県"),
    (29, "奈良県"),
    (30, "和歌山県"),
    (31, "鳥取県"),
    (32, "島根県"),
    (33, "岡山県"),
    (34, "広島県"),
    (35, "山口県"),
    (36, "徳島県"),
    (37, "香川県"),
    (38, "愛媛県"),
    (39, "高知県"),
    (40, "福岡県"),
    (41, "佐賀県"),
    (42, "長崎県"),
    (43, "熊本県"),
    (44, "大分県"),
    (45, "宮崎県"),
    (46, "鹿児島県"),
    (47, "沖縄県"),
    (48, "未定")
)


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    zip_code = models.CharField(verbose_name='郵便番号', max_length=8, blank=True, null=True)
    address1 = models.IntegerField(verbose_name='都道府県', blank=True, null=True, choices=LOCATION)
    address2 = models.CharField(verbose_name='市区町村番地', max_length=40, blank=True, null=True)
    address3 = models.CharField(verbose_name='建物名', max_length=40, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} の配送先情報'


class Category(models.Model):
    id = models.IntegerField(primary_key=True, editable=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class Item(models.Model):
    DAYS = (
        (0, "選択してください"),
        (1, "1~2日で発送"),
        (2, "2~3日で発送"),
        (3, "4~7日で発送")
    )

    STATE = (
        (0, "選択してください"),
        (1, "未使用"),
        (2, "未使用に近い状態"),
        (3, "目立った傷や汚れなし"),
        (4, "やや傷や汚れあり"),
        (5, "傷や汚れあり"),
        (6, "全体的に状態が悪い")
    )

    def validate_choice(value):
        if value == 0:
            raise ValidationError(
                _("選択してください"),
                params={'value': value}
            )
        return value

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="商品名", max_length=30)
    explanation = models.TextField(verbose_name="出品者からの一言", max_length=3000, blank=True)
    state = models.IntegerField(verbose_name="商品の状態", choices=STATE, default=STATE[0][0], validators=[validate_choice])
    category = models.ForeignKey("Category", default="選択してください", verbose_name="カテゴリ", validators=[validate_choice], on_delete=models.DO_NOTHING)
    shipping_area = models.IntegerField(verbose_name="発送元の地域", choices=LOCATION, default=LOCATION[0][0],
                                        validators=[validate_choice])
    shipping_day = models.IntegerField(verbose_name="発送までの日数", choices=DAYS, default=DAYS[0][0],
                                       validators=[validate_choice])
    at_created = models.DateTimeField(verbose_name="出品日", auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}\'s {self.name}'


def get_image_filename(instance, filename):
    title = instance.item.name
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)


class Image(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='', upload_to=get_image_filename)

    def __str__(self):
        return f'{self.item.name}\'s image'


class Like(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} liked {self.item.name}'


class Room(models.Model):
    timestamp = models.DateTimeField(auto_now=True)


class RoomMember(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.room} has {self.member}'


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name="room_messages", on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.message}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    comment = models.TextField(verbose_name="コメント", max_length="1000")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.comment}'


class Notification(models.Model):
    NOTIFI_TYPE = (
        ('comment', 'comment'),
        ('like', 'like'),
        ('transaction_request', 'transaction_request')
    )

    actor = models.ForeignKey(User, related_name='notify_actor', on_delete=models.CASCADE, null=True)
    recipient = models.ForeignKey(User, related_name='notify_recipient', on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=255, choices=NOTIFI_TYPE)
    description = models.CharField(max_length=255)
    target_content_type = models.ForeignKey(
        ContentType,
        related_name='notify_target',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')
    new_message = models.BooleanField(default=True)
    unread = models.BooleanField(default=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.actor} {self.description}'


class TradeRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} request to {self.item.name}'


class Trade(models.Model):
    trading_start_date = models.DateTimeField(auto_now_add=True)


class TradeMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.message}'


class TradeInfo(models.Model):
    trader = models.ForeignKey(User, models.SET_NULL, null=True)
    traded_item = models.ForeignKey(Item, models.SET_NULL, null=True)
    trade = models.ForeignKey(Trade, models.CASCADE)
