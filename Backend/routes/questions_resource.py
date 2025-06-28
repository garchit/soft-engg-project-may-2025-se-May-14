from models.questions import Question
from models import db
from flask_restful import Resource
from flask import request
from models.unit import Unit
from sqlalchemy.exc import SQLAlchemyError

class QuestionResource(Resource):
    def get(self,id):
        try:
            question=db.session.query(Question).filter(Question.id==id).first()
            
            if question:
                return {"message":"Question fetched Successfully",
                        "id":question.id,
                        "unit_id":question.unit_id,
                        "description":question.description,
                        "option_a":question.option_a,
                        "option_b":question.option_b,
                        "option_c":question.option_c,
                        "option_d":question.option_d,
                        "correct_option":question.correct_option
                        },200   
        except SQLAlchemyError as e:
            db.session.rollback()        
            return {"error":"Internal Server Error","details":str(e)},500

    def post(self):
        data=request.get_json(force=True)
        unit_id=data.get("unit_id")
        description=data.get("description")
        marks=data.get("marks")
        option_a=data.get("option_a")
        option_b=data.get("option_b")
        option_c=data.get("option_c")
        option_d=data.get("option_d")
        correct_option=data.get("correct_option")
        required_fields=[unit_id,description,option_a,option_b,option_c,option_d,correct_option]
        list_correct_option=["a","b","c","d"]

        check_unit=db.session.query(Unit).filter(Unit.id==unit_id).first()
        if not check_unit:
            return {"error":"No such Unit"},404
        
        for fields in required_fields:
            if not fields:
                return {"error":"Required Fields missing"},401
            
        if correct_option not in list_correct_option:
            return {"error":"values of correct option must be a,b,c or d"},400
         
        try:

            if marks is None:
                marks=1
            question=Question(unit_id=unit_id,description=description,marks=marks,option_a=option_a,
                                option_b=option_b,option_c=option_c,
                                option_d=option_d,correct_option=correct_option)
            db.session.add(question)
            db.session.commit()
            return {"message":"Question added Successfully"},201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Internal Server Error", "details": str(e)}, 500

    def put(self,id):
        data=request.get_json(force=True)
        unit_id=data.get("unit_id")
        description=data.get("description")
        marks=data.get("marks")
        option_a=data.get("option_a")
        option_b=data.get("option_b")
        option_c=data.get("option_c")
        option_d=data.get("option_d")
        correct_option=data.get("correct_option")
        required_fields=[unit_id,description,option_a,option_b,option_c,option_d,correct_option]
        list_correct_option=["a","b","c","d"]

        check_unit=db.session.query(Unit).filter(Unit.id==unit_id).first()
        if not check_unit:
            return {"error":"No such Unit"},404
        
        for fields in required_fields:
            if not fields:
                return {"error":"Required Fields missing"},401
            
        if correct_option not in list_correct_option:
            return {"error":"values of correct option must be a,b,c or d"},400
        
        if marks is None:
                marks=1
     
        try:        
            question=db.session.query(Question).filter(Question.id==id).first()
            if not question:
                return {"error":"question not found"},404
            question.description=description
            question.unit_id=unit_id
            question.correct_option=correct_option
            question.option_a=option_a
            question.option_b=option_b
            question.option_c=option_c
            question.option_d=option_d
            question.marks=marks
            db.session.commit()
            return {"message":"Question updated Sucessfully"},200   

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Internal Server Error", "details": str(e)}, 500

    def delete(self,id):
        try:
            question=db.session.query(Question).filter(Question.id==id).first()
            if not question:
                return {"error":"Question not found"},404
            db.session.delete(question)
            db.session.commit()
            return {"message":"Question Deleted Succefully"},200
        
        except SQLAlchemyError as e:
            return {"error":"Internal Server Error","details":str(e)},500

        