from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import FlexApplication, L4Application, mTLSApplication
from extras.models import Tag

# @receiver(m2m_changed, sender=FlexApplication.tags.through)
# @receiver(m2m_changed, sender=L4Application.tags.through)
# @receiver(m2m_changed, sender=mTLSApplication.tags.through)
def validate_cluster_tag(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'pre_add':
        # Get the tags being added
        tags = Tag.objects.filter(pk__in=pk_set)
        # Check if the cluster has the same tags
        for tag in tags:
            if instance.cluster and not instance.cluster.tags.filter(name=tag.name).exists():
                raise ValidationError(f"Cluster {instance.cluster} does not have tag {tag.name}")