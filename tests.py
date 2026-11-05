import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_add_multiple_choices():
    question = Question(title='q1')

    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    choice3 = question.add_choice('c')

    assert len(question.choices) == 3
    assert [c.text for c in question.choices] == ['a', 'b', 'c']


def test_choice_ids_are_sequential():
    question = Question(title='q1')

    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    choice3 = question.add_choice('c')

    assert choice1.id == 1
    assert choice2.id == 2
    assert choice3.id == 3


def test_add_choice_with_empty_text():
    question = Question(title='q1')

    with pytest.raises(Exception, match='Text cannot be empty'):
        question.add_choice('')


def test_add_choice_with_text_longer_than_100_characters():
    question = Question(title='q1')

    with pytest.raises(Exception, match='Text cannot be longer than 100 characters'):
        question.add_choice('a' * 101)


def test_remove_choice_by_id():
    question = Question(title='q1')

    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')

    question.remove_choice_by_id(choice1.id)

    assert len(question.choices) == 1
    assert question.choices[0] == choice2


def test_remove_nonexistent_choice():
    question = Question(title='q1')
    question.add_choice('a')

    with pytest.raises(Exception, match='Invalid choice id'):
        question.remove_choice_by_id(999)


def test_remove_all_choices():
    question = Question(title='q1')

    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')

    question.remove_all_choices()

    assert question.choices == []


def test_set_correct_choices():
    question = Question(title='q1')

    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    choice3 = question.add_choice('c')

    question.set_correct_choices([choice1.id, choice3.id])

    assert choice1.is_correct
    assert not choice2.is_correct
    assert choice3.is_correct


def test_correct_selected_choices():
    question = Question(title='q1', max_selections=2)

    choice1 = question.add_choice('a', is_correct=True)
    choice2 = question.add_choice('b')
    choice3 = question.add_choice('c', is_correct=True)

    result = question.correct_selected_choices([
        choice1.id,
        choice3.id
    ])

    assert result == [choice1.id, choice3.id]


def test_correct_selected_choices_exceed_max_selections():
    question = Question(title='q1', max_selections=2)

    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    choice3 = question.add_choice('c')

    with pytest.raises(Exception, match='Cannot select more than 2 choices'):
        question.correct_selected_choices([
            choice1.id,
            choice2.id,
            choice3.id
        ])