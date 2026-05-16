<template>
  <div class="dashboard">
    <div class="header">
      <div class="header-left">
        <img src="/images/logo.png" class="logo" alt="logo">
        <h2>选课推荐系统</h2>
      </div>
      <div class="header-right">
        <n-button type="primary" size="small" @click="openSimulatedSelection">模拟选课</n-button>
        <n-dropdown trigger="click" :options="menuOptions" @select="handleMenuCommand">
          <div class="menu-btn">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <line x1="4" y1="6" x2="20" y2="6"></line>
              <line x1="4" y1="12" x2="20" y2="12"></line>
              <line x1="4" y1="18" x2="20" y2="18"></line>
            </svg>
          </div>
        </n-dropdown>
      </div>
      <div class="mobile-menu-btn" @click="toggleMobileMenu">菜单</div>
    </div>

    <div class="main">
      <n-card>
        <template #header>
          <div class="card-header-tabs">
            <n-tabs v-model:value="mainSearchMode" @update:value="handleMainTabChange" type="segment">
              <n-tab-pane name="course" tab="课程检索" />
              <n-tab-pane name="cs_course" tab="教师检索（计算机学院）" />
            </n-tabs>
          </div>
        </template>

        <!-- 课程检索 -->
        <div v-if="mainSearchMode === 'course'">
          <div class="search-form">
            <n-form :inline="true" :model="{}">
              <n-form-item>
                <n-input v-model:value="searchKeyword" placeholder="搜索课程名" clearable @update:value="debounceFilterCourses" style="width: 200px;" />
              </n-form-item>
              <n-form-item>
                <n-select v-model:value="selectedMajor" placeholder="全部专业" clearable :options="majorOptions" @update:value="onMajorChange" style="width: 200px;" />
              </n-form-item>
              <n-form-item>
                <n-select v-model:value="selectedCollege" placeholder="全部学院" clearable :options="collegeOptions" @update:value="loadCourses" style="width: 200px;" />
              </n-form-item>
              <n-form-item>
                <n-select v-model:value="selectedCourseType" multiple placeholder="全部课程性质" clearable :options="courseTypeOptions" @update:value="loadCourses" style="width: 220px;" />
              </n-form-item>
              <n-form-item v-if="selectedMajor">
                <n-select v-model:value="selectedMajorCourseType" placeholder="对本专业分类" clearable :options="majorCourseTypeOptions" @update:value="filterCourses" style="width: 180px;" />
              </n-form-item>
              <n-form-item>
                <n-input v-model:value="teacherKeyword" placeholder="搜索教师名（支持拼音缩写）" clearable @update:value="filterCourses" style="width: 200px;" />
              </n-form-item>
            </n-form>
          </div>

          <div v-if="isLoading" class="loading-skeleton">
            <div class="skeleton-grid">
              <skeleton-card v-for="n in 8" :key="n" :lines="5" />
            </div>
          </div>

          <div v-if="!isLoading" class="course-grid">
            <n-card v-for="course in paginatedCourses" :key="course.id" class="course-card" :hoverable="true" @click="showDetail(course)">
              <template #header>
                <div class="course-card-header">
                  <span class="course-name">{{ course.name }}</span>
                  <n-tag v-if="course.major_names" size="small" type="info">{{ course.major_names }}</n-tag>
                </div>
              </template>
              <div class="course-info">
                <p><n-text depth="2">学分:</n-text> {{ course.credit }}</p>
                <p v-if="course.college"><n-text depth="2">开课学院:</n-text> {{ course.college }}</p>
                <p><n-text depth="2">考核方式:</n-text> {{ course.assessment_method || '闭卷笔试' }}</p>
                <p v-if="course.topic_category"><n-text depth="2">主题类别:</n-text> {{ course.topic_category }}</p>
                <p><n-text depth="2">教师:</n-text> {{ course.teacher_names }}</p>
                <p><n-text depth="2">课程性质:</n-text> {{ course.course_types ? course.course_types.join('、') : (course.course_type || '') }}</p>
                <p><n-text depth="2">开课学期:</n-text> {{ course.semesters ? course.semesters.join('、') : '' }}</p>
                <p v-if="selectedMajor && course.major_study_semesters && course.major_study_semesters[selectedMajor] && course.major_study_semesters[selectedMajor].length > 0">
                  <n-text depth="2">建议修读学期:</n-text> {{ course.major_study_semesters[selectedMajor].join('、') }}
                </p>
                <p v-if="selectedMajor && course.major_course_types && course.major_course_types[selectedMajor]">
                  <n-text depth="2">对本专业:</n-text> <n-tag :type="course.major_course_types[selectedMajor] === '必修' ? 'error' : 'success'" size="small">{{ course.major_course_types[selectedMajor] }}</n-tag>
                </p>
                <div v-if="course.teacher_ratings && Object.keys(course.teacher_ratings).length > 0">
                  <div v-for="(rating, teacherId) in course.teacher_ratings" :key="teacherId" class="teacher-rating-item">
                    <span>{{ getTeacherName(teacherId) }}: </span>
                    <n-rate :value="rating" readonly :allow-half="true" size="small" />
                    <span style="margin-left: 8px; color: #999; font-size: 12px;">({{ course.teacher_evaluation_counts?.[teacherId] || 0 }}人评价)</span>
                  </div>
                </div>
                <p v-else><n-text depth="2">评分:</n-text> 暂无评价</p>
                <p class="course-desc" :title="course.description">
                  <n-text depth="2">概述:</n-text> {{ course.description || '暂无介绍' }}
                </p>
              </div>
              <template #footer>
                <n-button type="primary" size="small" @click.stop="showDetail(course)">查看详情</n-button>
              </template>
            </n-card>
          </div>

          <n-empty v-if="!isLoading && courses.length === 0" description="暂无课程" />

          <div class="pagination-wrap">
            <n-pagination v-if="courses.length > pageSize" v-model:page="currentPage" :page-count="totalPages" @update:page="handlePageChange" />
          </div>
        </div>

        <!-- 教师检索 -->
        <div v-if="mainSearchMode === 'cs_course'">
          <div class="search-form">
            <n-form :inline="true" :model="{}">
              <n-form-item>
                <n-input v-model:value="csTeacherKeyword" placeholder="搜索教师名（支持拼音缩写）" clearable @update:value="filterCsTeachers" style="width: 200px;" />
              </n-form-item>
              <n-form-item>
                <n-select v-model:value="csCourseTypeFilter" multiple placeholder="全部课程性质" clearable :options="courseTypeOptions" style="width: 200px;" />
              </n-form-item>
            </n-form>
          </div>

          <div class="course-grid">
            <n-card v-for="teacher in paginatedCsTeachers" :key="teacher.id" class="course-card teacher-card" :hoverable="true">
              <template #header>
                <div class="teacher-card-header">
                  <span class="teacher-name">{{ teacher.name }}</span>
                  <n-button type="primary" size="small" @click.stop="openTeacherEvaluate(teacher)">评价老师</n-button>
                </div>
              </template>
              <p style="font-weight: 600; margin-bottom: 10px;">授课列表：</p>
              <div class="teacher-courses-list">
                <div v-for="course in getTeacherCourses(teacher.id)" :key="course.id" class="teacher-course-item" @click="showDetail(course)">
                  <span class="course-name-small">{{ course.name }}</span>
                </div>
              </div>
            </n-card>
          </div>

          <n-empty v-if="csFilteredTeachers.length === 0" description="暂无教师数据" />

          <div class="pagination-wrap">
            <n-pagination v-if="csTotalPages > 1" v-model:page="csCurrentPage" :page-count="csTotalPages" @update:page="() => {}" />
          </div>
        </div>
      </n-card>
    </div>

    <!-- 课程详情 -->
    <n-modal v-model:show="showDetailDialog" :title="selectedCourse?.name" preset="card" :style="{ maxWidth: '620px' }" :mask-closable="true">
      <div v-if="selectedCourse">
        <n-descriptions :column="1" bordered>
          <n-descriptions-item label="课程名">{{ selectedCourse.name }}</n-descriptions-item>
          <n-descriptions-item label="学分">{{ selectedCourse.credit }}</n-descriptions-item>
          <n-descriptions-item v-if="selectedCourse.college" label="开课学院">{{ selectedCourse.college }}</n-descriptions-item>
          <n-descriptions-item label="考核方式">{{ selectedCourse.assessment_method || '闭卷笔试' }}</n-descriptions-item>
          <n-descriptions-item label="专业">
            <span>{{ selectedCourse.major_names }}</span>
            <n-tag v-if="selectedMajor && selectedCourse.major_course_types && selectedCourse.major_course_types[selectedMajor]"
              size="small" :type="selectedCourse.major_course_types[selectedMajor] === '必修' ? 'error' : 'success'" style="margin-left: 10px;">
              {{ selectedCourse.major_course_types[selectedMajor] }}
            </n-tag>
          </n-descriptions-item>
          <n-descriptions-item label="授课教师">{{ selectedCourse.teacher_names }}</n-descriptions-item>
          <n-descriptions-item label="课程性质">{{ selectedCourse.course_types ? selectedCourse.course_types.join('、') : (selectedCourse.course_type || '') }}</n-descriptions-item>
          <n-descriptions-item label="开课学期">{{ selectedCourse.semesters ? selectedCourse.semesters.join('、') : '' }}</n-descriptions-item>
          <n-descriptions-item v-if="selectedMajor && selectedCourse.major_study_semesters && selectedCourse.major_study_semesters[selectedMajor] && selectedCourse.major_study_semesters[selectedMajor].length > 0" label="建议修读学期">
            {{ selectedCourse.major_study_semesters[selectedMajor].join('、') }}
          </n-descriptions-item>
          <n-descriptions-item label="教师评分" v-if="selectedCourse.teacher_ratings && Object.keys(selectedCourse.teacher_ratings).length > 0">
            <div v-for="(rating, teacherId) in selectedCourse.teacher_ratings" :key="teacherId" style="margin-bottom: 5px;">
              <span>{{ getTeacherName(teacherId) }}: </span>
              <n-rate :value="rating" readonly :allow-half="true" size="small" />
              <span style="margin-left: 10px; color: #999; font-size: 12px;">({{ selectedCourse.teacher_evaluation_counts?.[teacherId] || 0 }}人评价)</span>
            </div>
          </n-descriptions-item>
          <n-descriptions-item v-else label="评分">暂无评价</n-descriptions-item>
          <n-descriptions-item label="课程概述">{{ selectedCourse.description || '暂无介绍' }}</n-descriptions-item>
        </n-descriptions>

        <h4 style="margin-top: 20px; margin-bottom: 10px;">教师评价</h4>
        <div v-if="courseEvaluations.length === 0" style="color: #999; margin-bottom: 15px;">暂无评价，快来评价吧</div>
        <div v-for="ev in courseEvaluations" :key="ev.id" class="evaluation-item">
          <div class="eval-header">
            <strong>{{ ev.teacher_name || getTeacherName(ev.teacher_id) }}</strong>
            <n-rate :value="ev.rating" readonly :allow-half="true" size="small" />
            <span style="color: #999; font-size: 12px;">{{ ev.created_at }}</span>
            <n-button v-if="ev.user_id === currentUserId" type="error" size="tiny" @click="deleteEvaluation(ev.id)">删除</n-button>
          </div>
          <p class="eval-comment">{{ ev.comment || '无评价内容' }}</p>
        </div>

        <n-divider />
        <h4 style="margin-bottom: 10px;">添加评价</h4>
        <n-form :model="evalForm" label-placement="left" label-width="60px">
          <n-form-item label="教师">
            <n-select v-model:value="evalForm.teacher_id" placeholder="请选择教师" :options="teacherSelectOptions" />
          </n-form-item>
          <n-form-item label="评分">
            <n-rate v-model:value="evalForm.rating" :allow-half="true" />
          </n-form-item>
          <n-form-item label="评价">
            <n-input v-model:value="evalForm.comment" type="textarea" :rows="3" placeholder="写下你的评价..." />
          </n-form-item>
          <n-button type="primary" @click="addEvaluation">提交评价</n-button>
        </n-form>
      </div>
    </n-modal>

    <!-- 教师评价对话框 -->
    <n-modal v-model:show="showTeacherEvalDialog" :title="'评价教师 - ' + (selectedTeacherForEval?.name || '')" preset="card" :style="{ maxWidth: '500px' }" :mask-closable="true">
      <n-form :model="teacherEvalForm" label-placement="left" label-width="80px">
        <n-form-item label="课程">
          <n-select v-model:value="teacherEvalForm.course_id" placeholder="请选择课程" :options="teacherEvalCourseOptions" />
        </n-form-item>
        <n-form-item label="评分">
          <n-rate v-model:value="teacherEvalForm.rating" :allow-half="true" />
        </n-form-item>
        <n-form-item label="评价">
          <n-input v-model:value="teacherEvalForm.comment" type="textarea" :rows="4" placeholder="写下你的评价..." />
        </n-form-item>
        <n-button type="primary" @click="submitTeacherEval">提交</n-button>
      </n-form>
    </n-modal>

    <!-- 设置 -->
    <n-modal v-model:show="showSettingsDialog" title="设置" preset="card" :style="{ maxWidth: '400px' }" :mask-closable="true">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span>深色模式</span>
        <n-switch v-model:value="isDarkMode" @update:value="toggleDarkMode" />
      </div>
    </n-modal>

    <!-- 反馈 -->
    <n-modal v-model:show="showFeedbackDialog" title="用户反馈" preset="card" :style="{ maxWidth: '500px' }" :mask-closable="true">
      <n-card size="small" style="margin-bottom: 15px; max-height: 300px; overflow-y: auto;">
        <template #header><span>我的反馈记录</span></template>
        <div v-for="fb in myFeedbacks" :key="fb.id" class="feedback-item">
          <p class="feedback-content">{{ fb.content }}</p>
          <div class="feedback-footer">
            <n-text depth="3" style="font-size: 12px;">{{ fb.created_at }}</n-text>
            <n-button type="error" size="tiny" @click="handleDeleteFeedback(fb)">删除</n-button>
          </div>
        </div>
        <n-empty v-if="myFeedbacks.length === 0" description="暂无反馈记录" />
      </n-card>
      <n-input v-model:value="feedbackContent" type="textarea" :rows="4" placeholder="请输入您的反馈内容..." />
      <template #footer>
        <n-space justify="end">
          <n-button @click="showFeedbackDialog = false">取消</n-button>
          <n-button type="primary" @click="submitFeedback">提交</n-button>
        </n-space>
      </template>
    </n-modal>

    <button class="refresh-btn" :class="{ 'is-spinning': isRefreshing }" @click="handleRefresh" :disabled="isRefreshing" aria-label="刷新">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="refresh-icon">
        <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
        <path d="M3 3v5h5" />
      </svg>
    </button>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { useMessage, useDialog } from 'naive-ui'
