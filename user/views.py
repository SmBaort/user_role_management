from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Role, User
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import transaction


def create_user(data):
    try:
        # Validate required fields
        required_fields = ['firstName', 'lastName', 'email', 'password']
        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Validate email
        try:
            validate_email(data['email'])
        except ValidationError:
            return JsonResponse({'error': 'Invalid email address'}, status=400)

        # Check if email already exists
        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({'error': 'Email already registered'}, status=400)        

        if 'password' in data:
                data['password'] = make_password(data['password'])      

        if 'role' in data:
            try:
                data['role'] = Role.objects.get(id=data['role'])
            except Role.DoesNotExist:
                return JsonResponse({'error': 'Invalid Role ID'}, status=400)

        user = User.objects.create(**data)
        return JsonResponse({'id': user.id, 'email': user.email}, status=201)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class RoleListView(View):
    def get(self, request):
        try:
            search = request.GET.get('search', '')
            roles = Role.objects.filter(
                Q(roleName__icontains=search) | 
                Q(accessModules__icontains=search)
            ).values('id', 'roleName', 'accessModules', 'createdAt', 'active')
            return JsonResponse(list(roles), safe=False, status=200)
        except Exception as e:
            return JsonResponse({'message': str(e),}, status=400)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if 'accessModules' in data:
                data['accessModules'] = list(set(data['accessModules']))
            role = Role.objects.create(**data)
            return JsonResponse({'id': role.id, 'roleName': role.roleName}, status=200)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class RoleDetailView(View):
    def get(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
            return JsonResponse({'id': role.id, 'roleName': role.roleName, 'accessModules': role.accessModules, 'active': role.active}, status=200)
        except Role.DoesNotExist:
            return JsonResponse({'error': 'Role not found for the RoleID: ' + str(pk)}, status=404)

    def put(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
            data = json.loads(request.body)
            if 'accessModules' in data:
                data['accessModules'] = list(set(data['accessModules']))
            for key, value in data.items():
                setattr(role, key, value)
            role.save()
            return JsonResponse({'id': role.id, 'roleName': role.roleName, 'accessModules': role.accessModules, 'active': role.active}, status=200)
        except Role.DoesNotExist:
            return JsonResponse({'error': 'Role not found for the RoleID: ' + str(pk)}, status=404)

    def delete(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
            role.delete()
            return JsonResponse({'message': 'Role deleted successfully'}, status=200)
        except Role.DoesNotExist:
            return JsonResponse({'error': 'Role not found for the RoleID: ' + str(pk)}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(View):
    def get(self, request):
        try:
            search = request.GET.get('search', '')
            users = User.objects.filter(
                Q(firstName__icontains=search) | 
                Q(lastName__icontains=search) | 
                Q(email__icontains=search) |
                Q(role__roleName__icontains=search) |
                Q(role__accessModules__icontains=search)
            ).values('id', 'email', 'firstName', 'lastName', 'role__roleName', 'role__accessModules', 'createdAt', 'active')
            return JsonResponse(list(users), safe=False, status=200)
        except Exception as e:
            return JsonResponse({'message': str(e),}, status=400)

    def post(self, request):
        try:
            data = json.loads(request.body)
            return create_user(data)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)            


@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(View):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            return JsonResponse({
                'id': user.id,
                'email': user.email,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'role': user.role.roleName if user.role else None,
                'accessModules': user.role.accessModules if user.role else None
            })
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            data = json.loads(request.body)
            
            for key, value in data.items():
                if key == 'password':
                    user.password = make_password(value)
                elif key == 'role':
                    try:
                        user.role = Role.objects.get(id=value)
                    except Role.DoesNotExist:
                        return JsonResponse({'error': 'Invalid role ID'}, status=400)
                else:
                    setattr(user, key, value)
            
            user.save()
            
            return JsonResponse({
                'id': user.id,
                'email': user.email,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'role': user.role.roleName if user.role else None
            })
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            return create_user(data)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        # Validate required fields
        if 'email' not in data or 'password' not in data:
            return JsonResponse({'error': 'Email and password are required'}, status=400)
        
        user = User.objects.get(email=data['email'])
        if check_password(data['password'], user.password):
                return JsonResponse({
                    'id': user.id,
                    'email': user.email
                })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class AccessModuleView(View):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            module = request.GET.get('module')
            if not module:
                return JsonResponse({'error': 'Module name is required'}, status=400)
            has_access = module in user.role.accessModules if user.role else False
            return JsonResponse({'has_access': has_access})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def put(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
            data = json.loads(request.body)            
            
            new_modules = data['modules']
            if not isinstance(new_modules, list):
                return JsonResponse({'error': 'Modules must be a list'}, status=400)
            
            # Update access modules ensuring uniqueness
            role.accessModules = list(set(role.accessModules + new_modules))
            role.save()
            return JsonResponse({'id': role.id, 'roleName': role.roleName, 'accessModules': role.accessModules, 'active': role.active}, status=200)
        except Role.DoesNotExist:
            return JsonResponse({'error': 'Role not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def delete(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
            data = json.loads(request.body)
            module = data['module']        
            # Remove the module if it exists
            if module in role.accessModules:
                role.accessModules.remove(module)
                role.save()
                message = f"Module '{module}' removed successfully"
            else:
                message = f"Module '{module}' not found in access modules"            
            return JsonResponse({'id': role.id, 'roleName': role.roleName, 'accessModules': role.accessModules, 'message': message}, status=200)            
        except Role.DoesNotExist:
            return JsonResponse({'error': 'Role not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class BulkUserUpdateView(View):
    def put(self, request):
        try:
            data = json.loads(request.body)
            type = data.get('type')
            
            if type == 'same_data':
                return self.update_users_same_data(data)
            elif type == 'different_data':
                return self.update_users_different_data(data)
            else:
                return JsonResponse({'error': 'Invalid update_type'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def update_users_same_data(self, data):
        user_ids = data.get('user_ids', [])
        update_data = data.get('update_data', {})
        print(user_ids)
        print(update_data)
        
        if not user_ids or not update_data:
            return JsonResponse({'error': 'user_ids and update_data are required'}, status=400)
        
        try:
            with transaction.atomic():
                updated_count = User.objects.filter(id__in=user_ids).update(**update_data)
            
            return JsonResponse({
                'message': f'Successfully updated {updated_count} users',
                'updated_count': updated_count
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def update_users_different_data(self, data):
        user_updates = data.get('user_updates', [])
        
        if not user_updates:
            return JsonResponse({'error': 'user_updates is required'}, status=400)
        
        updated_users = []
        errors = []
        
        try:
            with transaction.atomic():
                for update in user_updates:
                    user_id = update.get('id')
                    update_data = update.get('data', {})
                    
                    if not user_id or not update_data:
                        errors.append(f"Invalid update data for user {user_id}")
                        continue
                    
                    try:
                        user = User.objects.get(id=user_id)
                        for key, value in update_data.items():
                            setattr(user, key, value)
                        user.save()
                        updated_users.append(user_id)
                    except User.DoesNotExist:
                        errors.append(f"User with id {user_id} not found")
                    except Exception as e:
                        errors.append(f"Error updating user {user_id}: {str(e)}")
            
            return JsonResponse({
                'message': f'Updated {len(updated_users)} users',
                'updated_users': updated_users,
                'errors': errors
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
