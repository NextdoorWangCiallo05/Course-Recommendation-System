<template>
  <div class="simulated-selection">
    <div class="header">
      <div class="header-left">
        <img src="/images/logo.png" class="logo" alt="logo">
        <h2>模拟选课</h2>
      </div>
      <div class="header-right">
        <n-text depth="3">欢迎, {{ username }}</n-text>
        <n-button size="small" @click="goHome">返回主页</n-button>
        <n-button size="small" @click="resetSelection">重新选择</n-button>
      </div>
    </div>

    <div class="main">
      <n-card>
        <template #header>
          <div class="card-header">
            <n-steps :current="currentStep" :status="stepStatus" class="multi-row-steps">
              <n-step title="选择专业" />
              <n-step title="选择方向" />
              <n-step title="选择班级" />
              <n-step title="通识必修" />
              <n-step title="英语班级" />
              <n-step title="英语必修" />
              <n-step title="体育必修" />
              <n-step title="学科必修" />
              <n-step title="专业必修" />
              <n-step title="专业选修" />
              <n-step title="实践课" />
              <n-step title="通识选修" />
              <n-step title="个性课程" />
              <n-step title="选课总结" />
            </n-steps>
          </div>
        </template>

        <!-- Step 0: 选择专业 -->
        <div v-if="currentStep === 0" class="step-content">
          <h3 class="step-title">请选择你的专业</h3>
          <div class="option-grid">
            <div v-for="major in majors" :key="major.value" class="option-card" :class="{ selected: selectedMajor === major.value }" @click="selectMajor(major.value)">
              <div class="option-icon">{{ major.icon }}</div>
              <div class="option-name">{{ major.label }}</div>
            </div>
          </div>
        </div>

        <!-- Step 1: 选择方向 -->
        <div v-if="currentStep === 1" class="step-content">
          <h3 class="step-title">请选择具体方向</h3>
          <div class="option-grid">
            <div v-for="sub in subMajors" :key="sub.value" class="option-card" :class="{ selected: selectedSubMajor === sub.value }" @click="selectSubMajor(sub.value)">
              <div class="option-icon">{{ sub.icon }}</div>
              <div class="option-name">{{ sub.label }}</div>
            </div>
          </div>
        </div>

        <!-- Step 2: 选择班级 -->
        <div v-if="currentStep === 2" class="step-content">
          <h3 class="step-title">请选择班级类型</h3>
          <div class="option-grid two-col">
            <div v-for="cls in classTypes" :key="cls.value" class="option-card" :class="{ selected: selectedClassType === cls.value }" @click="selectClassType(cls.value)">
              <div class="option-icon">{{ cls.icon }}</div>
              <div class="option-name">{{ cls.label }}</div>
              <div class="option-desc">{{ cls.desc }}</div>
            </div>
          </div>
        </div>

        <!-- Step 3-12: 课程选择 -->
        <div v-for="stepNum in [3,5,6,7,8,9,10,11,12]" :key="'step-'+stepNum">
          <div v-if="currentStep === stepNum" class="step-content">
            <div class="selection-summary">
              <n-tag type="primary" size="small">专业: {{ getMajorLabel }}</n-tag>
              <n-tag v-if="selectedSubMajor" type="success" size="small">方向: {{ getSubMajorLabel }}</n-tag>
              <n-tag v-if="selectedClassType" type="warning" size="small">班级: {{ getClassTypeLabel }}</n-tag>
            </div>
            <div class="credit-scoreboard">
              <n-card size="small" :bordered="true">
                <div class="scoreboard-content">
                  <div class="score-item" v-for="item in creditBoard(stepNum)" :key="item.label">
                    <span class="score-label">{{ item.label }}</span>
                    <span class="score-value" :class="{ requirement: item.isReq }">{{ item.value }}</span>
                  </div>
                </div>
              </n-card>
              <n-alert v-if="creditMessage(stepNum)" :type="creditMessageType(stepNum)" :closable="false" size="small" class="credit-alert">{{ creditMessage(stepNum) }}</n-alert>
            </div>

            <div v-if="loading" class="loading-state"><n-spin size="large" /></div>
            <div v-else-if="courseList(stepNum).length === 0" class="empty-state"><n-empty description="暂无课程" /></div>

            <div v-else class="course-list">
              <n-card v-for="course in courseList(stepNum)" :key="course.id" size="small" class="course-card" :class="{ 'course-selected': getSel(stepNum, course.id).selected }">
                <template #header>
                  <div class="course-header">
                    <n-checkbox v-model:checked="getSel(stepNum, course.id).selected" size="medium" class="course-checkbox" :disabled="isFixedCourse(stepNum, course.name)" @update:checked="(val) => onCourseChange(stepNum, course, val)">
                      <span class="course-name">{{ course.name }}</span>
                    </n-checkbox>
                    <div class="course-info-tags">
                      <span class="credit-tag">{{ course.credit }} 学分</span>
                      <n-tag v-if="course.college" size="tiny" type="info">{{ course.college }}</n-tag>
                      <n-tag v-if="isFixedCourse(stepNum, course.name)" size="tiny" type="warning">必修</n-tag>
                      <n-tag v-if="stepNum === 6 && isIntermediatePECourse(course.name)" size="tiny" type="info">需先修初级</n-tag>
                      <n-tag v-if="stepNum === 11 && isArtCourse(course)" size="tiny" type="success">艺术审美</n-tag>
                      <n-tag v-if="stepNum === 11 && isHistoryCourse(course)" size="tiny" type="info">四史</n-tag>
                      <n-tag v-if="stepNum === 11 && isInnovationCourse(course)" size="tiny" type="primary">创新创业</n-tag>
                    </div>
                  </div>
                </template>
                <div class="course-content">
                  <div class="course-desc">{{ course.description || '暂无课程描述' }}</div>
                  <div class="teacher-selection">
                    <n-radio-group v-model:value="getSel(stepNum, course.id).teacherId" size="small">
                      <n-radio v-for="(tid, idx) in (course.teacher_ids||[])" :key="tid" :value="tid" :style="{ marginRight: '12px', padding: '4px 0' }">
                        <span class="teacher-name">{{ (course.teacher_names||'').split(',')[idx] }}</span>
                      </n-radio>
                    </n-radio-group>
                  </div>
                  <div class="semester-selection">
                    <span class="field-label">修读学期：</span>
                    <n-select v-model:value="getSel(stepNum, course.id).semester" placeholder="请选择学期" :options="semesterOptions" size="small" style="width: 160px" />
                  </div>
                  <div v-if="stepNum === 11 && isPlaceholderCourse(course.name)" class="quantity-selection">
                    <span class="field-label">修读门数：</span>
                    <n-input-number v-model:value="getSel(stepNum, course.id).quantity" :min="0" :max="9" size="small" />
                    <span class="quantity-hint">（每门{{ course.credit }}学分）</span>
                  </div>
                  <div v-if="stepNum === 12 && isPlaceholderIndividualCourse(course.name)" class="quantity-selection">
                    <span class="field-label">修读门数：</span>
                    <n-input-number v-model:value="getSel(stepNum, course.id).quantity" :min="0" :max="9" size="small" />
                    <span class="quantity-hint">（每门{{ course.credit }}学分）</span>
                  </div>
                </div>
              </n-card>
            </div>

            <div v-if="stepNum === 11 && courseList(11).length > 0" class="category-filter">
              <span class="filter-label">分类筛选：</span>
              <n-radio-group v-model:value="generalElectiveCategoryFilter" size="small">
                <n-radio-button value="">全部 ({{ courseList(11).length }})</n-radio-button>
                <n-radio-button value="四史类">四史类</n-radio-button>
                <n-radio-button value="艺术审美类">艺术审美类</n-radio-button>
                <n-radio-button value="创新创业类">创新创业类</n-radio-button>
                <n-radio-button value="其他类">其他类</n-radio-button>
              </n-radio-group>
            </div>
          </div>
        </div>

        <!-- Step 4: 英语快/慢班选择 -->
        <div v-if="currentStep === 4" class="step-content">
          <div class="selection-summary">
            <n-tag type="primary" size="small">专业: {{ getMajorLabel }}</n-tag>
            <n-tag v-if="selectedSubMajor" type="success" size="small">方向: {{ getSubMajorLabel }}</n-tag>
            <n-tag v-if="selectedClassType" type="warning" size="small">班级: {{ getClassTypeLabel }}</n-tag>
          </div>
          <h3 class="step-title">请选择英语班级类型</h3>
          <div class="option-grid two-col">
            <div class="option-card" :class="{ selected: selectedEnglishClass === 'fast' }" @click="selectEnglishClass('fast')">
              <div class="option-icon">🚀</div>
              <div class="option-name">快班</div>
              <div class="option-desc">选择大学英语2、大学英语3 + 两门其他英语课程</div>
            </div>
            <div class="option-card" :class="{ selected: selectedEnglishClass === 'slow' }" @click="selectEnglishClass('slow')">
              <div class="option-icon">🐢</div>
              <div class="option-name">慢班</div>
              <div class="option-desc">选择大学英语1、大学英语2、大学英语3 + 一门其他英语课程</div>
            </div>
          </div>
        </div>

        <!-- Step 13: 选课总结 -->
        <div v-if="currentStep === 13" class="step-content">
          <div class="selection-summary">
            <n-tag type="primary" size="small">专业: {{ getMajorLabel }}</n-tag>
            <n-tag v-if="selectedSubMajor" type="success" size="small">方向: {{ getSubMajorLabel }}</n-tag>
            <n-tag v-if="selectedClassType" type="warning" size="small">班级: {{ getClassTypeLabel }}</n-tag>
          </div>
          <div class="summary-credit-total">
            <n-card size="small">
              <div class="scoreboard-content">
                <div class="score-item total">
                  <span class="score-label">选课总计</span>
                  <span class="score-value">{{ totalSelectedCreditsWithIndividual }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item"><span class="score-label">通识必修</span><span class="score-value">{{ selectedGeneralCredits }} 学分</span></div>
                <div class="score-divider"></div>
                <div class="score-item"><span class="score-label">英语必修</span><span class="score-value">{{ selectedEnglishCredits }} 学分</span></div>
                <div class="score-divider"></div>
                <div class="score-item"><span class="score-label">体育必修</span><span class="score-value">{{ selectedPECredits }} 学分</span></div>
                <div class="score-divider"></div>
                <div class="score-item"><span class="score-label">学科必修</span><span class="score-value">{{ selectedAcademicCredits }} 学分</span></div>
                <div class="score-divider"></div>
                <div class="score-item"><span class="score-label">专业必修</span><span class="score-value">{{ selectedMajorRequiredCredits }} 学分</span></div>
                <div class="score-divider"></div>
                <div class="score-item"><span class="score-label">专业选修</span><span class="score-value">{{ selectedMajorElectiveCredits }} 学分</span></div>
                <div class="score-divider"></div>
                <div class="score-item"><span class="score-label">实践课</span><span class="score-value">{{ selectedPracticeCredits }} 学分</span></div>
                <div class="score-divider"></div>
                <div class="score-item"><span class="score-label">通识选修</span><span class="score-value">{{ selectedGeneralElectiveCredits }} 学分</span></div>
                <div class="score-divider"></div>
                <div class="score-item"><span class="score-label">个性课程</span><span class="score-value">{{ selectedIndividualCredits }} 学分</span></div>
              </div>
            </n-card>
          </div>
          <div class="summary-table-wrapper">
            <h3 class="summary-title">选课清单</h3>
            <n-data-table :columns="summaryColumns" :data="summaryCourses" :bordered="true" :single-line="false" size="small" max-height="500" />
          </div>
        </div>

        <!-- 导航按钮 -->
        <div class="nav-buttons">
          <n-space justify="space-between">
            <n-button v-if="currentStep > 0 && currentStep < 3" @click="prevStep">上一步</n-button>
            <n-button v-if="currentStep === 3" @click="prevStep">上一步</n-button>
            <n-button v-if="currentStep > 3 && currentStep < 13" @click="prevStep">上一步</n-button>
            <n-button v-if="currentStep === 13" @click="prevStep">上一步</n-button>
            <span>
              <n-button v-if="currentStep === 0" type="primary" @click="nextStep" :disabled="!selectedMajor">下一步</n-button>
              <n-button v-if="currentStep === 1" type="primary" @click="nextStep">下一步</n-button>
              <n-button v-if="currentStep === 2" type="primary" @click="loadGeneralCourses">下一步</n-button>
              <n-button v-if="currentStep === 3" type="primary" @click="goToEnglishClassSelection">下一步</n-button>
              <n-button v-if="currentStep === 4" type="primary" @click="loadEnglishCourses" :disabled="!selectedEnglishClass">下一步</n-button>
              <n-button v-if="currentStep === 5" type="primary" @click="loadPECourses">下一步</n-button>
              <n-button v-if="currentStep === 6" type="primary" @click="loadAcademicCourses">下一步</n-button>
              <n-button v-if="currentStep === 7" type="primary" @click="handleAfterAcademic">下一步</n-button>
              <n-button v-if="currentStep === 8" type="primary" @click="loadMajorElectiveCourses">下一步</n-button>
              <n-button v-if="currentStep === 9" type="primary" @click="loadPracticeCourses">下一步</n-button>
              <n-button v-if="currentStep === 10" type="primary" @click="loadGeneralElectiveCourses">下一步</n-button>
              <n-button v-if="currentStep === 11" type="primary" @click="loadIndividualCourses">下一步</n-button>
              <n-button v-if="currentStep === 12" type="primary" @click="goToSummary">下一步</n-button>
              <n-button v-if="currentStep === 13" type="primary" @click="exportSummary">导出 TXT</n-button>
              <n-button v-if="currentStep === 13" type="success" @click="exportSummaryCSV">导出 CSV</n-button>
              <n-button v-if="currentStep === 13" type="warning" @click="resetSelection">重新选择</n-button>
            </span>
          </n-space>
        </div>
      </n-card>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { useMessage } from 'naive-ui'
import request from '../api'

export default defineComponent({
  setup() {
    const message = useMessage()
    return { message }
  },
  data() {
    return {
      username: '',
      currentStep: 0,
      selectedMajor: null,
      selectedSubMajor: null,
      selectedClassType: null,
      selectedEnglishClass: null,
      loading: false,
      generalCourses: [],
      englishCourses: [],
      peCourses: [],
      academicCourses: [],
      majorRequiredCourses: [],
      majorElectiveCourses: [],
      practiceCourses: [],
      generalElectiveCourses: [],
      individualCourses: [],
      generalCourseSelections: {},
      englishCourseSelections: {},
      peCourseSelections: {},
      academicCourseSelections: {},
      majorRequiredCourseSelections: {},
      majorElectiveCourseSelections: {},
      practiceCourseSelections: {},
      generalElectiveCourseSelections: {},
      individualCourseSelections: {},
      generalElectiveCategoryFilter: '',
      majors: [
        { value: 'computer_category', label: '计算机类', icon: '💻' },
        { value: 'ai', label: '人工智能', icon: '🤖' },
        { value: 'software_exp', label: '软件（实验）', icon: '🔧' },
        { value: 'ai_exp', label: '人工智能（实验）', icon: '🧪' }
      ],
      subMajors: [
        { value: 'computer', label: '计算机', icon: '🖥️' },
        { value: 'software', label: '软件', icon: '💾' },
        { value: 'big_data', label: '大数据', icon: '📊' }
      ],
      classTypes: [
        { value: 'normal', label: '普通班', icon: '📚', desc: '常规教学班级' },
        { value: 'excellence', label: '卓越工程师', icon: '⭐', desc: '卓越工程师培养计划' }
      ],
      semesterOptions: ['大一上','大一下','大二上','大二下','大三上','大三下','大四上','大四下'].map(s => ({ label: s, value: s }))
    }
  },
  computed: {
    getMajorLabel() {
      const m = this.majors.find(m => m.value === this.selectedMajor)
      return m ? m.label : '未知'
    },
    getSubMajorLabel() {
      const m = this.subMajors.find(m => m.value === this.selectedSubMajor)
      return m ? m.label : ''
    },
    getClassTypeLabel() {
      const m = this.classTypes.find(m => m.value === this.selectedClassType)
      return m ? m.label : ''
    },
    stepStatus() {
      return this.currentStep >= 13 ? 'finish' : 'process'
    },
    electiveCreditRequirement() {
      const map = {
        computer: 23.5, software: 20.5, big_data: 22.5,
        ai: 24.5, software_exp: 21, ai_exp: 21
      }
      if (this.selectedSubMajor) return map[this.selectedSubMajor] || 0
      return map[this.selectedMajor] || 0
    },
    selectedGeneralCredits() { return this.calcCredits(this.generalCourses, this.generalCourseSelections) },
    selectedEnglishCredits() { return this.calcCredits(this.englishCourses, this.englishCourseSelections) },
    selectedPECredits() { return this.calcCredits(this.peCourses, this.peCourseSelections) },
    selectedAcademicCredits() { return this.calcCredits(this.academicCourses, this.academicCourseSelections) },
    selectedMajorRequiredCredits() { return this.calcCredits(this.majorRequiredCourses, this.majorRequiredCourseSelections) },
    selectedMajorElectiveCredits() { return this.calcCredits(this.majorElectiveCourses, this.majorElectiveCourseSelections) },
    selectedPracticeCredits() { return this.calcCredits(this.practiceCourses, this.practiceCourseSelections) },
    selectedGeneralElectiveCredits() {
      let total = 0
      this.generalElectiveCourses.forEach(course => {
        const sel = this.generalElectiveCourseSelections[course.id]
        if (sel && sel.selected) {
          const qty = (this.isPlaceholderCourse(course.name) && sel.quantity > 0) ? sel.quantity : 1
          total += parseFloat(course.credit) * qty
        }
      })
      return total
    },
    selectedIndividualCredits() {
      let total = 0
      this.individualCourses.forEach(course => {
        const sel = this.individualCourseSelections[course.id]
        if (sel && sel.selected) {
          const qty = (this.isPlaceholderIndividualCourse(course.name) && sel.quantity > 0) ? sel.quantity : 1
          total += parseFloat(course.credit) * qty
        }
      })
      return total
    },
    totalSelectedCredits() {
      return this.selectedGeneralCredits + this.selectedEnglishCredits + this.selectedPECredits + this.selectedAcademicCredits
    },
    totalSelectedCreditsWithIndividual() {
      return this.selectedGeneralCredits + this.selectedEnglishCredits + this.selectedPECredits +
        this.selectedAcademicCredits + this.selectedMajorRequiredCredits + this.selectedMajorElectiveCredits +
        this.selectedPracticeCredits + this.selectedGeneralElectiveCredits + this.selectedIndividualCredits
    },
    summaryCourses() {
      const list = []
      const add = (course, sel, category) => {
        if (!sel || !sel.selected) return
        const names = (course.teacher_names || '').split(',')
        const ids = course.teacher_ids || []
        const idx = ids.indexOf(sel.teacherId)
        list.push({
          category, name: course.name,
          teacher: idx >= 0 ? names[idx] : '待定',
          semester: sel.semester || '',
          credit: this.isPlaceholderIndividualCourse(course.name) ? (course.credit * (sel.quantity || 1)) : course.credit
        })
      }
      this.generalCourses.forEach(c => add(c, this.generalCourseSelections[c.id], '通识必修'))
      this.englishCourses.forEach(c => add(c, this.englishCourseSelections[c.id], '英语必修'))
      this.peCourses.forEach(c => add(c, this.peCourseSelections[c.id], '体育必修'))
      this.academicCourses.forEach(c => add(c, this.academicCourseSelections[c.id], '学科必修'))
      this.majorRequiredCourses.forEach(c => add(c, this.majorRequiredCourseSelections[c.id], '专业必修'))
      this.majorElectiveCourses.forEach(c => add(c, this.majorElectiveCourseSelections[c.id], '专业选修'))
      this.practiceCourses.forEach(c => add(c, this.practiceCourseSelections[c.id], '实践课'))
      this.generalElectiveCourses.forEach(c => add(c, this.generalElectiveCourseSelections[c.id], '通识选修'))
      this.individualCourses.forEach(c => add(c, this.individualCourseSelections[c.id], '个性课程'))
      return list
    },
    summaryColumns() {
      return [
        { title: '序号', key: 'index', width: 60, render: (_, i) => i + 1 },
        { title: '课程类别', key: 'category', width: 100 },
        { title: '课程名称', key: 'name', ellipsis: { tooltip: true } },
        { title: '授课教师', key: 'teacher', width: 120 },
        { title: '修读学期', key: 'semester', width: 100 },
        { title: '学分', key: 'credit', width: 70 }
      ]
    }
  },
  mounted() {
    this.username = localStorage.getItem('username') || ''
  },
  methods: {
    calcCredits(courses, selections) {
      let total = 0
      courses.forEach(course => {
        const sel = selections[course.id]
        if (sel && sel.selected) total += parseFloat(course.credit) || 0
      })
      return total
    },
    getSel(stepNum, courseId) {
      const map = {
        3: 'generalCourseSelections', 5: 'englishCourseSelections', 6: 'peCourseSelections',
        7: 'academicCourseSelections', 8: 'majorRequiredCourseSelections', 9: 'majorElectiveCourseSelections',
        10: 'practiceCourseSelections', 11: 'generalElectiveCourseSelections', 12: 'individualCourseSelections'
      }
      const key = map[stepNum]
      if (!this[key][courseId]) {
        this[key][courseId] = { selected: false, teacherId: null, semester: '', quantity: 1 }
        if (stepNum === 3 || stepNum === 7 || stepNum === 8) {
          this[key][courseId].selected = true
        }
      }
      return this[key][courseId]
    },
    courseList(stepNum) {
      const map = { 3: 'generalCourses', 5: 'englishCourses', 6: 'peCourses', 7: 'academicCourses',
        8: 'majorRequiredCourses', 9: 'majorElectiveCourses', 10: 'practiceCourses',
        11: 'generalElectiveCourses', 12: 'individualCourses' }
      let list = this[map[stepNum]] || []
      if (stepNum === 11) {
        const filter = this.generalElectiveCategoryFilter
        if (filter === '四史类') list = list.filter(c => this.isHistoryCourse(c))
        else if (filter === '艺术审美类') list = list.filter(c => this.isArtCourse(c))
        else if (filter === '创新创业类') list = list.filter(c => this.isInnovationCourse(c))
        else if (filter === '其他类') list = list.filter(c => !this.isHistoryCourse(c) && !this.isArtCourse(c) && !this.isInnovationCourse(c))
      }
      return list
    },
    creditBoard(stepNum) {
      const items = [
        { label: '通识必修已选', value: this.selectedGeneralCredits + ' 学分' },
        { label: '英语必修已选', value: this.selectedEnglishCredits + ' 学分' }
      ]
      if (stepNum >= 6) items.push({ label: '体育必修已选', value: this.selectedPECredits + ' 学分' })
      if (stepNum >= 6) items.push({ label: '体育要求', value: '4 学分', isReq: true })
      if (stepNum >= 7) items.push({ label: '学科必修已选', value: this.selectedAcademicCredits + ' 学分' })
      if (stepNum >= 8) items.push({ label: '专业必修已选', value: this.selectedMajorRequiredCredits + ' 学分' })
      if (stepNum >= 9) items.push({ label: '专业选修已选', value: this.selectedMajorElectiveCredits + ' 学分' })
      if (stepNum >= 9) items.push({ label: '选修要求', value: this.electiveCreditRequirement + ' 学分', isReq: true })
      if (stepNum >= 10) items.push({ label: '实践课已选', value: this.selectedPracticeCredits + ' 学分' })
      if (stepNum >= 11) items.push({ label: '通识选修已选', value: this.selectedGeneralElectiveCredits + ' 学分' })
      if (stepNum >= 11) items.push({ label: '通识选修要求', value: '至少 9 学分', isReq: true })
      if (stepNum >= 11) items.push({ label: '艺术审美要求', value: '至少 2 学分', isReq: true })
      if (stepNum >= 11) items.push({ label: '四史课程', value: '至少 1 门', isReq: true })
      if (stepNum >= 11) items.push({ label: '创新创业', value: '至少 1 门', isReq: true })
      if (stepNum >= 12) items.push({ label: '个性课程已选', value: this.selectedIndividualCredits + ' 学分' })
      if (stepNum >= 12) items.push({ label: '个性课程要求', value: '至少 6 学分', isReq: true })
      items.push({ label: '已选总计', value: this.totalSelectedCreditsWithIndividual + ' 学分' })
      return items
    },
    creditMessage(stepNum) {
      if (stepNum === 5 && this.selectedEnglishCredits !== 8) return '英语必修需选择4门课，共8学分'
      if (stepNum === 5 && this.selectedEnglishCredits === 8) return '英语必修已满足8学分要求'
      if (stepNum === 6 && this.selectedPECredits !== 4) return '体育必修需选择4门课，共4学分'
      if (stepNum === 6 && this.selectedPECredits === 4) return '体育必修已满足4学分要求'
      if (stepNum === 9 && this.selectedMajorElectiveCredits < this.electiveCreditRequirement) return '专业选修学分未达到修读要求'
      if (stepNum === 9 && this.selectedMajorElectiveCredits >= this.electiveCreditRequirement) return '专业选修学分已达到修读要求'
      if (stepNum === 11 && !this.generalElectiveRequirementsMet) return '通识选修未满足要求'
      if (stepNum === 11 && this.generalElectiveRequirementsMet) return '通识选修已满足要求'
      if (stepNum === 12 && !this.individualRequirementsMet) return '个性课程未满足要求'
      if (stepNum === 12 && this.individualRequirementsMet) return '个性课程已满足要求'
      return ''
    },
    creditMessageType(stepNum) {
      const m = this.creditMessage(stepNum)
      if (m.includes('未') || m.includes('需')) return 'warning'
      if (m.includes('满足') || m.includes('已')) return 'success'
      return 'info'
    },
    initSelection(stepNum, course) {
      this.getSel(stepNum, course.id)
    },
    selectMajor(value) {
      this.selectedMajor = value
      this.selectedSubMajor = null
      this.selectedClassType = null
      if (value !== 'computer_category') {
        this.nextStep()
      }
    },
    selectSubMajor(value) {
      this.selectedSubMajor = value
      this.nextStep()
    },
    selectClassType(value) {
      this.selectedClassType = value
    },
    selectEnglishClass(value) {
      this.selectedEnglishClass = value
    },
    isFixedCourse(stepNum, name) {
      if (stepNum === 3) return name === '形势与政策' || name === '大学生心理健康教育' || name.includes('思政') || name.includes('习概')
      if (stepNum === 5) return !name.includes('(初)') && !name.includes('(中)') && name.includes('英语')
      if (stepNum === 6) return name.includes('体育') && !name.includes('(初)') && !name.includes('(中)')
      if (stepNum === 11) return name.includes('国家安全')
      return false
    },
    isFixedPECourse(name) { return name.includes('体育') && !name.includes('(初)') && !name.includes('(中)') },
    isIntermediatePECourse(name) { return name.includes('(中)') },
    isPlaceholderCourse(name) { return name.includes('学分通识选修课') },
    isPlaceholderIndividualCourse(name) { return name.includes('学分个性课') },
    isArtCourse(course) { return course.topic_category === '艺术审美类' || (course.name && course.name.includes('艺术')) },
    isHistoryCourse(course) { return course.topic_category === '四史类' || (course.name && (course.name.includes('党史') || course.name.includes('四史') || course.name.includes('新中国史') || course.name.includes('改革开放史') || course.name.includes('社会主义发展史'))) },
    isInnovationCourse(course) { return course.topic_category === '创新创业类' || (course.name && (course.name.includes('创业') || course.name.includes('创新'))) },
    onCourseChange(stepNum, course, val) {
      if (stepNum === 11 && !val) {
        if (this.isFixedGeneralElective(course.name)) {
          this.getSel(11, course.id).selected = true
        }
      }
      if (stepNum === 12) {
        this.onIndividualCourseChange(course, val)
      }
    },
    isFixedGeneralElective(name) { return name.includes('国家安全') },
    onIndividualCourseChange(course, val) {},
    generalElectiveRequirementsMet() {
      const hasHistory = this.generalElectiveCourses.some(c => this.getSel(11, c.id).selected && this.isHistoryCourse(c))
      const hasArt = this.generalElectiveCourses.some(c => this.getSel(11, c.id).selected && this.isArtCourse(c))
      const hasInnovation = this.generalElectiveCourses.some(c => this.getSel(11, c.id).selected && this.isInnovationCourse(c))
      return this.selectedGeneralElectiveCredits >= 9 && hasArt && hasHistory && hasInnovation
    },
    individualRequirementsMet() {
      return this.selectedIndividualCredits >= 6
    },
    async loadGeneralCourses() {
      this.currentStep = 3
      this.loading = true
      try {
        this.generalCourses = await request.get('/courses', { params: { course_type: '通识必修' } })
        this.generalCourses.forEach(c => this.initSelection(3, c))
      } catch { this.message.error('加载课程失败') } finally { this.loading = false }
    },
    async loadEnglishCourses() {
      this.currentStep = 5
      this.loading = true
      try {
        this.englishCourses = await request.get('/courses', { params: { course_type: '英语必修' } })
        this.englishCourses.forEach(c => this.initSelection(5, c))
      } catch { this.message.error('加载课程失败') } finally { this.loading = false }
    },
    async loadPECourses() {
      this.currentStep = 6
      this.loading = true
      try {
        this.peCourses = await request.get('/courses', { params: { course_type: '体育必修' } })
        this.peCourses.forEach(c => this.initSelection(6, c))
        this.peCourses.forEach(c => { if (this.isFixedPECourse(c.name)) this.getSel(6, c.id).selected = true })
      } catch { this.message.error('加载课程失败') } finally { this.loading = false }
    },
    async loadAcademicCourses() {
      this.currentStep = 7
      this.loading = true
      try {
        this.academicCourses = await request.get('/courses', { params: { course_type: '学科必修', major_id: this.selectedMajor } })
        this.academicCourses.forEach(c => this.initSelection(7, c))
      } catch { this.message.error('加载课程失败') } finally { this.loading = false }
    },
    handleAfterAcademic() {
      if (this.selectedMajor === 'ai_exp') {
        this.currentStep = 10
      } else {
        this.loadMajorRequiredCourses()
      }
    },
    async loadMajorRequiredCourses() {
      this.currentStep = 8
      this.loading = true
      try {
        this.majorRequiredCourses = await request.get('/courses', { params: { course_type: '专业必修', major_id: this.selectedMajor } })
        this.majorRequiredCourses.forEach(c => this.initSelection(8, c))
      } catch { this.message.error('加载课程失败') } finally { this.loading = false }
    },
    async loadMajorElectiveCourses() {
      this.currentStep = 9
      this.loading = true
      try {
        this.majorElectiveCourses = await request.get('/courses', { params: { course_type: '专业选修', major_id: this.selectedMajor } })
        this.majorElectiveCourses.forEach(c => this.initSelection(9, c))
      } catch { this.message.error('加载课程失败') } finally { this.loading = false }
    },
    async loadPracticeCourses() {
      this.currentStep = 10
      this.loading = true
      try {
        this.practiceCourses = await request.get('/courses', { params: { course_type: '实践课', major_id: this.selectedMajor } })
        this.practiceCourses.forEach(c => this.initSelection(10, c))
      } catch { this.message.error('加载课程失败') } finally { this.loading = false }
    },
    async loadGeneralElectiveCourses() {
      this.currentStep = 11
      this.loading = true
      try {
        this.generalElectiveCourses = await request.get('/courses', { params: { course_type: '通识选修' } })
        this.generalElectiveCourses.forEach(c => this.initSelection(11, c))
        this.generalElectiveCourses.forEach(c => { if (this.isFixedGeneralElective(c.name)) this.getSel(11, c.id).selected = true })
      } catch { this.message.error('加载课程失败') } finally { this.loading = false }
    },
    async loadIndividualCourses() {
      this.currentStep = 12
      this.loading = true
      try {
        this.individualCourses = await request.get('/courses', { params: { course_type: '个性课程' } })
        this.individualCourses.forEach(c => this.initSelection(12, c))
      } catch { this.message.error('加载课程失败') } finally { this.loading = false }
    },
    goToEnglishClassSelection() { this.currentStep = 4 },
    goToSummary() { this.currentStep = 13 },
    nextStep() { this.currentStep++ },
    prevStep() { this.currentStep-- },
    goHome() {
      const role = localStorage.getItem('role')
      this.$router.push(role === 'admin' || role === 'superadmin' ? '/admin' : '/student')
    },
    resetSelection() {
      this.currentStep = 0
      this.selectedMajor = null
      this.selectedSubMajor = null
      this.selectedClassType = null
      this.selectedEnglishClass = null
      this.generalCourses = []
      this.englishCourses = []
      this.peCourses = []
      this.academicCourses = []
      this.majorRequiredCourses = []
      this.majorElectiveCourses = []
      this.practiceCourses = []
      this.generalElectiveCourses = []
      this.individualCourses = []
      this.generalCourseSelections = {}
      this.englishCourseSelections = {}
      this.peCourseSelections = {}
      this.academicCourseSelections = {}
      this.majorRequiredCourseSelections = {}
      this.majorElectiveCourseSelections = {}
      this.practiceCourseSelections = {}
      this.generalElectiveCourseSelections = {}
      this.individualCourseSelections = {}
      this.generalElectiveCategoryFilter = ''
    },
    exportSummary() {
      const semesterMap = {
        '大一上': '大一上学期', '大一下': '大一下学期',
        '大二上': '大二上学期', '大二下': '大二下学期',
        '大三上': '大三上学期', '大三下': '大三下学期',
        '大四上': '大四上学期', '大四下': '大四下学期'
      }
      let text = '===== 选课清单 =====\n\n'
      text += `专业: ${this.getMajorLabel}\n`
      if (this.selectedSubMajor) text += `方向: ${this.getSubMajorLabel}\n`
      if (this.selectedClassType) text += `班级: ${this.getClassTypeLabel}\n`
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
    },
    exportSummaryCSV() {
      const semesterMap = {
        '大一上': '大一上学期', '大一下': '大一下学期',
        '大二上': '大二上学期', '大二下': '大二下学期',
        '大三上': '大三上学期', '大三下': '大三下学期',
        '大四上': '大四上学期', '大四下': '大四下学期'
      }
      const BOM = '\uFEFF'
      let csv = BOM + '序号,课程类别,课程名称,授课教师,修读学期,学分\n'
      this.summaryCourses.forEach((c, i) => {
        const sem = semesterMap[c.semester] || c.semester
        csv += `${i+1},${c.category},${c.name},${c.teacher},${sem},${c.credit}\n`
      })
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' })
      const a = document.createElement('a')
      a.href = URL.createObjectURL(blob)
      a.download = '选课清单.csv'
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
.header-right { display: flex; align-items: center; gap: 8px; }
.main { padding: 20px 24px; max-width: 1100px; margin: 0 auto; }
.card-header { display: flex; justify-content: center; }
.step-content { padding: 8px 0; }
.step-title { text-align: center; font-size: 18px; font-weight: 600; margin-bottom: 24px; color: #333; }
.selection-summary { display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }
.option-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; max-width: 600px; margin: 0 auto; }
.option-grid.two-col { grid-template-columns: 1fr 1fr; max-width: 500px; }
.option-card {
  padding: 24px 16px; border-radius: 12px; border: 2px solid #eee;
  text-align: center; cursor: pointer; transition: all 0.2s; background: #fff;
}
.option-card:hover { border-color: #2080F0; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(32,128,240,0.1); }
.option-card.selected { border-color: #2080F0; background: #f0f7ff; }
.option-icon { font-size: 36px; margin-bottom: 8px; }
.option-name { font-weight: 600; font-size: 15px; margin-bottom: 4px; }
.option-desc { font-size: 12px; color: #999; }
.credit-scoreboard { margin-bottom: 20px; }
.scoreboard-content { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; padding: 8px 0; }
.score-item { display: flex; align-items: center; gap: 4px; }
.score-label { font-size: 12px; color: #666; white-space: nowrap; }
.score-value { font-size: 14px; font-weight: 600; color: #333; }
.score-value.requirement { color: #E6A23C; }
.score-item.total .score-value { color: #2080F0; font-size: 16px; }
.score-divider { width: 1px; height: 24px; background: #e8eaed; }
.credit-alert { margin-top: 8px; }
.loading-state, .empty-state { text-align: center; padding: 40px 0; }
.course-list { display: flex; flex-direction: column; gap: 12px; }
.course-card { transition: all 0.2s; }
.course-card.course-selected { border: 1px solid #2080F0; }
.course-header { display: flex; align-items: flex-start; gap: 12px; flex-wrap: wrap; }
.course-checkbox { flex: 1; }
.course-name { font-weight: 600; font-size: 14px; }
.course-info-tags { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.credit-tag { font-size: 13px; color: #E6A23C; font-weight: 500; }
.course-content { padding: 4px 0; }
.course-desc { font-size: 13px; color: #999; margin-bottom: 12px; }
.teacher-selection { margin-bottom: 10px; }
.teacher-name { font-size: 13px; }
.semester-selection, .quantity-selection { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.field-label { font-size: 13px; color: #666; white-space: nowrap; }
.quantity-hint { font-size: 12px; color: #999; }
.category-filter { margin: 16px 0; display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.filter-label { font-size: 13px; color: #666; white-space: nowrap; }
.summary-credit-total { margin-bottom: 20px; }
.summary-title { font-size: 16px; font-weight: 600; margin-bottom: 12px; }
.nav-buttons { margin-top: 24px; }
html.dark-mode .header { background: rgba(25,25,45,0.85); }
html.dark-mode .header h2 { color: #e8e8e8; }
html.dark-mode .step-title { color: #e8e8e8; }
html.dark-mode .option-card { background: #1e1e1e; border-color: #333; }
html.dark-mode .option-card:hover { border-color: #4098FC; }
html.dark-mode .option-card.selected { background: #1a2740; border-color: #4098FC; }
html.dark-mode .score-label { color: #aaa; }
html.dark-mode .score-value { color: #e8e8e8; }
html.dark-mode .score-divider { background: #333; }
.multi-row-steps {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px 4px;
  padding: 8px 0;
}
.multi-row-steps .n-steps-item {
  min-width: 120px;
  flex: 0 0 auto;
}
.multi-row-steps .n-steps-item-title {
  font-size: 13px;
}
@media (max-width: 768px) {
  .main { padding: 12px; }
  .option-grid { grid-template-columns: 1fr 1fr; }
  .option-grid.two-col { grid-template-columns: 1fr; }
  .scoreboard-content { gap: 4px; }
  .score-divider { display: none; }
  .multi-row-steps .n-steps-item {
    min-width: 100px;
  }
  .multi-row-steps .n-steps-item-title {
    font-size: 12px;
  }
}
</style>
