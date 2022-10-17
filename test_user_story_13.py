import unittest
from TEAM1_GEDCOM import *


class TestUserStory13(unittest.TestCase):
    def setUp(self):
        child1 = Individual("@I1@")
        child1.name = "Mark /Rivers/"
        child1.sex = "M"
        child1.birth = datetime.strptime("21 APR 1987", "%d %b %Y").date()
        child1.child_id = "@F1@"

        child2 = Individual("@I2")
        child2.name = "Mary /Rivers/"
        child2.sex = "F"
        child2.birth = datetime.strptime("21 APR 1987", "%d %b %Y").date()
        child2.child_id = "@F1@"

        dad = Individual("@I3@")
        dad.name = "Jason /Rivers/"
        dad.sex = "M"
        dad.birth = datetime.strptime("19 SEP 1960", "%d %b %Y").date()
        dad.spouse_id = "@F1@"

        mom = Individual("@I4@")
        mom.name = "Abigail /Glute/"
        mom.sex = "F"
        mom.birth = datetime.strptime("3 OCT 1965", "%d %b %Y").date()
        mom.spouse_id = "@F1@"

        fam1 = Family("@F1@")
        fam1.husband = "@I3@"
        fam1.wife = "@I4@"
        fam1.children.append("@I1@")
        fam1.children.append("@I2@")
        fam1.marriage = datetime.strptime("29 JUL 1986", "%d %b %Y").date()

        individuals.append(child1)
        individuals.append(child2)
        individuals.append(dad)
        individuals.append(mom)

        families.append(fam1)

    def tearDown(self):
        individuals.clear()
        families.clear()

    def test_twins_pass(self):
        table = []
        sibling_age_space(table)
        self.assertTrue(table[0][3])

    def test_twins_fail(self):
        get_individual("@I1@").birth = datetime.strptime("21 APR 1987", "%d %b %Y").date()
        get_individual("@I2@").birth = datetime.strptime("24 APR 1987", "%d %b %Y").date()
        table = []
        sibling_age_space(table)
        self.assertFalse(table[0][3])

    def test_sibling_pass(self):
        table = []
        sibling_age_space(table)
        self.assertTrue(table[0][3])

    def test_sibling_fail(self):
        table = []
        get_individual("@I1@").birth = datetime.strptime("21 APR 1987", "%d %b %Y").date()
        get_individual("@I2@").birth = datetime.strptime("24 JUN 1987", "%d %b %Y").date()
        sibling_age_space(table)
        self.assertFalse(table[0][3])


if __name__ == '__main__':
    unittest.main(verbosity=2)
