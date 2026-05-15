import logging
import os
from pypinyin import lazy_pinyin

LOG_DIR = '/var/log/course-recommendation'
if not os.path.exists(LOG_DIR):
    LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'app.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def mask_student_id(student_id):
    if not student_id:
        return ''
    if len(student_id) <= 5:
        return student_id[:2] + '*' * (len(student_id) - 2)
    return student_id[:3] + '*' * (len(student_id) - 5) + student_id[-2:]


def mask_real_name(real_name):
    if not real_name:
        return ''
    if len(real_name) <= 1:
        return real_name
    return real_name[0] + '*' * (len(real_name) - 1)


def invalidate_course_cache():
    from cache import cache
    cache.delete_pattern('courses:*')


def invalidate_teacher_cache():
    from cache import cache
    cache.delete_pattern('teachers:*')


def invalidate_major_cache():
    from cache import cache
    cache.delete_pattern('majors:*')


def get_name_pinyin(name):
    if not name:
        return ''
    return ''.join([p[0] for p in lazy_pinyin(name)])
