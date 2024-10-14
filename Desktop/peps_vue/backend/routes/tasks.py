from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from database.connection import Tasks, db, User

from config import cfg

import json

# Экземпляр APIRouter
router = APIRouter()
router_key = "/api/tasks"

async def taskCreates():
    '''
        Create Task in Database
    '''
    try:
        tasks_json = {}
        
        try:
            with open('./../tasksArray.json', 'r', encoding='utf-8') as json_file:
                tasks_json = json.load(json_file)
                
        except Exception as e:
            print(e)
        
        if tasks_json:
            Tasks.clear()
            for key, value in tasks_json.items():
                db.add(Tasks(
                    task_name = value['task_name'],
                    task_name_ru = value['task_name_ru'],
                    task_type = value['task_type'],
                    task_photo = value['task_photo'],
                    task_redirect = value['task_redirect'],
                    task_gift_type = value['task_gift_type'],
                    task_gift = value['task_gift']
                ))

        db.flush()
        db.commit()

        return { 'success': True }
    
    except Exception as e:
        print(e)
        return { 'success': False }


@router.get('{}/create'.format(router_key))
async def task_create(request: Request):
    '''
        Create Task in Database
    '''
    try:
        data = dict(request.query_params)

        secret_key = data.get('key')
        task_name = data.get('task_name')
        task_name_ru = data.get('task_name_ru')
        task_type = data.get('task_type')
        task_photo = data.get('task_photo')
        task_redirect = data.get('task_redirect')
        task_gift_type = data.get('task_gift_type')
        task_gift = data.get('task_gift')
        
        if secret_key == cfg.get('SECRET_KEY'):
            db.add(Tasks(
                task_name = task_name,
                task_name_ru = task_name_ru,
                task_type = task_type,
                task_photo = task_photo,
                task_redirect = task_redirect,
                task_gift_type = task_gift_type,
                task_gift = task_gift
            ))

            db.flush()
            db.commit()

            return JSONResponse({ 'success': True, 'data': { 'task_name': task_name } })
        else:
            return JSONResponse({ 'success': False, 'error': 'wrong key' })
    
    except Exception as e:
        print(e)
        return JSONResponse({ 'success': False, 'error': str(e) })


@router.get('{}/get'.format(router_key))
async def tasks_get(request: Request):
    try:
        params = dict(request.query_params)
        secret_key = params.get('key')
        user_id = params.get('user_id', None)

        if secret_key == cfg.get('SECRET_KEY'):
            tasks = Tasks.get_tasks(user_id)

            # Фильтрация и сортировка задач
            filtered_tasks = []
            if tasks:
                filtered_tasks = sorted(
                    tasks,
                    key=lambda task: (
                        task['completed'] is True,       # Сначала не завершенные задачи
                        task['task_progress'] is False   # Затем задачи с task_progress == False
                    )
                )

            return JSONResponse({'success': True, 'tasks': filtered_tasks})
        else:
            return JSONResponse({'success': False, 'error': 'wrong key'})
    except Exception as e:
        print(e)
        return JSONResponse({'success': False, 'error': str(e)})


@router.get('{}/getTask'.format(router_key))
async def task_get(request: Request):
    try:
        params = dict(request.query_params)
        secret_key = params.get('key')
        
        if secret_key == cfg.get('SECRET_KEY'):
            if 'task_id' in params:
                task_id = params.get('task_id')
                user_id = params.get('user_id')

                task = db.query(Tasks).filter(Tasks.id == task_id).first()
                task.start_task(user_id)
                
                if task:
                    return JSONResponse({'success': True, 'task': task.as_dict()})
                else:
                    return JSONResponse({'success': False, 'error': 'task not found'})
            else:
                return JSONResponse({'success': False, 'error': 'task_id not found'})
        else:
            return JSONResponse({'success': False, 'error': 'wrong key'})
        
    except Exception as e:
        print(e)
        return JSONResponse({'success': False, 'error': str(e)})

@router.get('{}/task/nextStep'.format(router_key))
async def get_next_step(request: Request):
    try:
        params = dict(request.query_params)
        
        secret_key = params.get('key')
        task_id = params.get('task_id')
        user_id = params.get('user_id')

        if secret_key == cfg.get('SECRET_KEY'):
            task = db.query(Tasks).filter(Tasks.id == task_id).first()
            result = task.next_step(user_id)

            status = 'in_proccess'
            
            if result is True:
                status = "completed"
            
            return JSONResponse({'success': True, 'task_status': status, 'task': task.get_current_progress(user_id)})
        else:
            return JSONResponse({'success': False, 'error': 'wrong key'})
        
    except Exception as e:
        print(e)
        return JSONResponse({'success': False, 'error': str(e)})

@router.get('{}/task/endTask'.format(router_key))
async def endTask(request: Request):
    try:
        params = dict(request.query_params)
        
        secret_key = params.get('key')
        task_id = params.get('task_id')
        user_id = params.get('user_id')
        views = params.get('views')
        earn = params.get('earn')
        ton = params.get('ton')
        
        if secret_key == cfg.get('SECRET_KEY'):
            user = db.query(User).filter(User.user_id == user_id).first()

            if str(task_id) != 'story':
                task = db.query(Tasks).filter(Tasks.id == task_id).first()
                task.end_task(
                    user_id,
                    views,
                    earn,
                    ton
                )
            else:
                user.task_story = True
                
                user.views_balance = views
                user.earn_balance = earn
                user.ton_balance = ton
                
                db.commit()
            
            return JSONResponse({'success': True, 'balances': {'views': user.views_balance, 'earn': user.earn_balance, 'ton': user.ton_balance}})
        else:
            return JSONResponse({'success': False, 'error': 'wrong key'})
    
    except Exception as e:
        print(e)
        return JSONResponse({'success': False, 'error': str(e)})


