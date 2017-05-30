from app.data import db
from app.data.models import Company, Group, G_F_Association
from app.utils import fake_firma, fake_group

def test_assoc():
    parent = fake_firma()
    child1 = fake_group()
    child2 = fake_group()

    parent.save()
    child1.save()
    child2.save()

    parent.add_group(child1)
    parent.add_group(child2)

    ff=Company.find_by_id(parent.id)
    ff.delete()