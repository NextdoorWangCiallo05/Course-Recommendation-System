import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import Course, course_course_type, course_major, Major

with app.app_context():
    # 1. 查看所有课程类型
    results = db.session.execute(course_course_type.select()).fetchall()
    types = set(r.course_type for r in results)
    print("所有课程类型:", sorted(types))
    
    # 2. 查询所有实践课
    practice_results = db.session.execute(
        course_course_type.select().where(course_course_type.c.course_type == "实践课")
    ).fetchall()
    print(f"\n实践课数量: {len(practice_results)}")
    
    for r in practice_results:
        c = db.session.get(Course, r.course_id)
        if c:
            cms = db.session.execute(
                course_major.select().where(course_major.c.course_id == c.id)
            ).fetchall()
            majors_info = [(cm.major_id, cm.course_type_for_major) for cm in cms]
            print(f"  ID={c.id}: {c.name} (学分:{c.credit}) topic_category={c.topic_category} 专业关联: {majors_info}")
    
    # 3. 查看所有 topic_category 值
    print("\n所有 topic_category 值:")
    topics = db.session.query(Course.topic_category).distinct().all()
    for t in topics:
        print(f"  {t[0]}")
    
    # 4. 查看计算机(2)和软件(3)专业的实践课及其 topic_category
    print("\n\n计算机专业(ID=2)的实践课:")
    for r in practice_results:
        c = db.session.get(Course, r.course_id)
        if c:
            cms = db.session.execute(
                course_major.select().where(
                    course_major.c.course_id == c.id,
                    course_major.c.major_id.in_([2, 3])
                )
            ).fetchall()
            if cms:
                print(f"  ID={c.id}: {c.name} topic_category={c.topic_category}")
    
    # 5. 查看所有专业的实践课数量
    print("\n\n各专业实践课统计:")
    for m in Major.query.all():
        count = 0
        for r in practice_results:
            c = db.session.get(Course, r.course_id)
            if c:
                cm = db.session.execute(
                    course_major.select().where(
                        course_major.c.course_id == c.id,
                        course_major.c.major_id == m.id
                    )
                ).fetchone()
                if cm:
                    count += 1
        if count > 0:
            print(f"  {m.name}(ID={m.id}): {count} 门实践课")
