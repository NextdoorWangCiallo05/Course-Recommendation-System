<template>
  <div class="dashboard">
    <el-header class="header">
      <h2>选课推荐系统</h2>
      <div class="user-info">
        <span>欢迎, {{ username }}</span>
        <el-button type="warning" size="small" @click="openSimulatedSelection">模拟选课</el-button>
        <el-button type="primary" size="small" @click="openFeedback">反馈</el-button>
        <el-button type="success" size="small" @click="$router.push('/user-center')">用户中心</el-button>
        <el-button type="danger" size="small" @click="handleLogout">退出</el-button>
      </div>
    </el-header>
    <el-main class="main" :style="mainBgStyle">
      <el-card>
        <template #header>
          <div class="card-header">
            <el-tabs v-model="mainSearchMode" @tab-change="handleMainTabChange">
              <el-tab-pane label="课程检索" name="course"></el-tab-pane>
              <el-tab-pane label="教师检索（计算机学院）" name="cs_course"></el-tab-pane>
            </el-tabs>
          </div>
        </template>
        <div v-if="mainSearchMode === 'course'">
          <el-form :inline="true" class="search-form">
            <el-form-item label="搜索">
              <el-input v-model="searchKeyword" placeholder="搜索课程名" clearable @input="debounceFilterCourses" style="width: 200px;" />
            </el-form-item>
            <el-form-item label="专业分类">
              <el-select v-model="selectedMajor" placeholder="全部专业" clearable @change="onMajorChange" style="width: 200px;">
                <el-option v-for="m in majors" :key="m.id" :label="m.name" :value="m.id" />
              </el-select>
            </el-form-item>
            <el-form-item label="开课学院">
              <el-select v-model="selectedCollege" placeholder="全部学院" clearable @change="loadCourses" style="width: 200px;">
                <el-option v-for="college in colleges" :key="college" :label="college" :value="college" />
              </el-select>
            </el-form-item>
            <el-form-item label="课程性质">
              <el-select v-model="selectedCourseType" multiple placeholder="全部课程性质" clearable @change="loadCourses" style="width: 220px;">
                <el-option label="通识必修" value="通识必修" />
                <el-option label="通识选修" value="通识选修" />
                <el-option label="个性课程" value="个性课程" />
                <el-option label="学科必修" value="学科必修" />
                <el-option label="专业必修" value="专业必修" />
                <el-option label="专业选修" value="专业选修" />
                <el-option label="实践课" value="实践课" />
                <el-option label="英语必修" value="英语必修" />
                <el-option label="体育必修" value="体育必修" />
              </el-select>
            </el-form-item>
            <el-form-item v-if="selectedMajor" label="必修/选修">
              <el-select v-model="selectedMajorCourseType" placeholder="全部" clearable @change="loadCourses" style="width: 150px;">
                <el-option label="必修" value="必修" />
                <el-option label="选修" value="选修" />
              </el-select>
            </el-form-item>
            <el-form-item label="教师搜索">
              <el-input v-model="teacherKeyword" placeholder="搜索教师名（支持拼音缩写）" clearable @input="filterCourses" style="width: 180px;" />
            </el-form-item>
          </el-form>
          <div v-if="isLoading" class="loading-skeleton">
            <el-row :gutter="20">
              <el-col v-for="n in 6" :key="n" :xs="24" :sm="12" :md="8" :lg="6">
                <el-card class="course-card skeleton-card" shadow="hover">
                  <div class="skeleton-block skeleton-title"></div>
                  <div class="skeleton-block skeleton-tag"></div>
                  <div class="skeleton-block skeleton-line"></div>
                  <div class="skeleton-block skeleton-line short"></div>
                  <div class="skeleton-block skeleton-line"></div>
                  <div class="skeleton-block skeleton-btn"></div>
                </el-card>
              </el-col>
            </el-row>
          </div>
          <el-row v-if="!isLoading" :gutter="20">
            <el-col v-for="course in paginatedCourses" :key="course.id" :xs="24" :sm="12" :md="8" :lg="6">
              <el-card class="course-card" shadow="hover">
                <template #header>
                  <div class="card-header">
                    <span class="course-name">{{ course.name }}</span>
                  </div>
                  <div class="course-tags">
                    <el-tag type="info" size="small">{{ course.major_names }}</el-tag>
                  </div>
                </template>
                <div class="course-info">
                  <p><strong>学分:</strong> {{ course.credit }}</p>
                  <p v-if="course.college"><strong>开课学院:</strong> {{ course.college }}</p>
                  <p><strong>考核方式:</strong> {{ course.assessment_method || '闭卷笔试' }}</p>
                  <p v-if="course.topic_category"><strong>主题类别:</strong> {{ course.topic_category }}</p>
                  <p><strong>教师:</strong> {{ course.teacher_names }}</p>
                  <p><strong>课程性质:</strong> {{ course.course_types ? course.course_types.join('、') : (course.course_type || '') }}</p>
                  <p><strong>开课学期:</strong> {{ course.semesters ? course.semesters.join('、') : '' }}</p>
                  <p v-if="selectedMajor && course.major_study_semesters && course.major_study_semesters[selectedMajor] && course.major_study_semesters[selectedMajor].length > 0">
                    <strong>建议修读学期:</strong> {{ course.major_study_semesters[selectedMajor].join('、') }}
                  </p>
                  <p v-if="selectedMajor && course.major_course_types && course.major_course_types[selectedMajor]">
                    <strong>对本专业:</strong> {{ course.major_course_types[selectedMajor] }}
                  </p>
                  <div v-if="course.teacher_ratings && Object.keys(course.teacher_ratings).length > 0">
                    <div v-for="(rating, teacherId) in course.teacher_ratings" :key="teacherId" style="margin-left: 20px;">
                      <span>{{ getTeacherName(teacherId) }}: </span>
                      <el-rate :model-value="rating" disabled show-score text-color="#FF8D28" style="width: 120px;" />
                      <span style="margin-left: 30px; color: #909399; font-size: 12px;">({{ course.teacher_evaluation_counts?.[teacherId] || 0 }}人评价)</span>
                    </div>
                  </div>
                  <p v-else><strong>评分:</strong> 暂无评价</p>
                  <p class="course-desc" :title="course.description">
                    <strong>概述:</strong> {{ course.description || '暂无介绍' }}
                  </p>
                </div>
                <div class="card-actions">
                  <el-button type="primary" size="small" @click="showDetail(course)">查看详情</el-button>
                </div>
              </el-card>
            </el-col>
          </el-row>
          <el-empty v-if="courses.length === 0" description="暂无课程" />
          <el-pagination
            v-if="courses.length > pageSize"
            v-model:current-page="currentPage"
            :page-size="pageSize"
            :total="courses.length"
            layout="prev, pager, next"
            style="margin-top: 20px; justify-content: center;"
            @update:current-page="handlePageChange"
          />
        </div>
        <div v-if="mainSearchMode === 'cs_course'">
          <el-form :inline="true" class="search-form">
            <el-form-item label="搜索教师">
              <el-input v-model="csTeacherKeyword" placeholder="搜索教师名（支持拼音缩写）" clearable @input="filterCsTeachers" style="width: 200px;" />
            </el-form-item>
            <el-form-item label="课程性质">
              <el-select v-model="csCourseTypeFilter" multiple placeholder="全部课程性质" clearable style="width: 200px;">
                <el-option label="通识必修" value="通识必修" />
                <el-option label="通识选修" value="通识选修" />
                <el-option label="个性课程" value="个性课程" />
                <el-option label="学科必修" value="学科必修" />
                <el-option label="专业必修" value="专业必修" />
                <el-option label="专业选修" value="专业选修" />
                <el-option label="实践课" value="实践课" />
                <el-option label="英语必修" value="英语必修" />
                <el-option label="体育必修" value="体育必修" />
              </el-select>
            </el-form-item>
          </el-form>
          <!-- 按老师检索：显示老师卡片 -->
          <el-row :gutter="20" style="margin-top: 15px;">
            <el-col v-for="teacher in paginatedCsTeachers" :key="teacher.id" :xs="24" :sm="12" :md="8" :lg="6">
              <el-card class="course-card teacher-card" shadow="hover">
                <template #header>
                  <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="course-name teacher-name">👨‍🏫 {{ teacher.name }}</span>
                    <el-button type="primary" size="small" @click.stop="openTeacherEvaluate(teacher)">评价老师</el-button>
                  </div>
                </template>
                <div class="course-info">
                  <p style="font-weight: bold; margin-bottom: 10px;">📚 授课列表：</p>
                  <div class="teacher-courses-list">
                    <div v-for="course in getTeacherCourses(teacher.id)" :key="course.id" class="teacher-course-item" @click="showDetail(course)">
                      <div style="width: 100%;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                          <span class="course-name-small">{{ course.name }}</span>
                          <el-tag size="small" type="info">{{ course.credit }}学分</el-tag>
                        </div>
                        <div v-if="getTeacherCourseRating(teacher.id, course.id)" style="margin-top: 5px; font-size: 12px; color: #909399;">
                          <el-rate :model-value="getTeacherCourseRating(teacher.id, course.id).avg" disabled show-score text-color="#FF8D28" style="--el-rate-font-size: 14px;" />
                          ({{ getTeacherCourseRating(teacher.id, course.id).count }}人)
                        </div>
                        <div v-else style="margin-top: 5px; font-size: 12px; color: #c0c4cc;">暂无评价</div>
                      </div>
                    </div>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
          <el-empty v-if="filteredCsTeachers.length === 0" description="暂无数据" />
          <el-pagination
            v-if="filteredCsTeachers.length > csPageSize"
            v-model:current-page="csCurrentPage"
            :page-size="csPageSize"
            :total="filteredCsTeachers.length"
            layout="prev, pager, next"
            style="margin-top: 20px; justify-content: center;"
          />
        </div>
      </el-card>
    </el-main>

    <el-dialog v-model="showDetailDialog" :title="selectedCourse?.name" width="600px">
      <div v-if="selectedCourse" class="detail-content">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="课程名">{{ selectedCourse.name }}</el-descriptions-item>
          <el-descriptions-item label="学分">{{ selectedCourse.credit }}</el-descriptions-item>
          <el-descriptions-item label="开课学院" v-if="selectedCourse.college">{{ selectedCourse.college }}</el-descriptions-item>
          <el-descriptions-item label="考核方式">{{ selectedCourse.assessment_method || '闭卷笔试' }}</el-descriptions-item>
          <el-descriptions-item v-if="selectedCourse.topic_category" label="主题类别">{{ selectedCourse.topic_category }}</el-descriptions-item>
          <el-descriptions-item label="专业">
            <div v-for="major_id in selectedCourse.major_ids" :key="major_id" style="margin-bottom: 5px;">
              <span>{{ getMajorName(major_id) }}:</span>
              <el-tag size="small" :type="selectedCourse.major_course_types && selectedCourse.major_course_types[major_id] === '必修' ? 'danger' : 'success'">
                {{ selectedCourse.major_course_types && selectedCourse.major_course_types[major_id] || '必修' }}
              </el-tag>
            </div>
          </el-descriptions-item>
          <el-descriptions-item label="授课教师">{{ selectedCourse.teacher_names }}</el-descriptions-item>
          <el-descriptions-item label="课程性质">{{ selectedCourse.course_types ? selectedCourse.course_types.join('、') : (selectedCourse.course_type || '') }}</el-descriptions-item>
          <el-descriptions-item label="开课学期">{{ selectedCourse.semesters ? selectedCourse.semesters.join('、') : '' }}</el-descriptions-item>
          <el-descriptions-item v-if="selectedCourse.major_study_semesters && selectedCourse.major_ids" label="建议修读学期">
            <div v-for="major_id in selectedCourse.major_ids" :key="major_id" style="margin-bottom: 5px;">
              <span v-if="selectedCourse.major_study_semesters[major_id] && selectedCourse.major_study_semesters[major_id].length > 0">
                {{ getMajorName(major_id) }}: {{ selectedCourse.major_study_semesters[major_id].join('、') }}
              </span>
            </div>
          </el-descriptions-item>
          <el-descriptions-item v-if="selectedCourse.teacher_ratings && Object.keys(selectedCourse.teacher_ratings).length > 0" label="教师评分" :span="1">
            <div v-for="(rating, teacherId) in selectedCourse.teacher_ratings" :key="teacherId" style="margin-bottom: 10px;">
              <span>{{ getTeacherName(teacherId) }}: </span>
              <el-rate :model-value="rating" disabled show-score style="width: 120px;" />
              <span style="margin-left: 30px; color: #909399; font-size: 12px;">({{ selectedCourse.teacher_evaluation_counts?.[teacherId] || 0 }}人评价)</span>
            </div>
          </el-descriptions-item>
          <el-descriptions-item v-else label="评分">
            暂无评价
          </el-descriptions-item>
          <el-descriptions-item label="课程概述">{{ selectedCourse.description || '暂无介绍' }}</el-descriptions-item>
        </el-descriptions>
        <h4 style="margin-top: 20px; margin-bottom: 10px;">教师评价</h4>
        <div v-if="courseEvaluations.length > 0">
          <div v-for="item in courseEvaluations" :key="item.id" class="eval-item">
            <div class="eval-header">
              <span class="eval-teacher">{{ item.teacher_name }}</span>
              <el-rate v-model="item.rating" disabled style="width: 120px;" />
              <el-button v-if="item.user_id === currentUserId" type="danger" size="small" @click="deleteEvaluation(item.id)">删除</el-button>
            </div>
            <p class="eval-comment">{{ item.comment }}</p>
            <p class="eval-time">{{ item.created_at }}</p>
          </div>
        </div>
        <el-empty v-else description="暂无评价" :image-size="60" />
        <div style="margin-top: 20px;">
          <h4 style="margin-bottom: 10px;">添加评价</h4>
          <el-form :model="evalForm" label-width="80px">
            <el-form-item label="教师">
              <el-select v-model="evalForm.teacher_id" placeholder="请选择教师" :disabled="!selectedCourse">
                <el-option v-for="(teacher_id, index) in selectedCourse?.teacher_ids" :key="teacher_id" :label="selectedCourse.teacher_names.split(',')[index]" :value="teacher_id" />
              </el-select>
            </el-form-item>
            <el-form-item label="星级">
              <el-rate v-model="evalForm.rating" style="width: 200px;" />
            </el-form-item>
            <el-form-item label="评语">
              <el-input v-model="evalForm.comment" type="textarea" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="addEvaluation" :disabled="!evalForm.teacher_id">提交评价</el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </el-dialog>

    <el-dialog v-model="showTeacherEvalDialog" :title="'评价 ' + selectedTeacherForEval?.name" width="500px">
      <el-form label-width="80px">
        <el-form-item label="选择课程">
          <el-select v-model="teacherEvalForm.course_id" placeholder="请选择要评价的课程" style="width: 100%;">
            <el-option v-for="course in getTeacherCourses(selectedTeacherForEval?.id)" :key="course.id" :label="course.name" :value="course.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="星级评分">
          <el-rate v-model="teacherEvalForm.rating" style="width: 200px;" />
        </el-form-item>
        <el-form-item label="评价内容">
          <el-input v-model="teacherEvalForm.comment" type="textarea" :rows="4" placeholder="请输入您的评价..." />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showTeacherEvalDialog = false">取消</el-button>
        <el-button type="primary" @click="submitTeacherEval">提交评价</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showFeedbackDialog" title="用户反馈" width="500px">
      <el-card style="margin-bottom: 15px; max-height: 300px; overflow-y: auto;">
        <template #header>
          <span>我的反馈记录</span>
        </template>
        <div v-for="fb in myFeedbacks" :key="fb.id" class="feedback-item">
          <p class="feedback-content">{{ fb.content }}</p>
          <div class="feedback-footer">
            <span class="feedback-time">{{ fb.created_at }}</span>
            <el-button type="danger" size="small" @click="handleDeleteFeedback(fb)">删除</el-button>
          </div>
        </div>
        <el-empty v-if="myFeedbacks.length === 0" description="暂无反馈记录" />
      </el-card>
      <el-input v-model="feedbackContent" type="textarea" :rows="4" placeholder="请输入您的反馈内容..." />
      <template #footer>
        <el-button @click="showFeedbackDialog = false">取消</el-button>
        <el-button type="primary" @click="submitFeedback">提交</el-button>
      </template>
    </el-dialog>
    <button class="refresh-btn" :class="{ 'is-spinning': isRefreshing }" @click="handleRefresh" :disabled="isRefreshing" aria-label="刷新">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="refresh-icon">
        <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
        <path d="M3 3v5h5" />
      </svg>
    </button>
  </div>
