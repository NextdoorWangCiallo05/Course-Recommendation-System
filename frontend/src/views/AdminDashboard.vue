<template>
  <div class="dashboard">
    <div class="header">
      <div class="header-left">
        <img src="/images/logo.png" class="logo" alt="logo">
        <h2>选课推荐系统 - 管理面板</h2>
      </div>
      <div class="header-right">
        <n-text depth="3" class="welcome-text">欢迎, {{ username }}</n-text>
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
    </div>

    <div class="main">
      <n-menu v-model:value="currentMenu" mode="horizontal" :options="navItems" @update:value="handleMenuChange" />

      <!-- 课程预览 -->
      <div v-if="currentMenu === 'preview'">
        <n-card>
          <template #header>
            <div class="card-header">
              <n-tabs v-model:value="adminSearchMode" type="segment" @update:value="handleAdminTabChange">
                <n-tab-pane name="course" tab="课程检索" />
                <n-tab-pane name="cs_course" tab="教师检索（计算机学院）" />
              </n-tabs>
            </div>
          </template>

          <div v-if="adminSearchMode === 'course'">
            <n-form :inline="true" :model="{}">
              <n-form-item>
                <n-input v-model:value="adminSearchKeyword" placeholder="搜索课程名" clearable @update:value="debounceFilterAdminCourses" style="width: 200px;" />
              </n-form-item>
              <n-form-item>
                <n-select v-model:value="adminSelectedMajor" placeholder="全部专业" clearable :options="adminMajorOptions" @update:value="loadAdminCourses" style="width: 200px;" />
              </n-form-item>
              <n-form-item>
                <n-select v-model:value="adminSelectedCollege" placeholder="全部学院" clearable :options="adminCollegeOptions" @update:value="loadAdminCourses" style="width: 200px;" />
              </n-form-item>
              <n-form-item>
                <n-input v-model:value="adminTeacherKeyword" placeholder="搜索教师名" clearable @update:value="debounceFilterAdminCourses" style="width: 200px;" />
              </n-form-item>
            </n-form>

            <div v-if="adminLoading" class="skeleton-grid">
              <skeleton-card v-for="n in 8" :key="n" :lines="5" />
            </div>

            <div v-if="!adminLoading" class="course-grid">
              <n-card v-for="course in paginatedAdminCourses" :key="course.id" class="course-card" :hoverable="true" @click="showPreviewDetail(course)">
                <template #header>
                  <div class="course-card-header">
                    <span class="course-name">{{ course.name }}</span>
                    <n-tag v-if="course.major_names" size="small" type="info">{{ course.major_names }}</n-tag>
                  </div>
                </template>
                <div class="course-info">
                  <p><n-text depth="2">学分:</n-text> {{ course.credit }}</p>
                  <p v-if="course.college"><n-text depth="2">开课学院:</n-text> {{ course.college }}</p>
                  <p><n-text depth="2">教师:</n-text> {{ course.teacher_names }}</p>
                  <p><n-text depth="2">课程性质:</n-text> {{ course.course_types ? course.course_types.join('、') : course.course_type }}</p>
                  <p><n-text depth="2">开课学期:</n-text> {{ course.semesters ? course.semesters.join('、') : '' }}</p>
                  <div v-if="course.teacher_ratings && Object.keys(course.teacher_ratings).length > 0">
                    <div v-for="(rating, tid) in course.teacher_ratings" :key="tid" class="rating-item">
                      <span>{{ getAdminTeacherName(tid) }}: </span>
                      <n-rate :value="rating" readonly :allow-half="true" size="small" />
                    </div>
                  </div>
                  <p v-else><n-text depth="2">评分:</n-text> 暂无评价</p>
                  <p class="course-desc"><n-text depth="2">概述:</n-text> {{ course.description || '暂无介绍' }}</p>
                </div>
                <template #footer>
                  <n-button type="primary" size="small" @click.stop="showPreviewDetail(course)">查看详情</n-button>
                </template>
              </n-card>
            </div>
            <n-empty v-if="!adminLoading && adminCourses.length === 0" description="暂无课程" />
            <div class="pagination-wrap">
              <n-pagination v-if="adminCourses.length > adminPageSize" v-model:page="adminCurrentPage" :page-count="adminTotalPages" @update:page="handleAdminPageChange" />
            </div>
          </div>

          <div v-if="adminSearchMode === 'cs_course'">
            <n-form :inline="true" :model="{}">
              <n-form-item><n-input v-model:value="csAdminTeacherKeyword" placeholder="搜索教师名（支持拼音缩写）" clearable @update:value="filterCsAdminTeachers" style="width: 200px;" /></n-form-item>
            </n-form>
            <div class="course-grid">
              <n-card v-for="teacher in paginatedCsAdminTeachers" :key="teacher.id" class="course-card teacher-card" :hoverable="true">
                <template #header>
                  <div class="teacher-card-header">
                    <span class="teacher-name">{{ teacher.name }}</span>
                  </div>
                </template>
                <p style="font-weight:600;margin-bottom:10px;">授课列表：</p>
                <div class="teacher-courses-list">
                  <div v-for="course in getCsAdminTeacherCourses(teacher.id)" :key="course.id" class="teacher-course-item" @click="showPreviewDetail(course)">
                    <span>{{ course.name }}</span>
                  </div>
                </div>
              </n-card>
            </div>
            <n-empty v-if="csAdminFilteredTeachers.length === 0" description="暂无教师数据" />
          </div>
        </n-card>

        <n-modal v-model:show="showPreviewDetailDialog" :title="selectedPreviewCourse?.name" preset="card" :style="{ maxWidth: '620px' }" :mask-closable="true">
          <div v-if="selectedPreviewCourse">
            <n-descriptions :column="1" bordered>
              <n-descriptions-item label="学分">{{ selectedPreviewCourse.credit }}</n-descriptions-item>
              <n-descriptions-item v-if="selectedPreviewCourse.college" label="开课学院">{{ selectedPreviewCourse.college }}</n-descriptions-item>
              <n-descriptions-item label="考核方式">{{ selectedPreviewCourse.assessment_method || '闭卷笔试' }}</n-descriptions-item>
              <n-descriptions-item label="专业">
                <span>{{ selectedPreviewCourse.major_names }}</span>
                <n-tag v-if="previewSelectedMajor && selectedPreviewCourse.major_course_types && selectedPreviewCourse.major_course_types[previewSelectedMajor]"
                  size="small" :type="selectedPreviewCourse.major_course_types[previewSelectedMajor] === '必修' ? 'error' : 'success'" style="margin-left:10px">
                  {{ selectedPreviewCourse.major_course_types[previewSelectedMajor] }}
                </n-tag>
              </n-descriptions-item>
              <n-descriptions-item label="授课教师">{{ selectedPreviewCourse.teacher_names }}</n-descriptions-item>
              <n-descriptions-item label="课程性质">{{ selectedPreviewCourse.course_types ? selectedPreviewCourse.course_types.join('、') : selectedPreviewCourse.course_type }}</n-descriptions-item>
              <n-descriptions-item label="开课学期">{{ selectedPreviewCourse.semesters ? selectedPreviewCourse.semesters.join('、') : '' }}</n-descriptions-item>
              <n-descriptions-item v-if="previewSelectedMajor && selectedPreviewCourse.major_study_semesters?.[previewSelectedMajor]?.length" label="建议修读学期">
                {{ selectedPreviewCourse.major_study_semesters[previewSelectedMajor].join('、') }}
              </n-descriptions-item>
              <n-descriptions-item label="概述">{{ selectedPreviewCourse.description || '暂无介绍' }}</n-descriptions-item>
            </n-descriptions>
          </div>
        </n-modal>
      </div>

      <!-- 课程管理 -->
      <div v-if="currentMenu === 'manage'">
        <n-card>
          <template #header>
            <div class="card-header">
              <span style="font-size:18px;font-weight:600;">课程管理</span>
              <n-space>
                <n-button @click="loadAdminCourses">刷新</n-button>
                <n-button type="primary" @click="showAddCourseDialog">添加课程</n-button>
              </n-space>
            </div>
          </template>

          <n-form :inline="true" :model="{}">
            <n-form-item><n-input v-model:value="manageSearchKeyword" placeholder="搜索课程名" clearable @update:value="debounceFilterManage" style="width:200px" /></n-form-item>
            <n-form-item><n-select v-model:value="manageSelectedMajor" placeholder="全部专业" clearable :options="adminMajorOptions" @update:value="filterManage" style="width:200px" /></n-form-item>
            <n-form-item><n-select v-model:value="manageSelectedTeacher" placeholder="全部教师" clearable :options="manageTeacherOptions" @update:value="filterManage" style="width:200px" /></n-form-item>
          </n-form>

          <n-data-table :columns="manageColumns" :data="manageFilteredCourses" :bordered="false" :single-line="false" :loading="adminLoading" />

          <n-modal v-model:show="showCourseDialog" title="添加课程" preset="card" :style="{ maxWidth: '520px' }" :mask-closable="false">
            <n-form :model="courseForm" label-placement="left" label-width="100px">
              <n-form-item label="课程名"><n-input v-model:value="courseForm.name" placeholder="请输入课程名" /></n-form-item>
              <n-form-item label="学分"><n-input-number v-model:value="courseForm.credit" :min="0.5" :max="10" :step="0.5" /></n-form-item>
              <n-form-item label="开课学院"><n-input v-model:value="courseForm.college" placeholder="请输入开课学院" /></n-form-item>
              <n-form-item label="考核方式"><n-input v-model:value="courseForm.assessment_method" placeholder="请输入考核方式" /></n-form-item>
              <n-form-item label="序号"><n-input-number v-model:value="courseForm.order_num" :min="0" /></n-form-item>
              <n-form-item label="专业">
                <n-select v-model:value="courseForm.major_ids" multiple placeholder="请选择专业" :options="adminMajorOptions" />
              </n-form-item>
              <n-form-item label="教师"><n-input v-model:value="courseForm.teacher_names" placeholder="教师姓名（多个用逗号分隔）" /></n-form-item>
              <n-form-item label="课程性质">
                <n-select v-model:value="courseForm.course_types" multiple placeholder="请选择课程性质" :options="courseTypeOptions" />
              </n-form-item>
              <n-form-item label="开课学期">
                <n-select v-model:value="courseForm.semesters" multiple placeholder="请选择学期" :options="semesterOptions" />
              </n-form-item>
              <n-form-item label="课程描述"><n-input v-model:value="courseForm.description" type="textarea" :rows="3" /></n-form-item>
            </n-form>
            <template #footer>
              <n-space justify="end">
                <n-button @click="showCourseDialog = false">取消</n-button>
                <n-button type="primary" @click="submitCourse">确定</n-button>
              </n-space>
            </template>
          </n-modal>

          <n-modal v-model:show="showEditDialog" title="编辑课程" preset="card" :style="{ maxWidth: '520px' }" :mask-closable="false">
            <n-form :model="editCourseForm" label-placement="left" label-width="100px">
              <n-form-item label="课程名"><n-input v-model:value="editCourseForm.name" /></n-form-item>
              <n-form-item label="学分"><n-input-number v-model:value="editCourseForm.credit" :min="0.5" :max="10" :step="0.5" /></n-form-item>
              <n-form-item label="开课学院"><n-input v-model:value="editCourseForm.college" /></n-form-item>
              <n-form-item label="考核方式"><n-input v-model:value="editCourseForm.assessment_method" /></n-form-item>
              <n-form-item label="序号"><n-input-number v-model:value="editCourseForm.order_num" :min="0" /></n-form-item>
              <n-form-item label="专业">
                <n-select v-model:value="editCourseForm.major_ids" multiple placeholder="请选择专业" :options="adminMajorOptions" />
              </n-form-item>
              <n-form-item label="教师"><n-input v-model:value="editCourseForm.teacher_names" placeholder="教师姓名（多个用逗号分隔）" /></n-form-item>
              <n-form-item label="课程性质">
                <n-select v-model:value="editCourseForm.course_types" multiple placeholder="请选择课程性质" :options="courseTypeOptions" />
              </n-form-item>
              <n-form-item label="开课学期">
                <n-select v-model:value="editCourseForm.semesters" multiple placeholder="请选择学期" :options="semesterOptions" />
              </n-form-item>
              <n-form-item label="课程描述"><n-input v-model:value="editCourseForm.description" type="textarea" :rows="3" /></n-form-item>
            </n-form>
            <template #footer>
              <n-space justify="end">
                <n-button @click="showEditDialog = false">取消</n-button>
                <n-button type="primary" @click="submitEdit">确定</n-button>
              </n-space>
            </template>
          </n-modal>
        </n-card>
      </div>

      <!-- 选课分析 -->
      <div v-if="currentMenu === 'analysis'">
        <n-empty description="数据分析页面已独立至数据分析模块" />
        <n-button type="primary" @click="$router.push('/data-analysis')">前往数据分析</n-button>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, h } from 'vue'
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
      role: localStorage.getItem('role') || '',
      currentMenu: 'preview',
      courseTypeOptions: COURSE_TYPE_OPTIONS.map(t => ({ label: t.label, value: t.value })),
      semesterOptions: ['大一上','大一下','大二上','大二下','大三上','大三下','大四上','大四下'].map(s => ({ label: s, value: s })),
      adminLoading: false,
      adminCourses: [],
      adminAllCourses: [],
      adminMajors: [],
      adminColleges: [],
      adminSearchKeyword: '',
      adminSelectedMajor: null,
      adminSelectedCollege: null,
      adminTeacherKeyword: '',
      adminCurrentPage: 1,
      adminPageSize: 20,
      adminSearchMode: 'course',
      showPreviewDetailDialog: false,
      selectedPreviewCourse: null,
      previewSelectedMajor: null,
      // CS search
      csAdminTeacherKeyword: '',
      csAdminAllCourses: [],
      csAdminTeachers: [],
      csAdminFilteredTeachers: [],
      csAdminCurrentPage: 1,
      csAdminPageSize: 12,
      // Course management
      manageSearchKeyword: '',
      manageSelectedMajor: null,
      manageSelectedTeacher: null,
      manageAllCourses: [],
      manageFilteredCourses: [],
      showCourseDialog: false,
      showEditDialog: false,
      courseForm: { name: '', credit: 3.0, college: '', assessment_method: '闭卷笔试', order_num: 0, major_ids: [], teacher_names: '', course_types: [], semesters: [], description: '' },
      editCourseForm: { id: null, name: '', credit: 3.0, college: '', assessment_method: '闭卷笔试', order_num: 0, major_ids: [], teacher_names: '', course_types: [], semesters: [], description: '' },
      manageDebounceTimer: null,
      manageTeachers: []
    }
  },
  computed: {
    navItems() {
      const items = [
        { label: '课程预览', key: 'preview' },
        { label: '课程管理', key: 'manage' },
        { label: '数据分析', key: 'analysis' }
      ]
      if (this.role === 'superadmin') {
        items.push({ label: '账户管理', key: 'users' })
      }
      return items
    },
    menuOptions() {
      const items = [
        { label: '模拟选课', key: 'simulated' },
        { label: '数据分析', key: 'analysis_page' },
        { label: '用户中心', key: 'userCenter' },
        { label: '反馈', key: 'feedback' },
        { label: '设置', key: 'settings' },
        { type: 'divider', key: 'd1' },
        { label: '退出', key: 'logout' }
      ]
      if (this.role === 'superadmin') {
        items.unshift({ label: '账户管理', key: 'users' })
      }
      return items
    },
    adminMajorOptions() {
      return this.adminMajors.map(m => ({ label: m.name, value: m.id }))
    },
    adminCollegeOptions() {
      return this.adminColleges.map(c => ({ label: c, value: c }))
    },
    paginatedAdminCourses() {
      const start = (this.adminCurrentPage - 1) * this.adminPageSize
      return this.adminCourses.slice(start, start + this.adminPageSize)
    },
    adminTotalPages() {
      return Math.ceil(this.adminCourses.length / this.adminPageSize)
    },
    manageTeacherOptions() {
      const names = [...new Set(this.manageAllCourses.map(c => c.teacher_names).filter(Boolean))]
      return names.map(n => ({ label: n, value: n }))
    },
    manageColumns() {
      return [
        { title: 'ID', key: 'id', width: 60 },
        { title: '课程名', key: 'name', width: 200, ellipsis: { tooltip: true } },
        { title: '专业', key: 'major_names', width: 150, ellipsis: { tooltip: true } },
        { title: '教师', key: 'teacher_names', width: 150, ellipsis: { tooltip: true } },
        { title: '学分', key: 'credit', width: 60 },
        { title: '开课学院', key: 'college', width: 120, ellipsis: { tooltip: true } },
        { title: '开课学期', key: 'semesters', width: 160, render: row => (row.semesters || []).join('、') },
        {
          title: '操作',
          key: 'actions',
          width: 180,
          render: row => h('span', null, [
            h('n-button', { size: 'small', type: 'primary', style: 'margin-right:6px', onClick: () => this.handleEdit(row) }, () => '编辑'),
            h('n-button', { size: 'small', type: 'error', style: 'margin-right:6px', onClick: () => this.handleDelete(row) }, () => '删除'),
            h('n-button', { size: 'small', style: 'margin-right:6px', onClick: () => this.copyFrom(row) }, () => '复用')
          ])
        }
      ]
    },
    paginatedCsAdminTeachers() {
      const start = (this.csAdminCurrentPage - 1) * this.csAdminPageSize
      return this.csAdminFilteredTeachers.slice(start, start + this.csAdminPageSize)
    }
  },
  async mounted() {
    await this.loadAdminMajors()
    await this.loadAdminCourses()
    this.adminColleges = [...new Set(this.adminAllCourses.map(c => c.college).filter(Boolean))]
  },
  methods: {
    async loadAdminMajors() {
      try { this.adminMajors = await request.get('/majors') } catch {}
    },
    async loadAdminCourses() {
      this.adminLoading = true
      try {
        const params = {}
        if (this.adminSelectedMajor) params.major_id = this.adminSelectedMajor
        this.adminAllCourses = await request.get('/courses', { params })
        this.manageAllCourses = [...this.adminAllCourses]
        this.filterAdminCourses()
        this.filterManage()
      } catch { this.message.error('加载课程失败') } finally { this.adminLoading = false }
    },
    filterAdminCourses() {
      let f = [...this.adminAllCourses]
      if (this.adminSelectedCollege) f = f.filter(c => c.college === this.adminSelectedCollege)
      if (this.adminSearchKeyword) {
        const kw = this.adminSearchKeyword.toLowerCase()
        f = f.filter(c => c.name.toLowerCase().includes(kw))
      }
      if (this.adminTeacherKeyword) {
        const kw = this.adminTeacherKeyword.toLowerCase()
        f = f.filter(c => c.teacher_names && c.teacher_names.toLowerCase().includes(kw))
      }
      this.adminCourses = f
      this.adminCurrentPage = 1
    },
    debounceFilterAdminCourses() {
      if (this.manageDebounceTimer) clearTimeout(this.manageDebounceTimer)
      this.manageDebounceTimer = setTimeout(() => this.filterAdminCourses(), 300)
    },
    showPreviewDetail(course) {
      this.selectedPreviewCourse = course
      this.showPreviewDetailDialog = true
    },
    handleAdminTabChange(tab) {
      if (tab === 'cs_course') this.loadCsAdminCourses()
    },
    async loadCsAdminCourses() {
      this.csAdminAllCourses = await request.get('/courses', { params: { sort: 'asc', sort_by: 'order_num' } })
      this.csAdminAllCourses = this.csAdminAllCourses.filter(c => !c.college || c.college === '' || c.college === '计算机与人工智能学院')
      this.csAdminTeachers = this.getCsAdminUniqueTeachers(this.csAdminAllCourses)
      this.csAdminFilteredTeachers = [...this.csAdminTeachers]
    },
    getCsAdminUniqueTeachers(courses) {
      const map = new Map()
      courses.forEach(c => {
        if (c.teacher_ids && c.teacher_names) {
          const ids = Array.isArray(c.teacher_ids) ? c.teacher_ids : String(c.teacher_ids).split(',').map(s => s.trim())
          const names = Array.isArray(c.teacher_names) ? c.teacher_names : String(c.teacher_names).split(',')
          ids.forEach((id, i) => {
            if (!map.has(String(id))) map.set(String(id), { id: String(id), name: names[i]?.trim() || '' })
          })
        }
      })
      return Array.from(map.values())
    },
    filterCsAdminTeachers() {
      const kw = this.csAdminTeacherKeyword.toLowerCase()
      if (!kw) { this.csAdminFilteredTeachers = [...this.csAdminTeachers]; return }
      this.csAdminFilteredTeachers = this.csAdminTeachers.filter(t => t.name.toLowerCase().includes(kw))
    },
    getCsAdminTeacherCourses(tid) {
      return this.csAdminAllCourses.filter(c => {
        if (!c.teacher_ids) return false
        const ids = Array.isArray(c.teacher_ids) ? c.teacher_ids.map(String) : String(c.teacher_ids).split(',').map(s => s.trim())
        return ids.includes(tid)
      })
    },
    getAdminTeacherName(tid) {
      const t = this.adminMajors.length ? null : null
      return '教师'
    },
    handleMenuCommand(cmd) {
      switch (cmd) {
        case 'simulated': this.$router.push('/simulated-selection'); break
        case 'analysis_page': this.$router.push('/data-analysis'); break
        case 'users': this.$router.push('/user-management'); break
        case 'feedback': this.$router.push('/feedback'); break
        case 'userCenter': this.$router.push('/user-center'); break
        case 'settings': this.showSettingsDialog = true; break
        case 'logout': this.handleLogout(); break
      }
    },
    handleMenuChange(key) {
      if (key === 'users') this.$router.push('/user-management')
      else if (key === 'analysis') this.$router.push('/data-analysis')
    },
    handleLogout() {
      this.dialog.info({ title: '提示', content: '确定要退出吗？', positiveText: '确定', negativeText: '取消', onPositiveClick: () => {
        localStorage.clear(); clearCache(); this.$router.push('/login')
      }})
    },
    async handleAdminPageChange(p) { this.adminCurrentPage = p; window.scrollTo({ top: 0, behavior: 'smooth' }) },
    // Manage
    filterManage() {
      let f = [...this.manageAllCourses]
      if (this.manageSearchKeyword) f = f.filter(c => c.name.toLowerCase().includes(this.manageSearchKeyword.toLowerCase()))
      if (this.manageSelectedMajor) f = f.filter(c => c.majors?.some(m => m.id === this.manageSelectedMajor))
      if (this.manageSelectedTeacher) f = f.filter(c => c.teacher_names === this.manageSelectedTeacher)
      this.manageFilteredCourses = f
    },
    debounceFilterManage() {
      if (this.manageDebounceTimer) clearTimeout(this.manageDebounceTimer)
      this.manageDebounceTimer = setTimeout(() => this.filterManage(), 300)
    },
    showAddCourseDialog() {
      this.courseForm = { name: '', credit: 3.0, college: '', assessment_method: '闭卷笔试', order_num: 0, major_ids: [], teacher_names: '', course_types: [], semesters: [], description: '' }
      this.showCourseDialog = true
    },
    async submitCourse() {
      const f = this.courseForm
      if (!f.name || f.major_ids.length === 0 || !f.teacher_names || f.course_types.length === 0 || f.semesters.length === 0) {
        this.message.warning('请填写完整信息'); return
      }
      try {
        await request.post('/courses', f)
        this.message.success('课程创建成功'); this.showCourseDialog = false
        await this.loadAdminCourses()
      } catch (e) { this.message.error(e.response?.data?.msg || '创建失败') }
    },
    handleEdit(row) {
      this.editCourseForm = {
        id: row.id, name: row.name, credit: row.credit, college: row.college || '',
        assessment_method: row.assessment_method || '闭卷笔试', order_num: row.order_num || 0,
        major_ids: row.majors?.map(m => m.id) || [],
        teacher_names: row.teacher_names || '',
        course_types: row.course_types || [],
        semesters: row.semesters || [],
        description: row.description || ''
      }
      this.showEditDialog = true
    },
    async submitEdit() {
      const f = this.editCourseForm
      if (!f.name || f.major_ids.length === 0 || !f.teacher_names || f.course_types.length === 0 || f.semesters.length === 0) {
        this.message.warning('请填写完整信息'); return
      }
      try {
        await request.put(`/courses/${f.id}`, f)
        this.message.success('课程更新成功'); this.showEditDialog = false
        await this.loadAdminCourses()
      } catch (e) { this.message.error(e.response?.data?.msg || '更新失败') }
    },
    copyFrom(row) {
      this.courseForm = {
        name: row.name + '（复制）', credit: row.credit, college: row.college || '',
        assessment_method: row.assessment_method || '闭卷笔试', order_num: (row.order_num || 0) + 1,
        major_ids: row.majors?.map(m => m.id) || [],
        teacher_names: row.teacher_names || '',
        course_types: row.course_types || [],
        semesters: row.semesters || [],
        description: row.description || ''
      }
      this.showCourseDialog = true
    },
    handleDelete(row) {
      this.dialog.warning({
        title: '确认删除',
        content: `确定要删除课程「${row.name}」吗？`,
        positiveText: '确定', negativeText: '取消',
        onPositiveClick: async () => {
          try {
            await request.delete(`/courses/${row.id}`)
            this.message.success('课程已删除')
            await this.loadAdminCourses()
          } catch (e) { this.message.error(e.response?.data?.msg || '删除失败') }
        }
      })
    }
  }
})
</script>

