# user/management/commands/create_initial_skills.py
from django.core.management.base import BaseCommand
from user.models import Skill

class Command(BaseCommand):
    help = 'Create initial skills data'

    def handle(self, *args, **options):
        skills_data = [
            # Programming Skills
            {'name': 'JavaScript', 'category': 'programming', 'icon_class': 'fab fa-js-square', 'color_class': 'text-yellow-500'},
            {'name': 'Python', 'category': 'programming', 'icon_class': 'fab fa-python', 'color_class': 'text-blue-500'},
            {'name': 'React', 'category': 'programming', 'icon_class': 'fab fa-react', 'color_class': 'text-blue-500'},
            {'name': 'CSS', 'category': 'programming', 'icon_class': 'fab fa-css3-alt', 'color_class': 'text-blue-600'},
            {'name': 'HTML', 'category': 'programming', 'icon_class': 'fab fa-html5', 'color_class': 'text-orange-500'},
            {'name': 'Node.js', 'category': 'programming', 'icon_class': 'fab fa-node-js', 'color_class': 'text-green-500'},
            {'name': 'Django', 'category': 'programming', 'icon_class': 'fas fa-code', 'color_class': 'text-green-600'},
            {'name': 'Java', 'category': 'programming', 'icon_class': 'fab fa-java', 'color_class': 'text-red-500'},
            {'name': 'C++', 'category': 'programming', 'icon_class': 'fas fa-code', 'color_class': 'text-blue-700'},
            
            # Design Skills
            {'name': 'Photoshop', 'category': 'design', 'icon_class': 'fas fa-paint-brush', 'color_class': 'text-blue-600'},
            {'name': 'UI/UX Design', 'category': 'design', 'icon_class': 'fas fa-pencil-ruler', 'color_class': 'text-purple-500'},
            {'name': 'Figma', 'category': 'design', 'icon_class': 'fas fa-vector-square', 'color_class': 'text-purple-600'},
            {'name': 'Illustrator', 'category': 'design', 'icon_class': 'fas fa-bezier-curve', 'color_class': 'text-orange-600'},
            
            # Languages
            {'name': 'Spanish', 'category': 'language', 'icon_class': 'fas fa-language', 'color_class': 'text-green-500'},
            {'name': 'French', 'category': 'language', 'icon_class': 'fas fa-language', 'color_class': 'text-blue-500'},
            {'name': 'German', 'category': 'language', 'icon_class': 'fas fa-language', 'color_class': 'text-red-500'},
            {'name': 'Mandarin', 'category': 'language', 'icon_class': 'fas fa-language', 'color_class': 'text-yellow-600'},
            
            # Creative Skills
            {'name': 'Photography', 'category': 'photography', 'icon_class': 'fas fa-camera', 'color_class': 'text-purple-500'},
            {'name': 'Video Editing', 'category': 'photography', 'icon_class': 'fas fa-video', 'color_class': 'text-red-600'},
            {'name': 'Music Production', 'category': 'music', 'icon_class': 'fas fa-music', 'color_class': 'text-pink-500'},
            {'name': 'Guitar', 'category': 'music', 'icon_class': 'fas fa-guitar', 'color_class': 'text-brown-500'},
            {'name': 'Piano', 'category': 'music', 'icon_class': 'fas fa-piano', 'color_class': 'text-gray-700'},
            
            # Other Skills
            {'name': 'Data Science', 'category': 'other', 'icon_class': 'fas fa-chart-line', 'color_class': 'text-indigo-500'},
            {'name': 'Machine Learning', 'category': 'other', 'icon_class': 'fas fa-robot', 'color_class': 'text-cyan-500'},
            {'name': 'Digital Marketing', 'category': 'other', 'icon_class': 'fas fa-bullhorn', 'color_class': 'text-orange-500'},
            {'name': 'Project Management', 'category': 'other', 'icon_class': 'fas fa-tasks', 'color_class': 'text-green-600'},
            {'name': 'Public Speaking', 'category': 'other', 'icon_class': 'fas fa-microphone', 'color_class': 'text-purple-600'},
            {'name': 'Writing', 'category': 'other', 'icon_class': 'fas fa-pen', 'color_class': 'text-blue-600'},
            {'name': 'Cooking', 'category': 'other', 'icon_class': 'fas fa-utensils', 'color_class': 'text-red-500'},
        ]
        
        created_count = 0
        for skill_data in skills_data:
            skill, created = Skill.objects.get_or_create(
                name=skill_data['name'],
                defaults=skill_data
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created skill: {skill.name}")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} skills')
        )