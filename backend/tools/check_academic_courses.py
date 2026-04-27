from app import app
from models import db, Course, course_course_type

with app.app_context():
    # 先查询所有课程
    courses = Course.query.all()
    print(f'总课程数: {len(courses)}')
    
    # 统计课程性质
    course_types = set()
    academic_required_courses = []
    
    for course in courses:
        # 获取课程的所有课程性质
        course_course_types = []
        try:
            ct_results = db.session.execute(
                course_course_type.select().where(course_course_type.c.course_id == course.id)
            ).fetchall()
            for ct in ct_results:
                course_course_types.append(ct.course_type)
                course_types.add(ct.course_type)
        except Exception as e:
            print(f"Error with course {course.id}: {e}")
        
        # 如果course_course_type表没有数据，尝试用旧的course_type字段
        if not course_course_types and hasattr(course, 'course_type') and course.course_type:
            course_course_types.append(course.course_type)
            course_types.add(course.course_type)
        
        # 检查是否包含学科必修
        if any('学科必修' in ct for ct in course_course_types):
            academic_required_courses.append((course.id, course.name, course_course_types))
    
    print(f'\n所有课程性质: {sorted(course_types)}')
    print(f'\n学科必修课程数量: {len(academic_required_courses)}')
    for c in academic_required_courses:
        print(f'{c[0]}: {c[1]} - {c[2]}')
    
    # 检查专业关联
    from models import course_major
    print(f'\n检查课程-专业关联:')
    for course in courses[:10]:  # 只检查前10个课程
        try:
            cm_results = db.session.execute(
                course_major.select().where(course_major.c.course_id == course.id)
            ).fetchall()
            if cm_results:
                print(f'课程 {course.name} 关联专业:')
                for cm in cm_results:
                    print(f'  专业ID: {cm.major_id}, 课程性质: {cm.course_type_for_major}')
        except Exception as e:
            print(f"Error checking course-major for {course.id}: {e}")
