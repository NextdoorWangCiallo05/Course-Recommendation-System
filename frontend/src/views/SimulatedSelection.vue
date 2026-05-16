<template>
  <div class="simulated-selection">
    <div class="header">
      <div class="header-left">
        <img src="/images/logo.png" class="logo" alt="logo">
        <h2>模拟选课</h2>
      </div>
      <div class="header-right">
        <n-text depth="3">欢迎, {{ username }}</n-text>
        <n-button size="small" @click="goBack">返回</n-button>
      </div>
    </div>

    <div class="main">
      <n-card title="选课信息">
        <div class="selection-grid">
          <n-form-item label="专业">
            <n-select v-model:value="selectedMajor" placeholder="请选择专业" :options="majorOptions" @update:value="onMajorChange" />
          </n-form-item>
          <n-form-item v-if="subMajorOptions.length > 0" label="专业方向">
            <n-select v-model:value="selectedSubMajor" placeholder="请选择方向" clearable :options="subMajorOptions" />
          </n-form-item>
          <n-form-item v-if="classTypeOptions.length > 0" label="行政班级">
            <n-select v-model:value="selectedClassType" placeholder="请选择班级" clearable :options="classTypeOptions" />
          </n-form-item>
        </div>
        <n-button type="primary" @click="startSelection" :disabled="!selectedMajor">开始选课</n-button>
      </n-card>

      <n-card v-if="currentStep > 1" :title="stepTitle" style="margin-top:16px">
        <div class="step-selector">
          <n-steps :current="currentStep - 2" :status="stepStatus" @update:current="goToStep">
            <n-step title="通识必修" />
            <n-step title="英语必修" />
            <n-step title="体育必修" />
            <n-step title="学科必修" />
            <n-step title="专业必修" />
            <n-step title="专业选修" />
            <n-step title="实践课" />
            <n-step title="通识选修" />
            <n-step title="个性课程" />
            <n-step title="选课清单" />
          </n-steps>
        </div>

        <n-divider />
        <div v-if="loading" style="text-align:center;padding:40px"><n-spin size="large" /></div>

        <div v-if="!loading">
          <!-- 通用课程渲染 -->
          <div v-if="currentStep <= 9">
            <n-checkbox-group v-model:value="selectedCourseIds" @update:value="onSelectionChange">
              <div v-for="course in currentCourses" :key="course.id" class="course-select-item">
                <n-card size="small" :class="{ 'course-selected': selectedCourseIds.includes(course.id) }">
                  <n-checkbox :value="course.id" :disabled="isFixedPECourse(course.name)">
                    <div class="course-checkbox-content">
                      <span class="course-name-text">{{ course.name }}</span>
                      <span class="course-meta">{{ course.credit }} 学分</span>
                      <n-tag v-if="course.college" size="tiny" type="info">{{ course.college }}</n-tag>
                      <n-tag v-if="isFixedPECourse(course.name)" size="tiny" type="warning">必修</n-tag>
                      <n-tag v-if="isIntermediatePECourse(course.name)" size="tiny" type="info">需先修初级</n-tag>
                    </div>
                  </n-checkbox>
                  <div v-if="selectedCourseIds.includes(course.id) || isFixedPECourse(course.name)" class="course-extras">
                    <div class="teacher-select">
                      <n-select v-model:value="getSelection(course.id).teacherId" placeholder="选择教师" :options="getTeacherOptions(course)" size="small" style="width:200px" />
                    </div>
                    <div v-if="!isPECourse(course.name)" class="semester-select">
                      <n-select v-model:value="getSelection(course.id).semester" placeholder="选择学期" :options="semesterOptions" size="small" style="width:200px" />
                    </div>
                  </div>
                </n-card>
              </div>
            </n-checkbox-group>
            <n-empty v-if="currentCourses.length === 0" description="暂无课程" />
          </div>

          <!-- 体育课特殊处理 -->
          <div v-if="currentStep === 4">
            <n-alert type="info" :closable="false" style="margin-bottom:16px">体育课需选择2门（1门初级 + 1门中级）</n-alert>
          </div>

          <!-- 个性课特殊处理 -->
          <div v-if="currentStep === 10">
            <n-checkbox-group v-model:value="selectedCourseIds" @update:value="onSelectionChange">
              <div v-for="course in currentCourses" :key="course.id" class="course-select-item">
                <n-card size="small" :class="{ 'course-selected': selectedCourseIds.includes(course.id) }">
                  <n-checkbox :value="course.id">
                    <div class="course-checkbox-content">
                      <span class="course-name-text">{{ course.name }}</span>
                      <span class="course-meta">{{ course.credit }} 学分</span>
                      <n-tag v-if="isPlaceholderIndividualCourse(course.name)" size="tiny" type="warning">个性课</n-tag>
                    </div>
                  </n-checkbox>
                  <div v-if="selectedCourseIds.includes(course.id)" class="course-extras">
                    <div class="teacher-select">
                      <n-select v-model:value="getSelection(course.id).teacherId" placeholder="选择教师" :options="getTeacherOptions(course)" size="small" style="width:200px" />
                    </div>
                    <div v-if="isPlaceholderIndividualCourse(course.name)" class="quantity-select">
                      <n-input-number v-model:value="getSelection(course.id).quantity" :min="0" :max="20" size="small" />
                      <n-text depth="3" style="margin-left:8px;font-size:13px">门</n-text>
                    </div>
                  </div>
                </n-card>
              </div>
            </n-checkbox-group>
            <n-empty v-if="currentCourses.length === 0" description="暂无课程" />
          </div>

          <!-- 选课清单 -->
          <div v-if="currentStep === 11">
            <n-card size="small" style="margin-bottom:16px">
              <n-descriptions :column="3" label-placement="left" bordered size="small">
                <n-descriptions-item label="专业">{{ getMajorLabel(selectedMajor) }}</n-descriptions-item>
                <n-descriptions-item v-if="selectedSubMajor" label="方向">{{ getSubMajorLabel(selectedSubMajor) }}</n-descriptions-item>
                <n-descriptions-item v-if="selectedClassType" label="班级">{{ getClassTypeLabel(selectedClassType) }}</n-descriptions-item>
                <n-descriptions-item label="总学分">{{ totalSelectedCreditsWithIndividual }}</n-descriptions-item>
              </n-descriptions>
            </n-card>

            <n-data-table :columns="summaryColumns" :data="summaryCourses" :bordered="false" :single-line="false" size="small" />
          </div>
        </div>

        <n-divider v-if="currentStep > 1 && currentStep < 11" />
        <n-space v-if="currentStep > 1" justify="space-between">
          <n-button v-if="currentStep > 2" @click="prevStep">上一步</n-button>
          <n-button v-if="currentStep < 11" type="primary" @click="nextStep">下一步</n-button>
          <n-button v-if="currentStep === 11" type="success" @click="exportSummary">导出清单</n-button>
        </n-space>
      </n-card>
    </div>
  </div>
