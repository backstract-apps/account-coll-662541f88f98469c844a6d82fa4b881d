from sqlalchemy.orm import Session
from typing import List
from fastapi import Request, UploadFile
import models, schemas
import boto3

from pathlib import Path

async def get_employees(db: Session, request: Request):
    header1:str = request.headers.get('header1')


    employees_all = db.query(models.Employees).order_by(models.Employees.id).all()
    res = {
        'employees_all': employees_all,
    }
    return res

async def get_employees_id(db: Session, id: int):

    employees_one = db.query(models.Employees).filter(models.Employees.id == 'id').first()
    res = {
        'employees_one': employees_one,
    }
    return res

async def post_employees(db: Session, account_id: UploadFile):

    record_to_be_added = {'id': id, 'name': name, 'employee_id': employee_id, 'age': age, 'username': username, 'password': password, 'emailid': emailid}
    new_employees = models.Employees(**record_to_be_added)
    db.add(new_employees)
    db.commit()
    db.refresh(new_employees)
    employees_inserted_record = new_employees

    bucket_name = "test_region"
    region_name = "test_secret"
    file_path = "resources"

    s3_client = boto3.client(
        's3',
        aws_access_key_id="test_id",
        aws_secret_access_key="test_secret",
        aws_session_token=None,  # Optional, can be removed if not used
        region_name="test_secret"
    )

    # Read file content
    file_content = await account_id.read()

    name = account_id.filename
    file_path = file_path  + '/' + name
    # Upload the file to S3
    s3_client.put_object(
        Bucket=bucket_name,
        Key=file_path,
        Body=file_content
    )

    # Generate the URL for the uploaded file

    file_type = Path(account_id.filename).suffix
    file_size = 200
    file_url = f"https://{bucket_name}.s3.{region_name}.amazonaws.com/{file_path}"

    uploaded_file_url = file_url
    res = {
        'employees_inserted_record': employees_inserted_record,
    }
    return res

async def put_employees_id(db: Session, raw_data: schemas.PutEmployeesId):
    id:str = raw_data.id
    name:str = raw_data.name
    employee_id:str = raw_data.employee_id
    age:str = raw_data.age
    username:str = raw_data.username
    password:str = raw_data.password
    emailid:str = raw_data.emailid


    employees_edited_record = db.query(models.Employees).filter(models.Employees.id == id).first()
    for key, value in {'id': id, 'name': name, 'employee_id': employee_id, 'age': age, 'username': username, 'password': password, 'emailid': emailid}.items():
          setattr(employees_edited_record, key, value)
    db.commit()
    db.refresh(employees_edited_record)
    employees_edited_record = employees_edited_record

    res = {
        'employees_edited_record': employees_edited_record,
    }
    return res

async def delete_employees_id(db: Session, id: int):

    employees_deleted = None
    record_to_delete = db.query(models.Employees).filter(models.Employees.id == id).first()

    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        employees_deleted = record_to_delete
    res = {
        'employees_deleted': employees_deleted,
    }
    return res

