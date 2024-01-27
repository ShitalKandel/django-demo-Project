from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import Question

class QuestionModelTests(TestCase):
    
    #test was published with future question
    def test_published_w_f_q(self):
        
        time = timezone.now() + timezone.timedelta(days=30)
        future_question = Question(pub_date=time)
        
        # assert that was_published_recently() returns False for future questions
        self.assertIs(future_question.was_published_recently(),False)
        
    #test was published recently with old question
    def test_published_old_question(self):
        
        time = timezone.now() - timedelta(days=1 , seconds=1)
        old_question = Question(pub_date=time)
        self.asserIs(old_question.was_published_recently(),False)
        
     
     #test was published recently with recent question   
    def test_was_published_recent_question(self):
        time = timezone.now() - timedelta(hours=23 , minutes = 59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(),True)
