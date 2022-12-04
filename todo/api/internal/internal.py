from fastapi import APIRouter

internal_router = APIRouter()


@internal_router.get('/')
async def get_company_name():
    return {'company_name': 'My Company'}


@internal_router.get('/employees')
async def number_of_employees():
    return {'company_name': 'My Company', 'number_of_employees': 1000}