</template>

<script>
import request, { clearCache } from '../api'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  data() {
    return {
      username: '',
      currentUserId: null,
      isLoading: false,
      majors: [],
      teachers: [],
      courses: [],
      allCourses: [],
      selectedMajor: null,
      selectedCollege: null,
      colleges: [],
      selectedCourseType: [],
      selectedMajorCourseType: null,
      selectedTeacher: null,
      teacherKeyword: '',
      searchKeyword: '',
      showDetailDialog: false,
      selectedCourse: null,
      courseEvaluations: [],
      evalForm: { teacher_id: null, rating: 5, comment: '' },
      showFeedbackDialog: false,
      myFeedbacks: [],
      feedbackContent: '',
      isRefreshing: false,
      mainSearchMode: 'course',
      csSearchMode: 'course',
      csCourses: [],
      csAllCourses: [],
      csTeachers: [],
      csCourseKeyword: '',
      csTeacherKeyword: '',
      csSelectedTeacher: null,
      csCourseTypeFilter: [],
      csSortOrder: 'asc',
      showTeacherEvalDialog: false,
      selectedTeacherForEval: null,
      teacherEvalForm: { course_id: null, rating: 5, comment: '' },
      currentPage: 1,
      pageSize: 12,
      csCurrentPage: 1,
      csPageSize: 8,
      searchDebounceTimer: null,
      csSearchDebounceTimer: null
    }
  },
  async mounted() {
    this.username = localStorage.getItem('username')
    this.currentUserId = parseInt(localStorage.getItem('user_id'))
    await this.loadMajors()
    await this.loadTeachers()
    await this.loadCourses()
  },
  computed: {
    mainBgStyle() {
      return {
        backgroundColor: 'rgba(255, 255, 255, 0.4)',
        backgroundImage: 'url(/images/dashboard-bg.jpg)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundAttachment: 'fixed'
      }
    },
    filteredCsTeachers() {
      let teachers = this.csTeachers || []
      if (this.csTeacherKeyword) {
        const keyword = this.csTeacherKeyword.toLowerCase()
        teachers = teachers.filter(t => {
          const nameMatch = t.name.toLowerCase().includes(keyword)
          const pinyinMatch = t.name_pinyin && t.name_pinyin.toLowerCase().includes(keyword)
          return nameMatch || pinyinMatch
        })
      }
      if (this.csCourseTypeFilter && this.csCourseTypeFilter.length > 0) {
        const teacherIdsWithCourses = new Set()
        this.csAllCourses.forEach(course => {
          const types = course.course_types || (course.course_type ? [course.course_type] : [])
          if (types.some(t => this.csCourseTypeFilter.includes(t))) {
            if (course.teacher_ids && Array.isArray(course.teacher_ids)) {
              course.teacher_ids.forEach(id => teacherIdsWithCourses.add(String(id)))
            }
          }
        })
        teachers = teachers.filter(t => teacherIdsWithCourses.has(t.id))
      }
      return teachers
    },
    paginatedCourses() {
      const start = (this.currentPage - 1) * this.pageSize
      return this.courses.slice(start, start + this.pageSize)
    },
    paginatedCsTeachers() {
      const start = (this.csCurrentPage - 1) * this.csPageSize
      return this.filteredCsTeachers.slice(start, start + this.csPageSize)
    }
  },
  methods: {
    async handleRefresh() {
      if (this.isRefreshing) return
      this.isRefreshing = true
      await this.loadMajors()
      await this.loadTeachers()
      await this.loadCourses()
      setTimeout(() => {
        this.isRefreshing = false
        ElMessage.success('刷新成功')
      }, 500)
    },
    async loadMajors() {
      this.majors = await request.get('/majors')
    },
    async loadTeachers() {
      this.teachers = await request.get('/teachers')
    },
    onMajorChange() {
      this.selectedMajorCourseType = null
      this.currentPage = 1
      this.loadCourses()
    },
    handlePageChange() {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },
    async loadCourses() {
      this.isLoading = true
      try {
        const params = {}
        if (this.selectedMajor) {
          params.major_id = this.selectedMajor
        }
        if (this.selectedCourseType && this.selectedCourseType.length > 0) {
          params.course_type = this.selectedCourseType.join(',')
        }
        if (this.selectedMajor && this.selectedMajorCourseType) {
          params.major_course_type = this.selectedMajorCourseType
        }
        this.allCourses = await request.get('/courses', { params })
        this.updateColleges()
        this.filterCourses()
      } finally {
        this.isLoading = false
      }
    },
    updateColleges() {
      const collegeSet = new Set()
      if (this.allCourses) {
        this.allCourses.forEach(course => {
          if (course.college) {
            collegeSet.add(course.college)
          }
        })
      }
      this.colleges = Array.from(collegeSet).sort()
    },
    filterCourses() {
      let filtered = this.allCourses || []
      if (this.selectedCollege) {
        filtered = filtered.filter(c => c.college === this.selectedCollege)
      }
      if (this.searchKeyword) {
        const keyword = this.searchKeyword.toLowerCase()
        filtered = filtered.filter(c => c.name.toLowerCase().includes(keyword))
      }
      if (this.teacherKeyword) {
        const keyword = this.teacherKeyword.toLowerCase()
        filtered = filtered.filter(c => {
          if (c.teacher_names) {
            const nameMatch = c.teacher_names.toLowerCase().includes(keyword)
            const pinyinMatch = c.teacher_pinyins && c.teacher_pinyins.toLowerCase().includes(keyword)
            return nameMatch || pinyinMatch
          }
          return false
        })
      }
      if (this.selectedTeacher) {
        filtered = filtered.filter(c => c.teacher_ids && c.teacher_ids.includes(this.selectedTeacher))
      }
      this.courses = filtered
    },
    debounceFilterCourses() {
      if (this.searchDebounceTimer) clearTimeout(this.searchDebounceTimer)
      this.searchDebounceTimer = setTimeout(() => {
        this.currentPage = 1
        this.filterCourses()
      }, 300)
    },
    getTeacherName(teacherId) {
      const teacher = this.teachers.find(t => t.id === Number(teacherId))
      return teacher ? teacher.name : '未知教师'
    },
    async showDetail(course) {
      this.selectedCourse = course
      this.showDetailDialog = true
      this.courseEvaluations = await request.get('/evaluations', { params: { course_id: course.id } })
      // 重置评价表单
      this.evalForm = { teacher_id: null, rating: 5, comment: '' }
    },
    getMajorName(majorId) {
      const major = this.majors.find(m => m.id === Number(majorId))
      return major ? major.name : '未知专业'
    },
    async addEvaluation() {
      if (!this.evalForm.teacher_id || !this.selectedCourse) {
        ElMessage.warning('请选择教师')
        return
      }
      try {
        await request.post('/evaluations', {
          course_id: this.selectedCourse.id,
          teacher_id: this.evalForm.teacher_id,
          rating: this.evalForm.rating,
          comment: this.evalForm.comment
        })
        ElMessage.success('评价提交成功')
        // 重新加载评价
        this.courseEvaluations = await request.get('/evaluations', { params: { course_id: this.selectedCourse.id } })
        // 重新加载课程列表以更新评分
        await this.loadCourses()
        // 重置评价表单
        this.evalForm = { teacher_id: null, rating: 5, comment: '' }
      } catch (error) {
        ElMessage.error('评价提交失败')
        console.error(error)
      }
    },
    async deleteEvaluation(id) {
      try {
        await ElMessageBox.confirm('确定要删除这条评价吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        await request.delete(`/evaluations/${id}`)
        ElMessage.success('评价删除成功')
        // 重新加载评价
        this.courseEvaluations = await request.get('/evaluations', { params: { course_id: this.selectedCourse.id } })
        // 重新加载课程列表以更新评分
        await this.loadCourses()
      } catch {
      }
    },
    async handleLogout() {
      try {
        await ElMessageBox.confirm('你真的要退出吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        localStorage.clear()
        clearCache()
        this.$router.push('/login')
      } catch {
      }
    },
    async openFeedback() {
      this.showFeedbackDialog = true
      this.myFeedbacks = await request.get('/feedbacks')
    },
    openSimulatedSelection() {
      this.$router.push('/simulated-selection')
    },
    async submitFeedback() {
      if (!this.feedbackContent.trim()) {
        ElMessage.warning('反馈内容不能为空')
        return
      }
      try {
        await request.post('/feedbacks', { content: this.feedbackContent })
        ElMessage.success('反馈提交成功')
        this.feedbackContent = ''
        this.myFeedbacks = await request.get('/feedbacks')
      } catch (error) {
        ElMessage.error('提交失败: ' + (error.message || '未知错误'))
      }
    },
    async handleDeleteFeedback(fb) {
      try {
        await ElMessageBox.confirm('确定要删除这条反馈吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        await request.delete(`/feedbacks/${fb.id}`)
        ElMessage.success('删除成功')
        this.myFeedbacks = await request.get('/feedbacks')
      } catch {
      }
    },
    handleMainTabChange(tab) {
      if (tab === 'cs_course') {
        this.loadCsCourses()
      }
    },
    async loadCsCourses() {
      const params = { sort: this.csSortOrder, sort_by: 'order_num' }
      this.csAllCourses = await request.get('/courses', { params })
      this.csAllCourses = this.csAllCourses.filter(c => !c.college || c.college === '' || c.college === '计算机与人工智能学院')
      this.csTeachers = this.getUniqueTeachers(this.csAllCourses)
      this.filterCsCourses()
    },
    getUniqueTeachers(courses) {
      const teacherMap = new Map()
      if (courses) {
        courses.forEach(course => {
          if (course.teacher_ids && course.teacher_names) {
            const ids = Array.isArray(course.teacher_ids) ? course.teacher_ids : (course.teacher_ids || '').split(',').map(id => id.trim())
            const names = Array.isArray(course.teacher_names) ? course.teacher_names : (course.teacher_names || '').split(',')
            const pinyins = course.teacher_pinyins ? (Array.isArray(course.teacher_pinyins) ? course.teacher_pinyins : (course.teacher_pinyins || '').split(',')) : []
            ids.forEach((id, index) => {
              const idStr = String(id)
              if (!teacherMap.has(idStr)) {
                teacherMap.set(idStr, { id: idStr, name: names[index] ? names[index].trim() : '', name_pinyin: pinyins[index] ? pinyins[index].trim() : '' })
              }
            })
          }
        })
      }
      return Array.from(teacherMap.values()).sort((a, b) => a.name.localeCompare(b.name, 'zh'))
    },
    filterCsCourses() {
      let filtered = this.csAllCourses || []
      if (this.csSearchMode === 'course') {
        if (this.csCourseKeyword) {
          const keyword = this.csCourseKeyword.toLowerCase()
          filtered = filtered.filter(c => c.name.toLowerCase().includes(keyword))
        }
      } else if (this.csSearchMode === 'teacher') {
        if (this.csSelectedTeacher) {
          filtered = filtered.filter(c => {
            if (!c.teacher_ids) return false
            const teacherIds = Array.isArray(c.teacher_ids) ? c.teacher_ids.map(id => String(id)) : (c.teacher_ids || '').split(',').map(id => id.trim())
            return teacherIds.includes(this.csSelectedTeacher)
          })
        }
      }
      if (this.csCourseTypeFilter && this.csCourseTypeFilter.length > 0) {
        filtered = filtered.filter(c => {
          const types = c.course_types || (c.course_type ? [c.course_type] : [])
          return types.some(t => this.csCourseTypeFilter.includes(t))
        })
      }
      this.csCourses = filtered
    },
    getTeacherRating(teacherId) {
      let total = 0
      let count = 0
      if (this.csAllCourses) {
        this.csAllCourses.forEach(course => {
          if (course.teacher_ratings && course.teacher_ratings[teacherId]) {
            total += course.teacher_ratings[teacherId] * (course.teacher_evaluation_counts?.[teacherId] || 1)
            count += course.teacher_evaluation_counts?.[teacherId] || 1
          }
        })
      }
      if (count === 0) return null
      return { avg: Math.round(total / count * 10) / 10, count }
    },
    getTeacherCourseRating(teacherId, courseId) {
      if (this.csAllCourses) {
        const course = this.csAllCourses.find(c => c.id === courseId)
        if (course && course.teacher_ratings && course.teacher_ratings[teacherId]) {
          return {
            avg: course.teacher_ratings[teacherId],
            count: course.teacher_evaluation_counts?.[teacherId] || 1
          }
        }
      }
      return null
    },
    openTeacherEvaluate(teacher) {
      this.selectedTeacherForEval = teacher
      this.teacherEvalForm = { course_id: null, rating: 5, comment: '' }
      this.showTeacherEvalDialog = true
    },
    async submitTeacherEval() {
      if (!this.teacherEvalForm.course_id) {
        ElMessage.warning('请选择课程')
        return
      }
      try {
        await request.post('/evaluations', {
          course_id: this.teacherEvalForm.course_id,
          teacher_id: parseInt(this.selectedTeacherForEval.id),
          rating: this.teacherEvalForm.rating,
          comment: this.teacherEvalForm.comment
        })
        ElMessage.success('评价成功')
        this.showTeacherEvalDialog = false
        await this.loadCsCourses()
      } catch (error) {
        ElMessage.error('评价失败: ' + (error.message || '未知错误'))
      }
    },
    getTeacherCourses(teacherId) {
      let courses = []
      if (this.csAllCourses) {
        courses = this.csAllCourses.filter(course => {
          if (!course.teacher_ids) return false
          const teacherIds = Array.isArray(course.teacher_ids) ? course.teacher_ids.map(id => String(id)) : (course.teacher_ids || '').split(',').map(id => id.trim())
          return teacherIds.includes(teacherId)
        })
        if (this.csCourseTypeFilter && this.csCourseTypeFilter.length > 0) {
          courses = courses.filter(c => {
            const types = c.course_types || (c.course_type ? [c.course_type] : [])
            return types.some(t => this.csCourseTypeFilter.includes(t))
          })
        }
      }
      return courses
    }
  }
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.85);
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow:
    0 4px 20px rgba(0, 0, 0, 0.08),
    inset 0 1px 2px rgba(255, 255, 255, 0.6);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
}

.header h2 {
  font-size: 20px;
  color: #333;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.main {
  padding: 20px;
  flex: 1;
  margin-top: 80px;
}

.main > .el-card {
  background: rgba(255, 255, 255, 0.75) !important;
  box-shadow:
    0 8px 32px rgba(31, 38, 135, 0.08),
    inset 0 1px 2px rgba(255, 255, 255, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  border-radius: 16px !important;
}

.search-form {
  margin-bottom: 20px;
}

.course-card {
  margin-bottom: 20px;
  background: rgba(255, 255, 255, 0.75) !important;
  box-shadow:
    0 8px 32px rgba(31, 38, 135, 0.08),
    inset 0 1px 2px rgba(255, 255, 255, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  border-radius: 16px !important;
  animation: cardFadeIn 0.4s ease both;
}

/* 骨架屏加载动画 */
.skeleton-card {
  pointer-events: none;
}

.skeleton-block {
  background: linear-gradient(90deg, rgba(200, 200, 200, 0.2) 25%, rgba(200, 200, 200, 0.4) 50%, rgba(200, 200, 200, 0.2) 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s ease infinite;
  border-radius: 6px;
  margin-bottom: 12px;
}

.skeleton-title {
  height: 20px;
  width: 60%;
}

.skeleton-tag {
  height: 24px;
  width: 40%;
}

.skeleton-line {
  height: 14px;
  width: 90%;
}

.skeleton-line.short {
  width: 50%;
}

.skeleton-btn {
  height: 32px;
  width: 80%;
  margin: 15px auto 0;
}

@keyframes skeleton-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.course-card:nth-child(2) { animation-delay: 0.05s; }
.course-card:nth-child(3) { animation-delay: 0.1s; }
.course-card:nth-child(4) { animation-delay: 0.15s; }
.course-card:nth-child(5) { animation-delay: 0.2s; }
.course-card:nth-child(6) { animation-delay: 0.25s; }
.course-card:nth-child(7) { animation-delay: 0.3s; }
.course-card:nth-child(8) { animation-delay: 0.35s; }

.course-card:hover {
  box-shadow:
    0 12px 40px rgba(31, 38, 135, 0.12),
    inset 0 1px 2px rgba(255, 255, 255, 0.7) !important;
  transform: translateY(-2px);
}

.teacher-card {
  background: rgba(255, 255, 255, 0.75) !important;
  box-shadow:
    0 8px 32px rgba(31, 38, 135, 0.08),
    inset 0 1px 2px rgba(255, 255, 255, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  border-radius: 16px !important;
}

.teacher-card:hover {
  box-shadow:
    0 12px 40px rgba(31, 38, 135, 0.12),
    inset 0 1px 2px rgba(255, 255, 255, 0.7) !important;
}

.course-name {
  font-weight: bold;
  font-size: 16px;
}

.course-info p {
  margin: 8px 0;
  color: #666;
}

.course-desc {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.card-actions {
  margin-top: 15px;
  text-align: center;
}

.teacher-card .teacher-name {
  font-size: 18px;
}

.teacher-courses-list {
  margin-top: 10px;
}

.teacher-course-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px dashed #ebeef5;
  cursor: pointer;
  transition: background-color 0.2s;
}

.teacher-course-item:hover {
  background-color: #f5f7fa;
  padding-left: 8px;
  padding-right: 8px;
}

.teacher-course-item:last-child {
  border-bottom: none;
}

.course-name-small {
  font-size: 13px;
  color: #333;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.detail-content {
  padding: 10px 0;
}

.eval-item {
  padding: 15px;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 15px;
}

.eval-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.eval-teacher {
  font-weight: bold;
  color: #333;
}

.eval-comment {
  color: #666;
  margin-bottom: 8px;
}

.eval-time {
  font-size: 12px;
  color: #999;
}

.feedback-item {
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}
.feedback-item:last-child {
  border-bottom: none;
}
.feedback-content {
  margin: 0 0 8px 0;
  color: #333;
}
.feedback-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.feedback-time {
  font-size: 12px;
  color: #999;
}

.floating-refresh-btn {
  position: fixed;
  bottom: 30px;
  left: 30px;
  width: 50px;
  height: 50px;
  font-size: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 999;
}

.refresh-btn {
  position: fixed;
  bottom: 30px;
  left: 30px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(16px) saturate(150%);
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.06),
    inset 0 1px 2px rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.3);
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  color: #4b5563;
  transition: all 0.2s ease;
  z-index: 999;
}

@media screen and (max-width: 768px) {
  .refresh-btn {
    bottom: 20px;
    left: 20px;
    padding: 6px;
  }
  .refresh-icon {
    width: 24px;
    height: 24px;
  }
}

.refresh-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.6);
  color: #0088FF;
}

.refresh-btn:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.refresh-icon {
  width: 32px;
  height: 32px;
}

.is-spinning .refresh-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes cardFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

:deep(.el-button) {
  padding: 15px 20px !important;
  font-size: 14px !important;
  border-radius: 20px !important;
  backdrop-filter: blur(16px) saturate(150%) !important;
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.06),
    inset 0 1px 2px rgba(255, 255, 255, 0.3) !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
}

