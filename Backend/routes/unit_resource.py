from flask import Flask, request
from flask_restful import Resource
from models.unit import Unit
from flask_login import login_required
from models import db
from sqlalchemy.exc import SQLAlchemyError

class UnitResource(Resource):
    def get(self,id):
        unit=db.session.query(Unit).filter(Unit.id==id).first()
        if not unit:
            return {"error":"Unit not found"},404
        return{
            "message":"Unit Found",
            "id":unit.id,
            "title":unit.title,
            "description":unit.description
        },200
    
    def post(self):
        data=request.get_json(force=True)
        title=data.get("title")
        description=data.get("description")
        try:
            check_by_title=db.session.query(Unit).filter(Unit.title==title).first()
            if check_by_title:
                return {"error":"Title Already Exist"},400
            new_unit=Unit(title=title,description=description)
            db.session.add(new_unit)
            db.session.commit()
            return {"message":"Unit added Succesfully"},201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Internal Server Error", "details": str(e)}, 500
    
    def put(self,id):
        data=request.get_json(force=True)
        title=data.get("title")
        description=data.get("description")
        check_title=db.session.query(Unit).filter(Unit.id!=id,Unit.title==title).first()
        if check_title:
            return {"error":"Title already Exist"},400
    
        unit=db.session.query(Unit).filter(Unit.id==id).first()
        if not unit:
            return {"error":"Unit not found"},404
        try:
            unit.title =title
            unit.description=description
            db.session.commit()
            return {
                "message":"Unit Updated Succesfully",
                "title":title,
                "description":description
            },200

        except:
            return {"error":"Internal Server Error"},500
    
    def delete(self,id):
        try:
            unit=db.session.query(Unit).filter(Unit.id==id).first()
            if not unit:
                return {"error":"No such unit"}
            db.session.delete(unit)
            db.session.commit()
            return {"message":"Unit Deleted Successfully"},200
        except:
            return {"error":"Internal Server Error"},500  