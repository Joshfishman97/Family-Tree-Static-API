from flask_sqlalchemy import SQLAlchemy
from random import randint


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._members = [
            {   
                "name": "George",
                "children":[{"name": "Pedro"}],
                "id": 123
            }
        ]

    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        return randint(0, 99999999)

    def add_member(self, member):
        member["id"] = self._generateId() 
        if "parent" in member:
            for grandparent in self._members:
                if grandparent["name"] == member["parent"]:
                    if "children" in grandparent:
                        grandparent["children"].append(member)
                    else: 
                        grandparent["children"] = [member]
                else:
                    for parent in grandparent["children"]:
                        if parent["name"] == member["parent"]:
                            if "children" in parent:
                                parent["children"].append(member)
                            else: 
                                parent["children"] = [member]
        else:
            self._members.append(member)
        return self._members

    def get_descendants(self,id):
        children = []
        grandchildren = []
        for grandparent in self._members:
            if grandparent["id"] == id:
                for child in grandparent["children"]:
                    children.append(child["name"])
                    if "children" in child:
                        for grandchild in child["children"]:
                            grandchildren.append(grandchild)
                return {"children":children, "grandchildren":grandchild}
            else:
                for parent in grandparent["children"]:
                        if parent["id"] == id:
                            if "children" in parent:
                                for child in parent["children"]:
                                    children.append(child["name"])
                            return {"children":children}
    
    def delete_member(self, id):
        # fill this method and update the return
        for i in range(len(self._members)):
            if self._members[i]["id"] == id:
                removed = self._members.pop(i)
        return removed


    def get_member(self, id):
        # fill this method and update the return
        for person in range(self._members):
            if person["id"] == id:
                return person
        return None

    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members

    
