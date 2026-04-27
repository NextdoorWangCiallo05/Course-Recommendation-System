from app import app, db
from models import Course, course_course_type, course_major, Major

with app.app_context():
    results = db.session.execute(
        course_course_type.select().where(course_course_type.c.course_type == "通识选修")
    ).fetchall()
    print(f"通识选修课程数量: {len(results)}")
    for r in results:
        c = db.session.get(Course, r.course_id)
        if c:
            cms = db.session.execute(
                course_major.select().where(course_major.c.course_id == c.id)
            ).fetchall()
            majors_info = [(cm.major_id, cm.course_type_for_major) for cm in cms]
            print(f"  ID={c.id}: {c.name} (学分:{c.credit}) 专业关联: {majors_info}")
