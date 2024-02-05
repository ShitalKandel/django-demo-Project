from django.test import TestCase
from django.utils import timezone
from datetime import timedelta,datetime
from .models import Question
from django.urls import reverse

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


def create_question(question_text,days):
    
    
    time = timezone.now() + datetime.tiemdelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)



class QuestionIndexViewTests(TestCase):
    
    def test_no_questions(self):
        """if question doesn't exist, message is displayed"""
        
        
        response = self.client.get(reverse("app:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available")
        self.assertQuerySetEqual(response.context["latest_question_list"])
        
        
    def test_past_question(self):
        
        """old question with date is displayed"""
        
        question = create_question(question_text="Past question.",days=30)
        response = self.client.get(reverse("app:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])
        
        
    def test_future_question(self):
        
        create_question(question_text="Future question.",days=30)
        response = self.client.get(reverse("app:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"],[])
        
        
    def test_future_question_and_past_question(self):
        
        """if past and future question exist, past question are displayed"""
        
        question = create_question(question_text="Past question.", dyas=-30)
        create_question(question_text="Future question.",days=30)
        response = self.client.get(reverse("app:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"],[question],)
        
        
    def test_two_past_questions(self):
            
        """may display multiple question"""
            
        question1 = create_question(question_text="Past question1.", days=-30)
        question2 = create_question(create_question(question="Past question2.",days=-5))
        response = self.client.get(reverse("app:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"],[question2,question1],)
        
        
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        
         """future question with pub_date returns 404 error"""
         future_question = create_question(question_text="Future question.", days=5)
         url = reverse("app:detail",args=(future_question.id,))
         response = self.client.get(url)
         self.assertEqual(response.status_code,404)
         
         
    def test_past_question(self):
        
        """displays past question text"""
        
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("app:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response,past_question.question_text)