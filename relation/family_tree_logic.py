from .models import PersonDetail, RelationShip
from django.db.models import Q
import logging

class FamilyTree:
    """
    This class is the base class for handling all operation of family tree.
    """

    def __init__(self, logger:logging) -> None:
        self.logger = logger

    def add_person(self, name, gender):
        """
        This method is used for creating new person in database.
        args:
            name:str("name of a person")
            gender:str("gender of a person")
        return:
            Boolean value either True or False
        """
        self.logger.info("FamilyTree | Starting method add_person")
        status = False
        try:
            self.logger.info("FamilyTree | Executing query to insert data into PersonDetail model")
            PersonDetail.objects.create(name = name, gender = gender)
            self.logger.info("FamilyTree | Successfully inserted")
            status = True
        except Exception as exc:
            self.logger.error(f"FamilyTree | Exception occured in add_person method, message: {exc}")
        
        finally:
            return status
    
    def get_person(self, id):
        """
        This method is used for getting person object from its id
        args:
            id:int("id of a person")
        return:
            False or PersonDetail object
        """
        self.logger.info("FamilyTree | Starting method get_person")
        res = False
        try:
            self.logger.info(f"FamilyTree | Executing query to get person detail with id {id}")
            res = PersonDetail.objects.get(id = id)
            self.logger.info("FamilyTree | Successfully inserted")

        except Exception as exc:
            self.logger.error(f"FamilyTree | Exception occured in get_person method, message: {exc}")
        
        finally:
            return res
    
    def add_relation_ship(self, person_1_id, person_2_id, r_type):
        """
        This method is used for adding relation between two person.
        In this method person 1 will be parent of person 2 or wife
        args:
            person_1_id: int("id of person 1")
            person_2_id: int("id of person 2")
            r_type: str("relation name in [father,mother,wife]")
        return:
            Boolean value either True or False
        """
        self.logger.info("FamilyTree | Starting method add_relation_ship")
        status = False
        message = "Internal server error"
        try:
            
            person_1 = self.get_person(id = person_1_id)
            person_2 = self.get_person(id = person_2_id)

            if person_1 and person_2:

                if person_1 != person_2:

                    duplicate = None
                    self.logger.info("FamilyTree | Executing query to check for duplicate relation")
                    try:
                        #This query will check for duplicate entry and also it will check for circular relation or any unwanted relation
                        #like a person has already a son or daughter of a person
                        duplicate = RelationShip.objects.get(Q(Q(first_person = person_1) & Q(
                                                second_relation = person_2)) | Q(Q(first_person = person_2) & 
                                                Q(second_relation = person_1)))
                    except:
                        duplicate = None
                    
                    if not duplicate:
                        self.logger.error("FamilyTree | No duplicate relation")
                        self.logger.info("FamilyTree | Executing query for inserting into RelationShip model")
                        
                        RelationShip.objects.create(first_person = person_1,
                                                second_relation = person_2,
                                                r_type = r_type)
                        self.logger.info("FamilyTree | Successfully inserted")
                        status = True
                        message = "Success"
                    
                    else:
                        self.logger.error("FamilyTree | Duplicate relation already exist")
                        status = False
                        message = "Relationship already exists"

                else:
                    self.logger.error("FamilyTree | both person details are same")
                    status = False
                    message = "Both person details are same, please provide two different person"

            else:
                self.logger.error("FamilyTree | Person details does not exist in database")
                status = False
                message = "Person details does not exist in database, please provide correct details"

        except Exception as exc:
            self.logger.error(f"FamilyTree | Exception occured in add_relation_ship method, message: {exc}")
            message = "Internal server error"

        finally:
            return status, message


    def get_total_sons_or_daughters(self, parant_id, sons=True):
        """
        This method is used for counting total number of sons or daughters a parent has.
        args:
            parant_id:int("id of a person")
            sons: boolean("Boolean field")
        return:
            total_count of sons if present or 0
        """
        self.logger.info("FamilyTree | Starting method get_total_sons_or_daughters")
        count = 0
        try:
            person = self.get_person(id = parant_id)

            self.logger.info(f"FamilyTree | Executing query to count number of sons or daughters a person has.")
            
            #this gender is used for making decision weather we are counting sons or daughters
            gender = "male"
            if not sons:
                gender = "femail"

            if person.gender == "male":
                count = RelationShip.objects.filter(first_person = person,
                                                second_relation__gender = gender,
                                                r_type="father").count()
                
            else:
                count = RelationShip.objects.filter(first_person = person,
                                                second_relation__gender = gender,
                                                r_type="mother").count()
        
            self.logger.info("FamilyTree | Query Executed successfully")

        except Exception as exc:
            self.logger.error(f"FamilyTree | Exception occured in get_total_sons_or_daughters method, message: {exc}")
        
        finally:
            return count


    def get_total_wives(self, parant_id):
        """
        This method is used for counting total number of wives a person has.
        args:
            parant_id:int("id of a person")
        return:
            total_count of wives
        """
        self.logger.info("FamilyTree | Starting method get_total_wives")
        count = 0
        try:
            person = self.get_person(id = parant_id)

            self.logger.info(f"FamilyTree | Executing query to count number of wives a person has.")
            
            count = RelationShip.objects.filter(second_relation = person,
                                            r_type="wife").count()
        
            self.logger.info("FamilyTree | Query Executed successfully")

        except Exception as exc:
            self.logger.error(f"FamilyTree | Exception occured in get_total_wives method, message: {exc}")
        
        finally:
            return count
    

    def get_father_name(self, son_id):
        """
        This method is used for getting father name of a person.
        args:
            son_id:int("id of a person")
        return:
            father name
        """
        self.logger.info("FamilyTree | Starting method get_father_name")
        name = None
        try:
            person = self.get_person(id = son_id)
            self.logger.info(f"FamilyTree | Executing query to count number of wives a person has.")
            name = RelationShip.objects.select_related("first_person").get(second_relation = person,
                                            r_type="father").first_person.name
        
            self.logger.info("FamilyTree | Query Executed successfully")

        except Exception as exc:
            self.logger.error(f"FamilyTree | Exception occured in get_father_name method, message: {exc}")
        
        finally:
            return name