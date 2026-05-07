from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import UserProfile
from projects.models import Project
from tasks.models import Task
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for the admin dashboard'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(f'Created admin user: {admin_user.username}')

        # Create manager user
        manager_user, created = User.objects.get_or_create(
            username='manager',
            defaults={
                'email': 'manager@example.com',
                'first_name': 'Manager',
                'last_name': 'User',
                'role': 'manager',
            }
        )
        if created:
            manager_user.set_password('manager123')
            manager_user.save()
            self.stdout.write(f'Created manager user: {manager_user.username}')

        # Create regular user
        regular_user, created = User.objects.get_or_create(
            username='user',
            defaults={
                'email': 'user@example.com',
                'first_name': 'Regular',
                'last_name': 'User',
                'role': 'user',
            }
        )
        if created:
            regular_user.set_password('user123')
            regular_user.save()
            self.stdout.write(f'Created regular user: {regular_user.username}')

        # Create additional users
        for i in range(1, 6):
            user, created = User.objects.get_or_create(
                username=f'user{i}',
                defaults={
                    'email': f'user{i}@example.com',
                    'first_name': f'User',
                    'last_name': f'{i}',
                    'role': 'user',
                }
            )
            if created:
                user.set_password('password123')
                user.save()

        # Create profiles
        for user in User.objects.all():
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'bio': f'This is the bio for {user.get_full_name() or user.username}',
                    'location': 'New York, NY',
                }
            )

        # Create sample projects
        projects_data = [
            {
                'name': 'E-commerce Website',
                'description': 'Building a modern e-commerce platform with Django and React',
                'status': 'active',
                'created_by': manager_user,
            },
            {
                'name': 'Mobile App Development',
                'description': 'Developing a mobile application for iOS and Android',
                'status': 'planning',
                'created_by': manager_user,
            },
            {
                'name': 'Data Analytics Dashboard',
                'description': 'Creating a dashboard for business intelligence and analytics',
                'status': 'completed',
                'created_by': admin_user,
            },
            {
                'name': 'API Integration',
                'description': 'Integrating third-party APIs for payment and shipping',
                'status': 'on_hold',
                'created_by': manager_user,
            },
        ]

        for project_data in projects_data:
            project, created = Project.objects.get_or_create(
                name=project_data['name'],
                defaults=project_data
            )
            if created:
                # Assign some users to the project
                project.assigned_users.add(regular_user)
                if project.name == 'E-commerce Website':
                    project.assigned_users.add(User.objects.get(username='user1'))
                    project.assigned_users.add(User.objects.get(username='user2'))
                self.stdout.write(f'Created project: {project.name}')

        # Create sample tasks
        tasks_data = [
            {
                'title': 'Setup project structure',
                'description': 'Initialize the project with proper folder structure and dependencies',
                'project': Project.objects.get(name='E-commerce Website'),
                'assigned_to': regular_user,
                'created_by': manager_user,
                'priority': 'high',
                'status': 'completed',
            },
            {
                'title': 'Design user authentication',
                'description': 'Implement user registration, login, and authentication system',
                'project': Project.objects.get(name='E-commerce Website'),
                'assigned_to': User.objects.get(username='user1'),
                'created_by': manager_user,
                'priority': 'high',
                'status': 'in_progress',
            },
            {
                'title': 'Create product catalog',
                'description': 'Build the product listing and detail pages',
                'project': Project.objects.get(name='E-commerce Website'),
                'assigned_to': User.objects.get(username='user2'),
                'created_by': manager_user,
                'priority': 'medium',
                'status': 'todo',
            },
            {
                'title': 'Research mobile frameworks',
                'description': 'Evaluate React Native vs Flutter for mobile development',
                'project': Project.objects.get(name='Mobile App Development'),
                'assigned_to': regular_user,
                'created_by': manager_user,
                'priority': 'medium',
                'status': 'in_progress',
            },
            {
                'title': 'Create wireframes',
                'description': 'Design app wireframes and user flow',
                'project': Project.objects.get(name='Mobile App Development'),
                'assigned_to': User.objects.get(username='user3'),
                'created_by': manager_user,
                'priority': 'low',
                'status': 'todo',
            },
        ]

        for task_data in tasks_data:
            task, created = Task.objects.get_or_create(
                title=task_data['title'],
                project=task_data['project'],
                defaults=task_data
            )
            if created:
                # Set due dates
                task.due_date = timezone.now() + timedelta(days=7)
                task.save()
                self.stdout.write(f'Created task: {task.title}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
        self.stdout.write('\nDemo accounts:')
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('Manager: manager / manager123')
        self.stdout.write('User: user / user123')