import request, { clearCache } from '../api'
import { COURSE_TYPE_OPTIONS } from '../constants'
import SkeletonCard from '../components/SkeletonCard.vue'

export default defineComponent({
  components: { SkeletonCard },
  setup() {
    const message = useMessage()
    const dialog = useDialog()
    return { message, dialog }
  },
  data() {
    return {
      username: localStorage.getItem('username') || '',
      currentUserId: parseInt(localStorage.getItem('user_id')) || null,
      courseTypeOptions: COURSE_TYPE_OPTIONS.map(t => ({ label: t.label, value: t.value })),
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
      teacherKeyword: '',
      searchKeyword: '',
      showDetailDialog: false,
      selectedCourse: null,
      courseEvaluations: [],
      evalForm: { teacher_id: null, rating: 5, comment: '' },
      showSettingsDialog: false,
      isDarkMode: localStorage.getItem('darkMode') === 'true',
      showFeedbackDialog: false,
      myFeedbacks: [],
      feedbackContent: '',
      showMobileMenu: false,
      isRefreshing: false,
      mainSearchMode: 'course',
      searchDebounceTimer: null,
      csTeacherKeyword: '',
      csFilteredTeachers: [],
      csAllCourses: [],
      csTeachers: [],
      csCourseTypeFilter: [],
      currentPage: 1,
      pageSize: 20,
      showTeacherEvalDialog: false,
      selectedTeacherForEval: null,
      teacherEvalForm: { course_id: null, rating: 5, comment: '' },
      csCurrentPage: 1,
      csPageSize: 12
    }
  },
  computed: {
    majorOptions() {
      return this.majors.map(m => ({ label: m.name, value: m.id }))
    },
    collegeOptions() {
      return this.colleges.map(c => ({ label: c, value: c }))
    },
    majorCourseTypeOptions() {
      return [
        { label: '全部', value: null },
        { label: '必修', value: '必修' },
        { label: '选修', value: '选修' }
      ].filter(Boolean)
    },
    paginatedCourses() {
      const start = (this.currentPage - 1) * this.pageSize
      return this.courses.slice(start, start + this.pageSize)
    },
    totalPages() {
      return Math.ceil(this.courses.length / this.pageSize)
    },
    menuOptions() {
      return [
        { label: '数据分析', key: 'analysis' },
        { label: '反馈', key: 'feedback' },
        { label: '用户中心', key: 'userCenter' },
        { label: '设置', key: 'settings' },
        { type: 'divider', key: 'd1' },
        { label: '退出', key: 'logout' }
      ]
    },
    teacherSelectOptions() {
      if (!this.selectedCourse) return []
      return (this.selectedCourse.teacher_ids || []).map((id, index) => ({
        label: (this.selectedCourse.teacher_names || '').split(',')[index] || `教师${id}`,
        value: id
      }))
    },
    teacherEvalCourseOptions() {
      if (!this.selectedTeacherForEval) return []
      return this.getTeacherCourses(this.selectedTeacherForEval.id).map(c => ({
        label: c.name,
        value: c.id
      }))
    },
    paginatedCsTeachers() {
      const start = (this.csCurrentPage - 1) * this.csPageSize
      return this.csFilteredTeachers.slice(start, start + this.csPageSize)
    },
    csTotalPages() {
      return Math.ceil(this.csFilteredTeachers.length / this.csPageSize)
    }
  },
  async mounted() {
    await this.loadMajors()
    await this.loadCourses()
    this.colleges = [...new Set(this.allCourses.map(c => c.college).filter(Boolean))]
  },
  methods: {
    async loadMajors() {
      try {
        this.majors = await request.get('/majors')
      } catch { this.message.error('加载专业失败') }
    },
    async loadCourses() {
      this.isLoading = true
      try {
        const params = {}
        if (this.selectedMajor) params.major_id = this.selectedMajor
        if (this.selectedCourseType && this.selectedCourseType.length > 0) params.course_type = this.selectedCourseType.join(',')
        this.allCourses = await request.get('/courses', { params })
        this.filterCourses()
      } catch { this.message.error('加载课程失败') }
      finally { this.isLoading = false }
    },
    filterCourses() {
      let filtered = [...this.allCourses]
      if (this.selectedMajor) filtered = filtered.filter(c => c.majors?.some(m => m.id === this.selectedMajor))
      if (this.selectedCollege) filtered = filtered.filter(c => c.college === this.selectedCollege)
      if (this.searchKeyword) {
        const kw = this.searchKeyword.toLowerCase()
        filtered = filtered.filter(c => c.name.toLowerCase().includes(kw))
      }
      if (this.teacherKeyword) {
        const kw = this.teacherKeyword.toLowerCase()
        filtered = filtered.filter(c => {
          if (c.teacher_names) {
            const nameMatch = c.teacher_names.toLowerCase().includes(kw)
            const pinyinMatch = c.teacher_pinyins && c.teacher_pinyins.toLowerCase().includes(kw)
            return nameMatch || pinyinMatch
          }
          return false
        })
      }
      if (this.selectedTeacher) filtered = filtered.filter(c => c.teacher_ids && c.teacher_ids.includes(this.selectedTeacher))
      this.courses = filtered
      this.currentPage = 1
    },
    debounceFilterCourses() {
      if (this.searchDebounceTimer) clearTimeout(this.searchDebounceTimer)
      this.searchDebounceTimer = setTimeout(() => { this.currentPage = 1; this.filterCourses() }, 300)
    },
    getTeacherName(teacherId) {
      const teacher = this.teachers.find(t => t.id === Number(teacherId))
      return teacher ? teacher.name : '未知教师'
    },
    async showDetail(course) {
      this.selectedCourse = course
      this.showDetailDialog = true
      this.courseEvaluations = await request.get('/evaluations', { params: { course_id: course.id } })
      this.evalForm = { teacher_id: null, rating: 5, comment: '' }
    },
    async addEvaluation() {
      if (!this.evalForm.teacher_id || !this.selectedCourse) { this.message.warning('请选择教师'); return }
      try {
        await request.post('/evaluations', { course_id: this.selectedCourse.id, teacher_id: this.evalForm.teacher_id, rating: this.evalForm.rating, comment: this.evalForm.comment })
        this.message.success('评价提交成功')
        this.courseEvaluations = await request.get('/evaluations', { params: { course_id: this.selectedCourse.id } })
        await this.loadCourses()
        this.evalForm = { teacher_id: null, rating: 5, comment: '' }
      } catch { this.message.error('评价提交失败') }
    },
    async deleteEvaluation(id) {
      this.dialog.info({ title: '提示', content: '确定要删除这条评价吗？', positiveText: '确定', negativeText: '取消', onPositiveClick: async () => {
        try {
          await request.delete(`/evaluations/${id}`)
          this.message.success('评价删除成功')
          this.courseEvaluations = await request.get('/evaluations', { params: { course_id: this.selectedCourse.id } })
          await this.loadCourses()
        } catch { this.message.error('删除失败') }
      }})
    },
    async handleLogout() {
      this.dialog.info({ title: '提示', content: '你真的要退出吗？', positiveText: '确定', negativeText: '取消', onPositiveClick: () => {
        localStorage.clear(); clearCache(); this.$router.push('/login')
      }})
    },
    handleMenuCommand(command) {
      switch (command) {
        case 'analysis': this.$router.push('/data-analysis'); break
        case 'feedback': this.openFeedback(); break
        case 'userCenter': this.$router.push('/user-center'); break
        case 'settings': this.showSettingsDialog = true; break
        case 'logout': this.handleLogout(); break
      }
    },
    toggleDarkMode(val) {
      if (val) { document.documentElement.classList.add('dark-mode'); localStorage.setItem('darkMode', 'true') }
      else { document.documentElement.classList.remove('dark-mode'); localStorage.setItem('darkMode', 'false') }
    },
    toggleMobileMenu() { this.showMobileMenu = !this.showMobileMenu },
    openSimulatedSelection() { this.$router.push('/simulated-selection') },
    onMajorChange(val) { this.selectedMajor = val; this.loadCourses() },
    handlePageChange(page) { this.currentPage = page; window.scrollTo({ top: 0, behavior: 'smooth' }) },
    async handleRefresh() {
      this.isRefreshing = true
      clearCache()
      await this.loadCourses()
      setTimeout(() => { this.isRefreshing = false }, 500)
    },
    async openFeedback() {
      this.showFeedbackDialog = true
      this.myFeedbacks = await request.get('/feedbacks')
    },
    async submitFeedback() {
      if (!this.feedbackContent.trim()) { this.message.warning('反馈内容不能为空'); return }
      try {
        await request.post('/feedbacks', { content: this.feedbackContent })
        this.message.success('反馈提交成功'); this.feedbackContent = ''
        this.myFeedbacks = await request.get('/feedbacks')
      } catch (e) { this.message.error('提交失败: ' + (e.message || '未知错误')) }
    },
    async handleDeleteFeedback(fb) {
      this.dialog.info({ title: '提示', content: '确定要删除这条反馈吗？', positiveText: '确定', negativeText: '取消', onPositiveClick: async () => {
        try { await request.delete(`/feedbacks/${fb.id}`); this.message.success('删除成功'); this.myFeedbacks = await request.get('/feedbacks') }
        catch { this.message.error('删除失败') }
      }})
    },
    handleMainTabChange(tab) { if (tab === 'cs_course') this.loadCsCourses() },
    async loadCsCourses() {
      const params = { sort: this.csSortOrder, sort_by: 'order_num' }
      this.csAllCourses = await request.get('/courses', { params })
      this.csAllCourses = this.csAllCourses.filter(c => !c.college || c.college === '' || c.college === '计算机与人工智能学院')
      this.csTeachers = this.getUniqueTeachers(this.csAllCourses)
      this.filterCsCourses()
    },
    getUniqueTeachers(courses) {
      const teacherMap = new Map()
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
      return Array.from(teacherMap.values())
    },
    filterCsTeachers() {
      const keyword = this.csTeacherKeyword.toLowerCase()
      if (!keyword) { this.csFilteredTeachers = this.csTeachers; return }
      this.csFilteredTeachers = this.csTeachers.filter(t => {
        const nameMatch = t.name.toLowerCase().includes(keyword)
        const pinyinMatch = t.name_pinyin && t.name_pinyin.toLowerCase().includes(keyword)
        return nameMatch || pinyinMatch
      })
      this.csCurrentPage = 1
    },
    filterCsCourses() {
      this.csFilteredTeachers = this.csTeachers
      this.filterCsTeachers()
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
    },
    openTeacherEvaluate(teacher) {
      this.selectedTeacherForEval = teacher
      this.teacherEvalForm = { course_id: null, rating: 5, comment: '' }
      this.showTeacherEvalDialog = true
    },
    async submitTeacherEval() {
      if (!this.teacherEvalForm.course_id || !this.selectedTeacherForEval) { this.message.warning('请选择课程'); return }
      try {
        await request.post('/evaluations', {
          course_id: this.teacherEvalForm.course_id,
          teacher_id: this.selectedTeacherForEval.id,
          rating: this.teacherEvalForm.rating,
          comment: this.teacherEvalForm.comment
        })
        this.message.success('评价提交成功')
        this.showTeacherEvalDialog = false
      } catch { this.message.error('评价提交失败') }
    }
  }
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(0,0,0,0.04);
  position: sticky;
  top: 0;
  z-index: 100;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.logo {
  width: 36px;
  height: 36px;
  border-radius: 8px;
}
.header h2 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.menu-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  color: #666;
}
.menu-btn:hover {
  background: rgba(0,0,0,0.04);
}
.mobile-menu-btn {
  display: none;
}
.main {
  padding: 20px 24px;
}
.card-header-tabs {
  display: flex;
  justify-content: center;
}
.search-form {
  margin-bottom: 16px;
}
.search-form :deep(.n-form-item) {
  margin-bottom: 8px;
}
.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}
.loading-skeleton .skeleton-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}
.course-card {
  cursor: pointer;
}
.course-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}
.course-name {
  font-weight: 600;
  font-size: 15px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.course-info p {
  margin-bottom: 6px;
  font-size: 13px;
  line-height: 1.6;
}
.course-desc {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.teacher-rating-item {
  margin-bottom: 6px;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 4px;
}
.pagination-wrap {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}
.teacher-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.teacher-name {
  font-weight: 600;
  font-size: 16px;
}
.teacher-courses-list {
  max-height: 200px;
  overflow-y: auto;
}
.teacher-course-item {
  padding: 6px 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
  margin-bottom: 4px;
}
.teacher-course-item:hover {
  background: rgba(0, 0, 0, 0.04);
}
.course-name-small {
  font-size: 13px;
}
.evaluation-item {
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}
.eval-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}
.eval-comment {
  font-size: 13px;
  color: #666;
  margin: 0;
}
.feedback-item {
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}
.feedback-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 6px;
}
.refresh-btn {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: none;
  background: #2080F0;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(32, 128, 240, 0.3);
  transition: all 0.2s;
  z-index: 1000;
}
.refresh-btn:hover { background: #4098FC; }
.refresh-btn.is-spinning .refresh-icon { animation: spin 0.6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.refresh-icon { width: 20px; height: 20px; }
html.dark-mode .header { background: rgba(25, 25, 45, 0.85); }
html.dark-mode .header h2 { color: #e8e8e8; }
html.dark-mode .teacher-course-item:hover { background: rgba(255,255,255,0.06); }
html.dark-mode .evaluation-item { border-bottom-color: #333; }
html.dark-mode .feedback-item { border-bottom-color: #333; }

@media screen and (max-width: 768px) {
  .main { padding: 12px; }
  .course-grid { grid-template-columns: 1fr; }
  .header-right .n-button:first-child { display: none; }
  .mobile-menu-btn { display: block; cursor: pointer; padding: 8px; color: #666; }
}
</style>