<style scoped>
.dashboard { min-height: 100vh; }
.header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(0,0,0,0.04);
  position: sticky; top: 0; z-index: 100;
}
.header-left { display: flex; align-items: center; gap: 12px; }
.logo { width: 36px; height: 36px; border-radius: 8px; }
.header h2 { font-size: 18px; font-weight: 600; color: #333; }
.header-right { display: flex; align-items: center; gap: 12px; }
.menu-btn {
  display: flex; align-items: center; justify-content: center;
  width: 36px; height: 36px; border-radius: 8px; cursor: pointer;
  color: #666; transition: background 0.2s;
}
.menu-btn:hover { background: rgba(0,0,0,0.04); }
.main { padding: 20px 24px; max-width: 1400px; margin: 0 auto; }
.card-header { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }
.course-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.skeleton-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.course-card { cursor: pointer; }
.course-card-header { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
.course-name { font-weight: 600; font-size: 15px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.course-info p { margin-bottom: 6px; font-size: 13px; line-height: 1.6; }
.course-desc { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.rating-item { margin-bottom: 4px; font-size: 13px; display: flex; align-items: center; gap: 4px; }
.pagination-wrap { display: flex; justify-content: center; margin-top: 24px; }
.teacher-card-header { display: flex; justify-content: space-between; align-items: center; }
.teacher-name { font-weight: 600; font-size: 16px; }
.teacher-courses-list { max-height: 200px; overflow-y: auto; }
.teacher-course-item { padding: 6px 8px; border-radius: 6px; cursor: pointer; transition: background 0.2s; margin-bottom: 4px; font-size: 13px; }
.teacher-course-item:hover { background: rgba(0,0,0,0.04); }
html.dark-mode .header { background: rgba(25,25,45,0.85); }
html.dark-mode .header h2 { color: #e8e8e8; }
html.dark-mode .teacher-course-item:hover { background: rgba(255,255,255,0.06); }
@media (max-width:768px) { .main { padding: 12px; } .course-grid { grid-template-columns: 1fr; } }
</style>