:deep(.el-button--primary) {
  background: rgba(0, 136, 255, 0.78) !important;
}

:deep(.el-button--primary:hover:not(:disabled)) {
  background: rgba(0, 136, 255, 0.91) !important;
}

:deep(.el-button--success) {
  background: rgba(52, 199, 89, 0.78) !important;
}

:deep(.el-button--success:hover:not(:disabled)) {
  background: rgba(52, 199, 89, 0.91) !important;
}

:deep(.el-button--warning) {
  background: rgba(255, 204, 0, 0.78) !important;
}

:deep(.el-button--warning:hover:not(:disabled)) {
  background: rgba(255, 204, 0, 0.91) !important;
}

:deep(.el-button--danger) {
  background: rgba(255, 56, 50, 0.78) !important;
}

:deep(.el-button--danger:hover:not(:disabled)) {
  background: rgba(255, 56, 50, 0.91) !important;
}

:deep(.el-button--info) {
  background: rgba(144, 147, 153, 0.5) !important;
}

:deep(.el-button--info:hover:not(:disabled)) {
  background: rgba(144, 147, 153, 0.7) !important;
}

:deep(.el-button--default) {
  background: rgba(255, 255, 255, 0.4) !important;
}

:deep(.el-button--default:hover:not(:disabled)) {
  background: rgba(255, 255, 255, 0.6) !important;
}

