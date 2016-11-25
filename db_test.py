from app.data import db
from app.data.models import Firma, Group, G_F_Association
from app.utils import fake_firma, fake_group

def test_assoc():
    parent = fake_firma()
    child1 = fake_group()
    child2 = fake_group()

    parent.save()
    child1.save()
    child2.save()

    assoc1 = G_F_Association()
    assoc1.firma_id = parent.id
    assoc1.group_id = child1.id

    assoc2 = G_F_Association()
    assoc2.firma_id = parent.id
    assoc2.group_id = child2.id

    assoc1.save()
    assoc2.save()

    ff=Firma.find_by_id(parent.id)
    ff.delete()