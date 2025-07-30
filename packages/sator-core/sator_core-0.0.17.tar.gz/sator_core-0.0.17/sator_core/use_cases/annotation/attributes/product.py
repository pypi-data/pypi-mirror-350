from sator_core.models.product.attributes import ProductAttributes
from sator_core.models.product.descriptor import ProductDescriptor

from sator_core.ports.driven.classifiers.product import ProductClassifierPort
from sator_core.ports.driven.persistence.storage import StoragePersistencePort
from sator_core.ports.driving.annotation.attributes.product import ProductAttributesAnnotationPort


class ProductAttributesAnnotation(ProductAttributesAnnotationPort):
    def __init__(self, product_classifier: ProductClassifierPort, storage_port: StoragePersistencePort):
        self.product_classifier = product_classifier
        self.storage_port = storage_port

    def annotate_product_attributes(self, product_id: str) -> ProductDescriptor | None:
        product_descriptor = self.storage_port.load(ProductDescriptor, product_id)

        if product_descriptor:
            return product_descriptor

        product_attributes = self.storage_port.load(ProductAttributes, product_id)

        if product_attributes:
            product_part = self.product_classifier.classify_product_part(product_attributes)
            product_type = self.product_classifier.classify_product_type(product_attributes, product_part)
            license_type = self.product_classifier.classify_license_type(product_attributes)

            product_descriptor = ProductDescriptor(
                product_id=product_id,
                type=product_type,
                part=product_part,
                license_type=license_type
            )

            self.storage_port.save(product_descriptor, product_id)
            return product_descriptor

        return None