.card-header {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 苹果风格分段控制器 - 液态玻璃效果 */
.card-header :deep(.el-tabs) {
  display: inline-flex;
  justify-content: center;
  background: rgba(0, 0, 0, 0.04);
  backdrop-filter: blur(20px) saturate(180%);
  border-radius: 20px;
  padding: 4px;
  box-shadow:
    inset 0 1px 2px rgba(0, 0, 0, 0.05),
    0 1px 3px rgba(0, 0, 0, 0.03);
}

.card-header :deep(.el-tabs__header) {
  margin: 0;
  border: none;
  display: flex;
  align-items: center;
}

.card-header :deep(.el-tabs__nav-wrap) {
  margin: 0;
  display: flex;
  align-items: center;
  border: none !important;
  padding: 0 !important;
}

.card-header :deep(.el-tabs__nav-wrap::after) {
  display: none !important;
}

.card-header :deep(.el-tabs__nav) {
  border: none;
  display: flex;
  gap: 2px;
  align-items: center;
  border-bottom: none !important;
}

.card-header :deep(.el-tabs__item) {
  border: none !important;
  border-radius: 20px;
  padding: 0 28px !important;
  font-size: 14px;
  color: #666;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  display: inline-flex !important;
  justify-content: center !important;
  align-items: center !important;
  text-align: center !important;
  white-space: nowrap;
  min-width: 80px;
  height: 40px !important;
  line-height: 1 !important;
  width: auto !important;
}

.card-header :deep(.el-tabs__item:hover) {
  color: #333;
}

.card-header :deep(.el-tabs__item.is-active) {
  background: linear-gradient(135deg, #0091FF 0%, #1E6EF4 100%);
  color: #fff;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(0, 122, 255, 0.35);
}

.card-header :deep(.el-tabs__active-bar) {
  display: none !important;
}
.user-info .el-button {
  font-size: 12px;
  padding: 15px 20px;
  border-radius: 20px !important;
  backdrop-filter: blur(16px) saturate(150%) !important;
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.06),
    inset 0 1px 2px rgba(255, 255, 255, 0.3) !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
}

.course-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.course-actions :deep(.el-button) {
  font-size: 14px;
  padding: 15px 20px;
  border-radius: 20px !important;
  backdrop-filter: blur(16px) saturate(150%) !important;
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.06),
    inset 0 1px 2px rgba(255, 255, 255, 0.3) !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
}

