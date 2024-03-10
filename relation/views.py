from django.shortcuts import render, HttpResponse, redirect
import json
from family_tree.app_logger import logger
from .family_tree_logic import FamilyTree
from .models import PersonDetail
from django.views import View


def home(request):
    all_person = PersonDetail.objects.all()
    return render(request, "index.html",context = {"all_person":all_person})


class CreatePerson(View):
    """This class is a django view class for creating new person in database"""

    def post(self, request):
        """Handling post request of the user"""
        logger.info("CreatePerson | Starting post method")
        name = request.POST.get("name","").strip()
        gender = request.POST.get("gender","").strip()

        logger.info("CreatePerson | Checking if name and gender is present in request body")
        if name != "" and gender != "" and len(name) > 3:
            fam_obj = FamilyTree(logger)

            logger.info("CreatePerson | Calling method add_person")
            res = fam_obj.add_person(name, gender)
            if res:
                logger.info("CreatePerson | method add_person successfully executed")
                return HttpResponse("Successfully created", status=200)
            
            else:
                logger.error("CreatePerson | method add_person failed")
                return HttpResponse("Failed to create, please try after some time", status=500)
        else:
            logger.error("CreatePerson | name and gender is not present in request body")
            return HttpResponse("Please check your input", status=400)


def add_relation_ship(request):
    """
    This is a django view function for creating relationship between 2 person and accepts only post method.
    """
    if request.method == "POST":
        logger.info("CreatePerson | Calling view function add_relation_ship")
        person_1_id = request.POST.get("person_1_id","")
        person_2_id = request.POST.get("person_2_id","")
        r_type = request.POST.get("r_type","")
        print(person_1_id, person_2_id, r_type)
        logger.info("CreatePerson | Calling value of person 1 id, person 2 id and relation type.")
        if person_1_id.strip() != "" and person_2_id.strip() != "" and r_type.strip() != "":
            logger.info("CreatePerson | Value of person 1 id, person 2 id and relation type is present.")
            fam_obj = FamilyTree(logger)

            status, message = fam_obj.add_relation_ship(person_1_id, person_2_id, r_type)
            return HttpResponse(message, status=(200 if status else 400)) 
        
        else:
            logger.error("CreatePerson | Value of person 1 id, person 2 id and relation type is not present.")
            return HttpResponse("Please provide correct request data", status=400)
    

def get_count_of_sons_daughter_wives(request):
    """
    This function is used for returning count or either sons, daughters or wives.
    required query params: parent_id and count_of
    values for count_of are sons, daughters, wives
    return:
        json response if status code is 200 else text data
    """
    logger.info("CreatePerson | Calling view function add_relation_ship")
    
    parent_id = request.GET.get("parent_id","").strip()
    count_of = request.GET.get("count_of","").strip()
    
    logger.info("CreatePerson | Checking value for parent_id and count_of.")
    if parent_id.strip() != "" and count_of.strip() != "" and count_of in ["sons", "daughters", "wives"]:
        fam_obj = FamilyTree(logger)
        count = 0

        if count_of == "sons":
            logger.info("CreatePerson | Calling method get_total_sons_or_daughters for counting sons.")
            count = fam_obj.get_total_sons_or_daughters(parent_id)

        elif count_of == "daughters":
            logger.info("CreatePerson | Calling method get_total_sons_or_daughters for counting daughters.")
            count = fam_obj.get_total_sons_or_daughters(parent_id, False)

        else:
            logger.info("CreatePerson | Calling method get_total_wives for counting wives.")
            count = fam_obj.get_total_wives(parent_id)

        return HttpResponse(json.dumps({"count_of":count_of, "count":count}), status=200, content_type="application/json")

    else:
        logger.error("CreatePerson | value for parent_id and count_of not present")
        return HttpResponse("Please provide correct request params", status=400)

    
def get_father_name(request):
    """
    This function is used for returning father name or the person and uses get request.
    return:
        json response status is 200 else string response
    """
    logger.info("CreatePerson | Calling view function get_father_name")
    son_id = request.GET.get("son_id","").strip()

    logger.info("CreatePerson | Checking value for son_id")
    if son_id != "":
        logger.info("CreatePerson | Calling method get_father_name")
        fam_obj = FamilyTree(logger)
        father_name = fam_obj.get_father_name(son_id)
        
        if father_name:
            logger.info("CreatePerson | Method get_father_name executed with success response")
            return HttpResponse(json.dumps({"father_name":father_name}), status=200, content_type="application/json")
        
        else:
            logger.error("CreatePerson | Method get_father_name executed with failed response")
            return HttpResponse("Father does not exist", status=400)

    else:
        logger.error("CreatePerson | value for son_id not present")
        return HttpResponse("Please provide correct request params", status=400)