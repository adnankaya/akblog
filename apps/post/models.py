from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator
from taggit.managers import TaggableManager
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from slugify import slugify
from ckeditor.fields import RichTextField
# internals
from apps.core.models import Base
from apps.core.utils import get_today_with_timezone
from .managers import PostObjectsManager, CategoryObjectsManager
from apps.core.models import UrlHit
# globals
User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=32)
    name_en = models.CharField(max_length=32, null=True, blank=True)
    slug = models.SlugField(max_length=250, unique=True)
    icon = models.CharField(max_length=64, null=True, blank=True)

    # actives = CategoryObjectsManager()

    CACHE_KEY = "categories"

    class Meta:
        db_table = "t_category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Post(Base):
    """
    Post Model
    """
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    body = RichTextField(validators=[MaxLengthValidator(81920)])
    slug = models.SlugField(max_length=250, unique_for_date='created_date')
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    tags = TaggableManager()
    actives = PostObjectsManager()

    CACHE_KEY = "post_actives"

    class Meta:
        db_table = "t_post"
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        unique_together = ["created_by", "slug"]

    def __str__(self) -> str:
        return self.title

    def get_tags(self):
        return self.tags.all()

    def get_hit_count(self):
        qs = UrlHit.objects.filter(url=self.get_absolute_url()).first()
        if qs:
            return qs.hits_count
        return 0

    def process_slugify(self):
        if self.created_date:
            _date = self.created_date.strftime("%Y-%m-%d")
        else:
            _date = timezone.datetime.today().strftime("%Y-%m-%d")
        self.slug = f"{slugify(self.title)}-{_date}"

    def process_post_package(self):
        """
        When a user creates a post, this function ensures to create
        a PostPackage object if the user has OrderedPackage.
        """
        try:
            op = self.created_by.get_active_ordered_package()
        except OrderedPackage.DoesNotExist:
            op = None
        try:
            bp = op.postpackage_set.last()
            used = bp.used
        except (PostPackage.DoesNotExist, AttributeError):
            used = 0
        finally:
            used += 1
        if op:
            bp = PostPackage.objects.create(
                post=self,
                ordered_package=op,
                used=used)
            #  if user consumed all package amount deactivate ordered package
            if bp.used == bp.ordered_package.package.total_amount:
                bp.ordered_package.is_active = False
                bp.ordered_package.save()

    def save(self, *args, **kwargs):
        try:
            with transaction.atomic():
                self.process_slugify()
                super(Post, self).save(*args, **kwargs)
                self.process_post_package()
        except Exception as e:
            raise ValueError(e)

    def get_absolute_url(self):
        return reverse('post:post-detail',
                       args=[
                           self.created_date.year,
                           self.created_date.month,
                           self.created_date.day,
                           self.slug,
                           self.pk
                       ])


class PostImage(Base):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    image = models.ImageField(_("Image"), upload_to="images/posts/")

    class Meta:
        db_table = 't_post_image'
        verbose_name = "Post Image"
        verbose_name_plural = "Post Images"

    def __str__(self) -> str:
        return self.image.path


class InappropriatePost(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    reason = models.TextField("Reason",
                              null=True, blank=True,
                              validators=[MaxLengthValidator(280)]
                              )
    reported_by = models.ForeignKey(User, related_name="reported_inappropriate_posts",
                                    on_delete=models.CASCADE)

    class Meta:
        db_table = 't_inappropriate_post'
        verbose_name = "Inappropriate Post"
        verbose_name_plural = "Inappropriate Posts"
        unique_together = ["post", "reported_by"]


class Package(Base):
    name = models.CharField("Name", max_length=32, unique=True)
    description = models.TextField(_("Description"))
    amount = models.PositiveSmallIntegerField(
        _("Total Amount"), default=1)
    gift = models.PositiveSmallIntegerField(_("Gift"), default=1)
    days_delta = models.PositiveSmallIntegerField(
        _("Days for Due"), default=365)
    css_class = models.CharField(max_length=140, null=True, blank=True)

    price_per = models.DecimalField(
        _("Price Per"), max_digits=8, decimal_places=2, default=1)
    discount = models.DecimalField(
        _("Discount"), max_digits=8, decimal_places=2, default=0)
    currency_symbol = models.CharField(max_length=1, default="₺")
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 't_package'
        verbose_name = "Package"
        verbose_name_plural = "Packages"

    def __str__(self) -> str:
        return self.name

    def get_total_cost(self):
        return (self.price_per * self.amount) - self.discount

    def get_actual_cost(self):
        return self.price_per * self.amount

    @property
    def total_amount(self):
        return self.amount + self.gift


class PostPackage(Base):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    ordered_package = models.ForeignKey(
        "OrderedPackage", on_delete=models.CASCADE)
    used = models.SmallIntegerField("Used", default=0)

    class Meta:
        db_table = 't_post_package'
        verbose_name = "Post Package"
        verbose_name_plural = "Post Packages"

    def last_used_date(self):
        return self.updated_date

    def get_balance(self):
        """How many post amount does a user have?"""
        return self.ordered_package.package.total_amount - self.used


class OrderedPackage(Base):
    package = models.ForeignKey("Package", on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    due_date = models.DateField(_("Due Date"), null=True)

    class Meta:
        db_table = 't_ordered_package'
        verbose_name = "Ordered Package"
        verbose_name_plural = "Ordered Packages"

    def __str__(self) -> str:
        return f"{self.user.username} {self.package.name}"

    def save(self, *args, **kwargs):
        # today = get_today_with_timezone()
        # self.due_date = today.date() + timezone.timedelta(days=self.package.days_delta)
        super().save(*args, **kwargs)


class PostCreateRule(Base):
    rule = models.CharField(max_length=120)

    class Meta:
        db_table = 't_post_create_rule'
        verbose_name = "Post Create Rule"
        verbose_name_plural = "Post Create Rules"

    def __str__(self) -> str:
        return self.rule