/* 手机端适配 (1080P竖屏) */
@media screen and (max-width: 768px) {
  .header {
    flex-direction: column;
    align-items: flex-start;
    padding: 15px;
    gap: 10px;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
  }
  
  .header h2 {
    font-size: 18px;
    margin: 0;
  }
  
  .main {
    margin-top: 120px;
  }
  
  .user-info {
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .user-info span {
    font-size: 14px;
  }
  
  .main {
    padding: 10px;
  }
  
  .search-form {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }
  
  .search-form .el-form-item {
    margin-bottom: 0;
  }
  
  .search-form .el-input,
  .search-form .el-select {
    width: 100% !important;
  }
  
  .course-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .course-card {
    padding: 15px;
  }
  
  .course-card h3 {
    font-size: 16px;
    margin-bottom: 10px;
  }
  
  .course-info {
    font-size: 14px;
  }
  
  .teacher-cards {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .teacher-card {
    padding: 15px;
  }
  
  .teacher-card h3 {
    font-size: 16px;
  }
  
  .teacher-actions {
    flex-direction: column;
    gap: 8px;
  }
  
  .teacher-actions .el-button {
    font-size: 20px;
    padding: 12px 20px;
  }
  
  .glass-btn {
    font-size: 12px;
    padding: 10px 20px;
    border-radius: 20px;
  }
}
</style>
