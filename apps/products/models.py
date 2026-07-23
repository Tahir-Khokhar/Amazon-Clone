import logging
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Tags & Attributes (unchanged from original)
# ---------------------------------------------------------------------------

class Tag(models.Model):
    """Reusable tags for products (e.g., 'new-arrival', 'sale')."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    """Attribute definition (e.g., 'Material', 'Capacity')."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    """Value of a product attribute (e.g., 'Cotton' for attribute 'Material')."""
    attribute = models.ForeignKey(
        ProductAttribute, on_delete=models.CASCADE, related_name='values'
    )
    value = models.CharField(max_length=100)
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='attribute_values'
    )

    class Meta:
        unique_together = ['attribute', 'product']

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


# ---------------------------------------------------------------------------
# Product Status
# ---------------------------------------------------------------------------

class ProductStatus(models.TextChoices):
    DRAFT = 'draft', _('Draft')
    PUBLISHED = 'published', _('Published')
    OUT_OF_STOCK = 'out_of_stock', _('Out of Stock')


# ---------------------------------------------------------------------------
# ProductImage
# ---------------------------------------------------------------------------

class ProductImage(models.Model):
    """Multiple images per product with auto-delete on removal."""
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'created_at']

    def __str__(self):
        return f"{self.product.name} - Image #{self.id}"

    def save(self, *args, **kwargs):
        """Ensure only one primary image per product."""
        if self.is_primary:
            ProductImage.objects.filter(
                product=self.product, is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# ProductVariant
# ---------------------------------------------------------------------------

class ProductVariant(models.Model):
    """Size / Color / other variant with its own price & stock."""
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='variants'
    )
    sku = models.CharField(max_length=100, unique=True, verbose_name=_("SKU"))
    name = models.CharField(max_length=200)
    additional_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00'),
        help_text=_("Additional price on top of the base product price.")
    )
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)
    weight = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        parts = [self.name]
        if self.color:
            parts.append(self.color)
        if self.size:
            parts.append(self.size)
        return " / ".join(parts)

    def clean(self):
        if self.stock < 0:
            raise ValidationError({'stock': _("Stock cannot be negative.")})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# ProductSpecification (NEW)
# ---------------------------------------------------------------------------

class ProductSpecification(models.Model):
    """Key-value specifications for a product (e.g., 'Processor: i7')."""
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='specifications'
    )
    key = models.CharField(max_length=100, verbose_name=_("Specification Key"))
    value = models.CharField(max_length=500, verbose_name=_("Specification Value"))

    class Meta:
        ordering = ['key']
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self):
        return f"{self.key}: {self.value}"


# ---------------------------------------------------------------------------
# Inventory (kept from original but may be optional)
# ---------------------------------------------------------------------------

class Inventory(models.Model):
    """Tracks stock levels per variant."""
    product_variant = models.OneToOneField(
        ProductVariant, on_delete=models.CASCADE, related_name='inventory'
    )
    stock_available = models.IntegerField(default=0)
    stock_reserved = models.IntegerField(default=0)
    stock_sold = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=5)
    last_restocked = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Inventories'

    def __str__(self):
        return f"{self.product_variant.name} – Inventory"


# ---------------------------------------------------------------------------
# Product (Main Model)
# ---------------------------------------------------------------------------

class Product(models.Model):
    """Core eCommerce product model."""

    # --- Relations ---
    brand = models.ForeignKey(
        'brands.Brand', on_delete=models.CASCADE, related_name='products'
    )
    category = models.ForeignKey(
        'categories.Category', on_delete=models.CASCADE, related_name='products'
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')

    # --- Identity ---
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.CharField(max_length=500, blank=True)
    full_description = models.TextField(
        blank=True, help_text=_("Complete product description.")
    )
    # Keep original description field for backward compatibility
    description = models.TextField(blank=True, default="")

    # --- SKU & Pricing ---
    sku = models.CharField(max_length=100, unique=True, verbose_name=_("SKU"))
    barcode = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    # --- Stock ---
    stock = models.IntegerField(
        default=0, validators=[MinValueValidator(0)],
        help_text=_("Current available stock quantity.")
    )

    # --- Media ---
    thumbnail = models.ImageField(
        upload_to='products/thumbnails/', blank=True, null=True
    )

    # --- Physical attributes ---
    weight = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    material = models.CharField(max_length=100, blank=True)
    warranty = models.CharField(max_length=100, blank=True)

    # --- Status & flags ---
    status = models.CharField(
        max_length=20, choices=ProductStatus.choices,
        default=ProductStatus.DRAFT
    )
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # --- Ratings ---
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=Decimal('0.00'),
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_("Average rating from 0.00 to 5.00.")
    )
    total_reviews = models.PositiveIntegerField(default=0)

    # --- Tracking ---
    views_count = models.IntegerField(default=0)
    sales_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['sku']),
            models.Index(fields=['status', 'is_active']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.name

    # ------------------------------------------------------------------
    # Slug auto-generation
    # ------------------------------------------------------------------
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        self.full_clean()
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        """Generate a unique slug from the product name."""
        base_slug = slugify(self.name)
        if not base_slug:
            base_slug = f"product-{self.pk or 'new'}"
        slug = base_slug
        counter = 1
        while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    # ------------------------------------------------------------------
    # Model-level validation
    # ------------------------------------------------------------------
    def clean(self):
        errors = {}

        # Negative stock
        if self.stock < 0:
            errors['stock'] = _("Stock cannot be negative.")

        # Duplicate SKU check (unique constraint will also catch this)
        if self.sku:
            qs = Product.objects.filter(sku__iexact=self.sku).exclude(pk=self.pk)
            if qs.exists():
                errors['sku'] = _("A product with this SKU already exists.")

        # Discount price > actual price
        if self.discount_price is not None and self.price is not None:
            if self.discount_price > self.price:
                errors['discount_price'] = _(
                    "Discount price cannot be greater than the actual price."
                )

        # Update status based on stock (auto-set to out_of_stock when stock = 0)
        if self.stock == 0 and self.status == ProductStatus.PUBLISHED:
            # Warn but don't force; user can keep as published with 0 stock or we auto-change
            logger.warning(
                f"Product '{self.name}' (SKU: {self.sku}) is published but stock is 0."
            )

        if errors:
            raise ValidationError(errors)

    # ------------------------------------------------------------------
    # Stock management
    # ------------------------------------------------------------------
    def reduce_stock(self, quantity: int):
        """Reduce stock after an order is placed. Raises ValueError if insufficient."""
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        if self.stock < quantity:
            raise ValueError(
                f"Insufficient stock for '{self.name}': "
                f"requested {quantity}, available {self.stock}."
            )
        self.stock -= quantity
        self.sales_count += quantity
        if self.stock == 0 and self.status == ProductStatus.PUBLISHED:
            self.status = ProductStatus.OUT_OF_STOCK
        self.save(update_fields=['stock', 'sales_count', 'status'])

    def restore_stock(self, quantity: int):
        """Restore stock when an order is cancelled / returned."""
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        self.stock += quantity
        self.sales_count = max(0, self.sales_count - quantity)
        if self.stock > 0 and self.status == ProductStatus.OUT_OF_STOCK:
            self.status = ProductStatus.PUBLISHED
        self.save(update_fields=['stock', 'sales_count', 'status'])
