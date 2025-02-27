from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from FMInvoice.models import LigneCommande,Facture
from django.db.models.signals import post_save
from django.utils import timezone
from django.db import transaction

@receiver(m2m_changed, sender=LigneCommande.emission_date_emission.through)
def update_prix_total(sender, instance, action, **kwargs):
    """
    Met à jour le prix total de la LigneCommande lorsque la relation ManyToMany est modifiée.
    """
    # Vérifier que l'action est bien une modification de la relation ManyToMany
    if action in ['post_add', 'post_remove', 'post_clear']:
        # Recalculer le prix total
        instance.prix_total = instance.calcul_prix_total()
        # Sauvegarder uniquement le champ 'prix_total'
        instance.save(update_fields=['prix_total'])