</template>

<script>
import { defineComponent, h } from 'vue'
import { useMessage } from 'naive-ui'
import request from '../api'

const courseTypeMap = {
  3: '通识必修', 4: '英语必修', 5: '体育必修', 6: '学科必修',
  7: '专业必修', 8: '专业选修', 9: '实践课', 10: '通识选修', 11: '个性课程'
}

export default defineComponent({
  setup() {
    const message = useMessage()
    return { message }
  },
  data() {
    return {
      username: localStorage.getItem('username') || '',
      majors: [],
      selectedMajor: null,
      selectedSubMajor: null,
      selectedClassType: null,
      currentStep: 1,
      loading: false,
      selectedCourseIds: [],
      courseSelections: {},
      allCourses: [],
      generalCourses: [],
      englishCourses: [],
      peCourses: [],
      academicCourses: [],
      majorRequiredCourses: [],
      majorElectiveCourses: [],
      practiceCourses: [],
      generalElectiveCourses: [],
      individualCourses: [],
      semesterOptions: ['大一上','大一下','大二上','大二下','大三上','大三下','大四上','大四下'].map(s => ({ label: s, value: s })),
      peCourseSelections: {},
      generalCourseSelections: {},
      englishCourseSelections: {},
      academicCourseSelections: {},
      majorRequiredCourseSelections: {},
      majorElectiveCourseSelections: {},
      practiceCourseSelections: {},
      generalElectiveCourseSelections: {},
      individualCourseSelections: {},
    }
  },
  computed: {
    majorOptions() {
      return this.majors.map(m => ({ label: m.name, value: m.id }))
    },
    subMajorOptions() { return [] },
    classTypeOptions() { return [] },
    stepTitle() {
      return courseTypeMap[this.currentStep] || (this.currentStep === 11 ? '选课清单' : '')
    },
    stepStatus() {
      return this.currentStep >= 11 ? 'finish' : 'process'
    },
    currentCourses() {
      const map = {
        3: this.generalCourses, 4: this.englishCourses, 5: this.peCourses,
        6: this.academicCourses, 7: this.majorRequiredCourses, 8: this.majorElectiveCourses,
        9: this.practiceCourses, 10: this.generalElectiveCourses, 11: this.individualCourses
      }
      return map[this.currentStep] || []
    },
    selectedCount() {
      return this.selectedCourseIds.length
    },
    totalCredits() {
      let total = 0
      this.selectedCourseIds.forEach(id => {
        const course = this.allCourses.find(c => c.id === id)
        if (course) total += course.credit
      })
      return total
    },
    summaryCourses() {
      const courses = []
      const addCourse = (course, sel, category) => {
        if (!sel) return
        const teacherNames = course.teacher_names ? course.teacher_names.split(',') : []
        const teacherIds = course.teacher_ids || []
        const teacherIndex = teacherIds.indexOf(sel.teacherId)
        const teacherName = teacherIndex >= 0 ? teacherNames[teacherIndex] : '待定'
        courses.push({
          category,
          name: course.name,
          teacher: teacherName || '待定',
          semester: this.semesterOptions.find(s => s.value === sel.semester)?.label || sel.semester || '',
          credit: course.credit
        })
      }
      this.generalCourses.forEach(c => addCourse(c, this.generalCourseSelections[c.id], '通识必修'))
      this.englishCourses.forEach(c => addCourse(c, this.englishCourseSelections[c.id], '英语必修'))
      this.peCourses.forEach(c => addCourse(c, this.peCourseSelections[c.id], '体育必修'))
      this.academicCourses.forEach(c => addCourse(c, this.academicCourseSelections[c.id], '学科必修'))
      this.majorRequiredCourses.forEach(c => addCourse(c, this.majorRequiredCourseSelections[c.id], '专业必修'))
      this.majorElectiveCourses.forEach(c => addCourse(c, this.majorElectiveCourseSelections[c.id], '专业选修'))
      this.practiceCourses.forEach(c => addCourse(c, this.practiceCourseSelections[c.id], '实践课'))
      this.generalElectiveCourses.forEach(c => addCourse(c, this.generalElectiveCourseSelections[c.id], '通识选修'))
      this.individualCourses.forEach(c => addCourse(c, this.individualCourseSelections[c.id], '个性课程'))
      return courses
    },
    totalSelectedCreditsWithIndividual() {
      let total = 0
      this.summaryCourses.forEach(c => { total += c.credit || 0 })
      return total.toFixed(1)
    },
    summaryColumns() {
      return [
        { title: '序号', key: 'index', width: 60, render: (_, i) => i + 1 },
        { title: '课程类别', key: 'category', width: 110 },
        { title: '课程名称', key: 'name', ellipsis: { tooltip: true } },
        { title: '授课教师', key: 'teacher', width: 120 },
        { title: '修读学期', key: 'semester', width: 120 },
        { title: '学分', key: 'credit', width: 70 }
      ]
    }
  },
  async mounted() {
    try { this.majors = await request.get('/majors') } catch { this.message.error('加载专业失败') }
  },
  methods: {
    goBack() {
      const role = localStorage.getItem('role')
      this.$router.push(role === 'admin' || role === 'superadmin' ? '/admin' : '/student')
    },
    getMajorLabel(id) { const m = this.majors.find(m => m.id === id); return m ? m.name : '未知' },
    getSubMajorLabel(id) { return '' },
    getClassTypeLabel(id) { return '' },
    getBackendMajorId() { return this.selectedMajor },
    onMajorChange() {
      this.selectedSubMajor = null
      this.selectedClassType = null
    },
    async startSelection() {
      this.currentStep = 2
      await this.loadStepCourses(3)
    },
    async loadStepCourses(step) {
      this.loading = true
      try {
        const courseType = courseTypeMap[step]
        const params = { course_type: courseType }
        if ([6, 7, 8, 9].includes(step)) params.major_id = this.getBackendMajorId()
        const response = await request.get('/courses', { params })
        switch (step) {
          case 3: this.generalCourses = response; break
          case 4: this.englishCourses = response; break
          case 5: this.peCourses = response; this.initPESelections(); break
          case 6: this.academicCourses = response; break
          case 7: this.majorRequiredCourses = response; break
          case 8: this.majorElectiveCourses = response; break
          case 9: this.practiceCourses = response; break
          case 10: this.generalElectiveCourses = response; break
          case 11: this.individualCourses = response; break
        }
      } catch { this.message.error('加载课程失败') } finally { this.loading = false }
    },
    async nextStep() {
      if (this.currentStep < 11) {
        const next = this.currentStep + 1
        if (next <= 11) await this.loadStepCourses(next)
        this.currentStep = next
      }
    },
    async prevStep() {
      if (this.currentStep > 2) this.currentStep--
    },
    goToStep(index) {
      if (index + 3 <= 11) this.currentStep = index + 3
    },
    onSelectionChange() {
      this.initSelectionData()
    },
    getSelection(courseId) {
      if (!this.courseSelections[courseId]) {
        this.courseSelections[courseId] = { teacherId: null, semester: '', quantity: 1 }
      }
      return this.courseSelections[courseId]
    },
    getTeacherOptions(course) {
      const names = course.teacher_names ? course.teacher_names.split(',') : []
      const ids = course.teacher_ids || []
      return ids.map((id, i) => ({ label: names[i] || `教师${id}`, value: id }))
    },
    initSelectionData() {
      const allCourses = [...this.generalCourses, ...this.englishCourses, ...this.peCourses,
        ...this.academicCourses, ...this.majorRequiredCourses, ...this.majorElectiveCourses,
        ...this.practiceCourses, ...this.generalElectiveCourses, ...this.individualCourses]
      this.allCourses = allCourses
    },
    initPESelections() {
      this.peCourses.forEach(c => {
        if (!this.peCourseSelections[c.id]) {
          this.peCourseSelections[c.id] = { teacherId: null, semester: '' }
        }
      })
    },
    isPECourse(name) { return name.includes('体育') },
    isFixedPECourse(name) { return name.includes('体育') && !name.includes('(初)') && !name.includes('(中)') },
    isIntermediatePECourse(name) { return name.includes('(中)') },
    isPlaceholderIndividualCourse(name) { return name.includes('学分个性课') },
    exportSummary() {
      const semesterMap = {
        '大一上': '大一上学期', '大一下': '大一下学期',
        '大二上': '大二上学期', '大二下': '大二下学期',
        '大三上': '大三上学期', '大三下': '大三下学期',
        '大四上': '大四上学期', '大四下': '大四下学期'
      }
      let text = '===== 选课清单 =====\n\n'
      text += `专业: ${this.getMajorLabel(this.selectedMajor)}\n`
      if (this.selectedSubMajor) text += `方向: ${this.getSubMajorLabel(this.selectedSubMajor)}\n`
      if (this.selectedClassType) text += `班级: ${this.getClassTypeLabel(this.selectedClassType)}\n`
      text += `总学分: ${this.totalSelectedCreditsWithIndividual}\n\n`
      text += '序号\t课程类别\t课程名称\t授课教师\t修读学期\t学分\n'
      this.summaryCourses.forEach((c, i) => {
        const sem = semesterMap[c.semester] || c.semester
        text += `${i+1}\t${c.category}\t${c.name}\t${c.teacher}\t${sem}\t${c.credit}\n`
      })
      const blob = new Blob([text], { type: 'text/plain;charset=utf-8' })
      const a = document.createElement('a')
      a.href = URL.createObjectURL(blob)
      a.download = '选课清单.txt'
      a.click()
      URL.revokeObjectURL(a.href)
    }
  }
})
</script>

