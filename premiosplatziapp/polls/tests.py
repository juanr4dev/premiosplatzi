import datetime
from urllib import response
from venv import create
from django.urls import reverse
from django.utils import timezone
from django.test import TestCase

from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns false for questions whose pub_date us in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(
            question_text="¿Quién es el mejor Course Director?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_now_questions(self):
        """was_published_recently returns false for questions whose pub_date are now"""
        time = timezone.now()
        future_question = Question(
            question_text="¿Quién es el mejor Course Director?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)

    def test_was_published_recently_with_pass_questions(self):
        """was_published_recently returns false for questions whose pub_date us in the past"""
        time = timezone.now() + datetime.timedelta(days=-2)
        future_question = Question(
            question_text="¿Quién es el mejor Course Director?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


def create_question(question_text, days):
    """Create a Questionand publish in offset days (negative for past)"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """If not question exists -> display appropiate message"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_questions(self):
        create_question("future question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_questions(self):
        question = create_question("past question", -30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [question])

    def test_future_question_and_past_question(self):
        """
        Even if both and future question exist, only past question are displayed
        """
        past_question = create_question("Past question", -30)
        future_question = create_question("Future question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [past_question])

    def test_two_question(self):
        """
        The question index page may display multiple questions
        """
        past_question_1 = create_question("Past question 1", -30)
        past_question_2 = create_question("Past question 2", -20)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [
                                 past_question_2, past_question_1])

    def test_two_future_question(self):
        """
        The question index page may display multiple questions
        """
        create_question("Future question 1", 30)
        create_question("future question 2", 20)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """
        Detail View not available for future questions
        """
        future_question = create_question("Future question 1", 30)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_past_question(self):
        """
        Show detail view for past questions
        """
        past_question = create_question("Past question 1", -30)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)



