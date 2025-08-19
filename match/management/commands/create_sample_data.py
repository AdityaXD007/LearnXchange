# management/commands/create_sample_data.py
# Create this file in: your_app/management/commands/create_sample_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from user.models import Profile, Skill, UserSkill 
import random

class Command(BaseCommand):
    help = 'Create sample data for testing the matching system'
    
    def handle(self, *args, **options):
        self.stdout.write('Creating sample skills...')
        self.create_skills()
        
        self.stdout.write('Creating sample users and profiles...')
        self.create_users_and_profiles()
        
        self.stdout.write('Creating sample user skills...')
        self.create_user_skills()
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
    
    def create_skills(self):
        skills_data = [
            ('JavaScript', 'programming', 'fab fa-js', 'text-yellow-600'),
            ('Python', 'programming', 'fab fa-python', 'text-blue-600'),
            ('React', 'programming', 'fab fa-react', 'text-blue-400'),
            ('Node.js', 'programming', 'fab fa-node-js', 'text-green-600'),
            ('CSS', 'programming', 'fab fa-css3', 'text-blue-500'),
            ('HTML', 'programming', 'fab fa-html5', 'text-orange-600'),
            ('Photography', 'photography', 'fas fa-camera', 'text-gray-600'),
            ('Lightroom', 'photography', 'fas fa-adjust', 'text-purple-600'),
            ('Photoshop', 'design', 'fas fa-magic', 'text-blue-600'),
            ('UI/UX Design', 'design', 'fas fa-paint-brush', 'text-pink-600'),
            ('Spanish', 'language', 'fas fa-language', 'text-red-600'),
            ('French', 'language', 'fas fa-language', 'text-blue-600'),
            ('Guitar', 'music', 'fas fa-guitar', 'text-amber-600'),
            ('Piano', 'music', 'fas fa-music', 'text-purple-600'),
            ('Digital Marketing', 'other', 'fas fa-bullhorn', 'text-green-600'),
            ('Data Science', 'programming', 'fas fa-chart-bar', 'text-indigo-600'),
        ]
        
        for name, category, icon, color in skills_data:
            skill, created = Skill.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'icon_class': icon,
                    'color_class': color
                }
            )
            if created:
                self.stdout.write(f'  Created skill: {name}')
    
    def create_users_and_profiles(self):
        users_data = [
            {
                'username': 'sarah_chen',
                'email': 'sarah@example.com',
                'full_name': 'Sarah Chen',
                'bio': 'Senior frontend developer specializing in React and modern JavaScript. Looking to learn Python for backend development.',
                'location': 'San Francisco, CA',
                'rating': 4.9
            },
            {
                'username': 'david_park',
                'email': 'david@example.com',
                'full_name': 'David Park',
                'bio': 'Professional photographer and visual designer. Interested in learning web development to create interactive portfolios.',
                'location': 'Los Angeles, CA',
                'rating': 4.6
            },
            {
                'username': 'maria_rodriguez',
                'email': 'maria@example.com',
                'full_name': 'Maria Rodriguez',
                'bio': 'Native Spanish speaker and language teacher. Also skilled in digital marketing. Looking to improve coding skills for career transition.',
                'location': 'Austin, TX',
                'rating': 4.8
            },
            {
                'username': 'alex_johnson',
                'email': 'alex@example.com',
                'full_name': 'Alex Johnson',
                'bio': 'Full-stack developer with expertise in Python and Node.js. Passionate about teaching and helping others learn to code.',
                'location': 'Seattle, WA',
                'rating': 4.7
            },
            {
                'username': 'emma_davis',
                'email': 'emma@example.com',
                'full_name': 'Emma Davis',
                'bio': 'UX/UI designer with a background in psychology. Love creating user-friendly interfaces and teaching design principles.',
                'location': 'New York, NY',
                'rating': 4.5
            },
            {
                'username': 'carlos_martinez',
                'email': 'carlos@example.com',
                'full_name': 'Carlos Martinez',
                'bio': 'Data scientist and Python enthusiast. Always eager to learn new technologies and share knowledge about data analysis.',
                'location': 'Miami, FL',
                'rating': 4.4
            }
        ]
        
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['full_name'].split()[0],
                    'last_name': ' '.join(user_data['full_name'].split()[1:])
                }
            )
            
            if created:
                profile = Profile.objects.create(
                    user=user,
                    full_name=user_data['full_name'],
                    bio=user_data['bio'],
                    location=user_data['location'],
                    rating=user_data['rating'],
                    sessions=random.randint(5, 50)
                )
                self.stdout.write(f'  Created user and profile: {user_data["username"]}')
    
    def create_user_skills(self):
        # Define skills for each user
        user_skills_mapping = {
            'sarah_chen': {
                'teaching': [('JavaScript', 'expert'), ('React', 'expert'), ('CSS', 'advanced')],
                'learning': [('Python', 'beginner'), ('Node.js', 'intermediate')]
            },
            'david_park': {
                'teaching': [('Photography', 'expert'), ('Lightroom', 'advanced'), ('Photoshop', 'advanced')],
                'learning': [('HTML', 'beginner'), ('CSS', 'beginner'), ('JavaScript', 'beginner')]
            },
            'maria_rodriguez': {
                'teaching': [('Spanish', 'expert'), ('Digital Marketing', 'advanced')],
                'learning': [('JavaScript', 'intermediate'), ('Python', 'beginner')]
            },
            'alex_johnson': {
                'teaching': [('Python', 'expert'), ('Node.js', 'expert'), ('JavaScript', 'advanced')],
                'learning': [('UI/UX Design', 'beginner'), ('Photography', 'intermediate')]
            },
            'emma_davis': {
                'teaching': [('UI/UX Design', 'expert'), ('Photoshop', 'advanced')],
                'learning': [('React', 'intermediate'), ('JavaScript', 'intermediate')]
            },
            'carlos_martinez': {
                'teaching': [('Python', 'expert'), ('Data Science', 'expert')],
                'learning': [('JavaScript', 'intermediate'), ('React', 'beginner')]
            }
        }
        
        for username, skills_data in user_skills_mapping.items():
            try:
                user = User.objects.get(username=username)
                
                # Create teaching skills
                for skill_name, proficiency in skills_data['teaching']:
                    try:
                        skill = Skill.objects.get(name=skill_name)
                        user_skill, created = UserSkill.objects.get_or_create(
                            user=user,
                            skill=skill,
                            skill_type='teaching',
                            defaults={
                                'proficiency_level': proficiency,
                                'status': 'active',
                                'sessions_count': random.randint(1, 20)
                            }
                        )
                        if created:
                            self.stdout.write(f'    {username} teaches {skill_name}')
                    except Skill.DoesNotExist:
                        self.stdout.write(f'    Skill not found: {skill_name}')
                
                # Create learning skills
                for skill_name, proficiency in skills_data['learning']:
                    try:
                        skill = Skill.objects.get(name=skill_name)
                        user_skill, created = UserSkill.objects.get_or_create(
                            user=user,
                            skill=skill,
                            skill_type='learning',
                            defaults={
                                'proficiency_level': proficiency,
                                'status': 'learning',
                                'sessions_count': random.randint(0, 5)
                            }
                        )
                        if created:
                            self.stdout.write(f'    {username} wants to learn {skill_name}')
                    except Skill.DoesNotExist:
                        self.stdout.write(f'    Skill not found: {skill_name}')
                        
            except User.DoesNotExist:
                self.stdout.write(f'    User not found: {username}')


