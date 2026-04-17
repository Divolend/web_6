import uuid

from app import app
from models import db, User, Course, Image, Review


def seed():
    with app.app_context():
        admin = db.session.execute(db.select(User).filter_by(login='user')).scalar()
        if not admin:
            admin = User(first_name='Иван', last_name='Иванов', middle_name='Иванович', login='user')
            admin.set_password('Qwerty123')
            db.session.add(admin)
            db.session.flush()

        img = db.session.execute(db.select(Image).filter_by(md5_hash='placeholder-hash')).scalar()
        if not img:
            img = Image(
                id=str(uuid.uuid4()),
                file_name='placeholder.png',
                mime_type='image/png',
                md5_hash='placeholder-hash',
            )
            db.session.add(img)
            db.session.flush()

        course = db.session.execute(db.select(Course)).scalar()
        if not course:
            course = Course(
                name='Основы Python',
                short_desc='Базовый курс программирования на Python для начинающих',
                full_desc='Курс охватывает основы синтаксиса Python, работу с типами данных, условные операторы, циклы, функции, работу с файлами и модулями.',
                category_id=1,
                author_id=admin.id,
                background_image_id=img.id,
            )
            db.session.add(course)
            db.session.flush()

        test_reviews = [
            ('petrov',   'Пётр',    'Петров',   5, 'Отличный курс, всё очень понятно объяснено!'),
            ('sidorova', 'Мария',   'Сидорова', 4, 'В целом хорошо, но можно добавить больше примеров.'),
            ('kozlov',   'Алексей', 'Козлов',   3, 'Удовлетворительно. Материал есть, но подача скучная.'),
            ('smirnov',  'Дмитрий', 'Смирнов',  2, 'Ожидал большего, много ошибок в заданиях.'),
            ('volkova',  'Анна',    'Волкова',  1, 'Плохо, не рекомендую — материал устаревший.'),
            ('popov',    'Сергей',  'Попов',    0, 'Ужасный курс, пустая трата времени.'),
            ('ivanova',  'Ольга',   'Иванова',  5, 'Шикарно! Преподаватель — профи.'),
            ('nikitin',  'Павел',   'Никитин',  4, 'Хороший курс для начинающих.'),
            ('fedorova', 'Елена',   'Фёдорова', 3, 'Среднячок, есть и лучше.'),
            ('morozov',  'Игорь',   'Морозов',  5, 'Мне всё понравилось, рекомендую.'),
            ('sokolova', 'Татьяна', 'Соколова', 2, 'Не оправдал ожиданий.'),
            ('belov',    'Андрей',  'Белов',    4, 'Хороший баланс теории и практики.'),
        ]

        for login, fn, ln, rating, text in test_reviews:
            user = db.session.execute(db.select(User).filter_by(login=login)).scalar()
            if not user:
                user = User(first_name=fn, last_name=ln, login=login)
                user.set_password('Qwerty123')
                db.session.add(user)
                db.session.flush()

            existing = db.session.execute(
                db.select(Review).filter_by(course_id=course.id, user_id=user.id)
            ).scalar()
            if existing:
                continue

            review = Review(rating=rating, text=text, course_id=course.id, user_id=user.id)
            db.session.add(review)
            course.rating_sum = (course.rating_sum or 0) + rating
            course.rating_num = (course.rating_num or 0) + 1

        db.session.commit()
        print('Seed done.')


if __name__ == '__main__':
    seed()
