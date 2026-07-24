from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import ImportJob
from .serializers import ImportJobSerializer, ImportCreateSerializer


class ImportJobListView(generics.ListAPIView):
    serializer_class = ImportJobSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = ImportJob.objects.all()


class ImportJobDetailView(generics.RetrieveAPIView):
    serializer_class = ImportJobSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = ImportJob.objects.all()


class ImportCreateView(generics.CreateAPIView):
    serializer_class = ImportCreateSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        from .models import ImportJob
        import csv
        import os
        
        file_obj = serializer.validated_data['file']
        file_type = serializer.validated_data['file_type']
        
        job = ImportJob.objects.create(
            user=self.request.user,
            file=file_obj,
            file_type=file_type,
            file_name=file_obj.name,
        )
        
        if file_type == 'products':
            self.process_products(job, file_obj)
        
        return job

    def process_products(self, job, file_obj):
        import csv
        import os
        from apps.products.models import Product, Category, Brand
        
        file_path = file_obj.path
        job.status = 'processing'
        job.save()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                job.total_rows = sum(1 for _ in reader)
                f.seek(0)
                reader = csv.DictReader(f)
                
                for row in reader:
                    try:
                        category, _ = Category.objects.get_or_create(
                            name=row.get('category', 'Uncategorized'),
                            defaults={'slug': row.get('category_slug', row.get('category', '').lower().replace(' ', '-'))}
                        )
                        brand, _ = Brand.objects.get_or_create(
                            name=row.get('brand', 'Unknown'),
                            defaults={'slug': row.get('brand_slug', row.get('brand', '').lower().replace(' ', '-'))}
                        )
                        Product.objects.create(
                            name=row.get('name', ''),
                            slug=row.get('slug', ''),
                            short_description=row.get('short_description', ''),
                            full_description=row.get('full_description', ''),
                            description=row.get('description', ''),
                            brand=brand,
                            category=category,
                            seller=self.request.user,
                            sku=row.get('sku', ''),
                            barcode=row.get('barcode', ''),
                            price=row.get('price', 0),
                            discount_price=row.get('discount_price') or None,
                            stock=row.get('stock', 0),
                            weight=row.get('weight') or None,
                            material=row.get('material', ''),
                            warranty=row.get('warranty', ''),
                            status=row.get('status', 'draft'),
                            is_featured=row.get('is_featured', '').lower() == 'true',
                        )
                        job.success_count += 1
                    except Exception as e:
                        job.errors.append({'row': reader.line_num, 'error': str(e)})
                        job.error_count += 1
                    job.processed_rows += 1
            
            job.status = 'completed'
        except Exception as e:
            job.status = 'failed'
            job.errors.append({'error': str(e)})
        finally:
            job.completed_at = timezone.now()
            job.save()


class ExportProductsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        import csv
        from django.http import HttpResponse
        from apps.products.models import Product
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'name', 'slug', 'sku', 'price', 'discount_price', 'stock',
            'category', 'brand', 'status', 'is_featured', 'material', 'warranty'
        ])
        
        for product in Product.objects.all():
            writer.writerow([
                product.name, product.slug, product.sku, product.price,
                product.discount_price or '', product.stock,
                product.category.name, product.brand.name, product.status,
                product.is_featured, product.material, product.warranty
            ])
        
        return response
