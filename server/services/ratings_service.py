from data.database import insert_query, read_query
from data.models import Vote


def vote(vote:Vote, student_id:int):
    insert_query('INSERT INTO ratings (courses_id, students_id, rating) VALUES (?, ?, ?)', 
                (vote.course_id, student_id, vote.rating))
    

def check_if_student_had_vote(course_id:int, student_id:int):
    return any(read_query('''select courses_id, students_id
                from ratings
                where courses_id=? and students_id=?''', (course_id, student_id)))

def average_rating(course_id):
    data = read_query('''select Round(sum(rating)/count(rating)*10/10,1) as average_score
                    from ratings
                    where courses_id = 1''')
    
    return data[0][0]