<style scoped>
.simulated-selection { min-height: 100vh; }
.header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 24px; background: rgba(255,255,255,0.85); backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(0,0,0,0.04); position: sticky; top: 0; z-index: 100;
}
.header-left { display: flex; align-items: center; gap: 12px; }
.logo { width: 36px; height: 36px; border-radius: 8px; }
.header h2 { font-size: 18px; font-weight: 600; color: #333; }
.header-right { display: flex; align-items: center; gap: 12px; }
.main { padding: 20px 24px; max-width: 1000px; margin: 0 auto; }
.selection-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px; }
@media (max-width:768px) { .selection-grid { grid-template-columns: 1fr; } }
.step-selector { margin-bottom: 16px; }
.course-select-item { margin-bottom: 8px; }
.course-selected { border: 1px solid #2080F0; }
.course-checkbox-content { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.course-name-text { font-weight: 500; }
.course-meta { color: #666; font-size: 13px; }
.course-extras { display: flex; gap: 12px; margin-top: 10px; flex-wrap: wrap; }
.teacher-select, .semester-select, .quantity-select { display: flex; align-items: center; }
html.dark-mode .header { background: rgba(25,25,45,0.85); }
html.dark-mode .header h2 { color: #e8e8e8; }
@media (max-width:768px) { .main { padding: 12px; } }
</style>
