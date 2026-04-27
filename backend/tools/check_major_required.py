"""
选择专业必修课程：
1. 从各个专业的专业必修中抽取数据
2. 对于拥有"专业必修/专业选修"双重性质的课程，检查专业对应的必修/选修标签
"""

from app import app, db
from models import Course, Major, course_course_type, course_major, course_major_semester

with app.app_context():
    majors = Major.query.all()
    print(f'专业总数: {len(majors)}')
    for m in majors:
        print(f'  ID={m.id}: {m.name}')

    courses = Course.query.all()
    print(f'\n课程总数: {len(courses)}')

    major_required_courses = {}
    dual_nature_courses = []

    for course in courses:
        cts = db.session.execute(
            course_course_type.select().where(course_course_type.c.course_id == course.id)
        ).fetchall()
        course_types = [ct.course_type for ct in cts]

        has_required = '专业必修' in course_types
        has_elective = '专业选修' in course_types

        if not has_required:
            continue

        if has_required and has_elective:
            dual_nature_courses.append(course.id)

        cm_list = db.session.execute(
            course_major.select().where(course_major.c.course_id == course.id)
        ).fetchall()

        for cm in cm_list:
            major_id = cm.major_id
            type_for_major = cm.course_type_for_major

            if has_required and has_elective:
                if type_for_major != '必修':
                    continue

            if major_id not in major_required_courses:
                major_required_courses[major_id] = []
            major_required_courses[major_id].append({
                'course_id': course.id,
                'course_name': course.name,
                'credit': course.credit,
                'type_for_major': type_for_major,
                'course_types': course_types,
            })

    print(f'\n{"="*60}')
    print(f'各专业专业必修课程统计')
    print(f'{"="*60}')

    all_major_ids = sorted(major_required_courses.keys())
    for major_id in all_major_ids:
        major = Major.query.get(major_id)
        courses_list = major_required_courses[major_id]
        print(f'\n专业: {major.name} (ID={major.id}) - 共 {len(courses_list)} 门专业必修课程')
        for c in sorted(courses_list, key=lambda x: x['course_id']):
            dual_tag = ' [双重性质]' if c['course_id'] in dual_nature_courses else ''
            print(f'  ID={c["course_id"]:3d}: {c["course_name"]} (学分:{c["credit"]}){dual_tag}')

    print(f'\n{"="*60}')
    print(f'双重性质课程检查（同时拥有"专业必修"和"专业选修"标签）')
    print(f'{"="*60}')

    for course_id in sorted(dual_nature_courses):
        course = Course.query.get(course_id)
        cm_list = db.session.execute(
            course_major.select().where(course_major.c.course_id == course.id)
        ).fetchall()

        print(f'\n课程: {course.name} (ID={course.id})')
        for cm in cm_list:
            major = Major.query.get(cm.major_id)
            tag = '✓ 已选入专业必修' if cm.course_type_for_major == '必修' else '✗ 专业选修'
            print(f'  专业: {major.name} (ID={cm.major_id}) -> course_type_for_major={cm.course_type_for_major} {tag}')

    print(f'\n{"="*60}')
    print(f'汇总')
    print(f'{"="*60}')
    print(f'专业数量: {len(all_major_ids)}')
    total_required = sum(len(v) for v in major_required_courses.values())
    print(f'专业必修课程总条目数: {total_required}')
    print(f'双重性质课程数: {len(dual_nature_courses)}')
    for major_id in all_major_ids:
        major = Major.query.get(major_id)
        print(f'  {major.name}: {len(major_required_courses[major_id])} 门')
