<template>
  <div class="simulated-selection">
    <el-header class="header">
      <h2>模拟选课</h2>
      <div class="user-info">
        <span>欢迎, {{ username }}</span>
        <el-button type="primary" size="small" @click="goHome">返回主页</el-button>
        <el-button type="danger" size="small" @click="handleLogout">退出</el-button>
      </div>
    </el-header>
    <el-main class="main" :style="mainBgStyle">
      <el-card>
        <template #header>
          <div class="card-header">
            <div style="width: 100%; display: flex; flex-direction: column; align-items: center;">
              <span style="margin-bottom: 10px;">模拟选课系统</span>
              <el-steps :active="currentStep" finish-status="success" class="multi-row-steps">
                <el-step title="选择专业" />
                <el-step title="选择方向" />
                <el-step title="选择班级" />
                <el-step title="通识必修" />
                <el-step title="英语快/慢班" />
                <el-step title="英语必修" />
                <el-step title="体育必修" />
                <el-step title="学科必修" />
                <el-step title="专业必修" />
                <el-step title="专业选修" />
                <el-step title="实践课" />
                <el-step title="通识选修" />
                <el-step title="个性课程" />
                <el-step title="选课总结" />
              </el-steps>
            </div>
          </div>
        </template>

        <!-- Step 1: 专业选择 -->
        <div v-if="currentStep === 0" class="step-content">
          <h3 class="step-title">请选择你的专业</h3>
          <div class="option-grid">
            <div
              v-for="major in majors"
              :key="major.value"
              class="option-card"
              :class="{ selected: selectedMajor === major.value }"
              @click="selectMajor(major.value)"
            >
              <div class="option-icon">{{ major.icon }}</div>
              <div class="option-name">{{ major.label }}</div>
            </div>
          </div>
        </div>

        <!-- Step 2: 方向选择（仅计算机类） -->
        <div v-if="currentStep === 1" class="step-content">
          <h3 class="step-title">请选择具体方向</h3>
          <div class="option-grid">
            <div
              v-for="sub in subMajors"
              :key="sub.value"
              class="option-card"
              :class="{ selected: selectedSubMajor === sub.value }"
              @click="selectSubMajor(sub.value)"
            >
              <div class="option-icon">{{ sub.icon }}</div>
              <div class="option-name">{{ sub.label }}</div>
            </div>
          </div>
        </div>

        <!-- Step 3: 班级选择（仅计算机/软件） -->
        <div v-if="currentStep === 2" class="step-content">
          <h3 class="step-title">请选择班级类型</h3>
          <div class="option-grid two-col">
            <div
              v-for="cls in classTypes"
              :key="cls.value"
              class="option-card"
              :class="{ selected: selectedClassType === cls.value }"
              @click="selectClassType(cls.value)"
            >
              <div class="option-icon">{{ cls.icon }}</div>
              <div class="option-name">{{ cls.label }}</div>
              <div class="option-desc">{{ cls.desc }}</div>
            </div>
          </div>
        </div>

        <!-- Step 4: 通识必修课程选择 -->
        <div v-if="currentStep === 3" class="step-content">
          <div class="selection-summary">
            <el-tag type="primary" size="large">专业: {{ getMajorLabel(selectedMajor) }}</el-tag>
            <el-tag v-if="selectedSubMajor" type="success" size="large">方向: {{ getSubMajorLabel(selectedSubMajor) }}</el-tag>
            <el-tag v-if="selectedClassType" type="warning" size="large">班级: {{ getClassTypeLabel(selectedClassType) }}</el-tag>
          </div>
          
          <div class="credit-scoreboard">
            <el-card class="scoreboard-card">
              <div class="scoreboard-content">
                <div class="score-item">
                  <span class="score-label">通识必修已选</span>
                  <span class="score-value">{{ selectedGeneralCredits }} 学分</span>
                </div>
              </div>
            </el-card>
          </div>
          
          <div v-if="loading" class="loading-state">
            <el-icon class="is-loading"><Loading /></el-icon>
            <span>加载课程中...</span>
          </div>
          
          <div v-else-if="generalCourses.length === 0" class="empty-state">
            <el-empty description="暂无通识必修课程" />
          </div>
          
          <div v-else class="course-list">
            <el-card
              v-for="course in generalCourses"
              :key="course.id"
              class="course-card"
              :body-style="{ padding: '20px' }"
            >
              <template #header>
                <div class="course-header">
                  <h3 class="course-name">{{ course.name }}</h3>
                  <div class="course-info">
                    <span class="credit">{{ course.credit }} 学分</span>
                    <span v-if="course.college" class="college">{{ course.college }}</span>
                  </div>
                </div>
              </template>
              
              <div class="course-content">
                <div class="course-description">{{ course.description || '暂无课程描述' }}</div>
                
                <!-- 教师选择 -->
                <div class="teacher-selection">
                  <h4>选择教师</h4>
                  <el-radio-group v-model="generalCourseSelections[course.id].teacherId" size="small">
                    <el-radio-button
                      v-for="(teacherId, index) in course.teacher_ids"
                      :key="teacherId"
                      :label="teacherId"
                    >
                      <span class="teacher-name">{{ course.teacher_names.split(',')[index] }}</span>
                      <span v-if="course.teacher_ratings[teacherId]" class="teacher-rating">
                        <el-rate v-model="course.teacher_ratings[teacherId]" disabled show-score score-template="{{ value }}" />
                      </span>
                    </el-radio-button>
                  </el-radio-group>
                </div>
                
                <!-- 学期选择 -->
                <div class="semester-selection">
                  <h4>修读学期</h4>
                  <el-select
                    v-model="generalCourseSelections[course.id].semester"
                    placeholder="请选择学期"
                    size="small"
                    :disabled="isPolicyCourse(course.name)"
                  >
                    <el-option
                      v-for="sem in studySemesters"
                      :key="sem.value"
                      :label="sem.label"
                      :value="sem.value"
                    />
                  </el-select>
                  <el-alert
                    v-if="isPolicyCourse(course.name)"
                    title="《形势与政策》为全部八个学期必修，无法更换"
                    type="info"
                    :closable="false"
                    show-icon
                    size="small"
                  />
                </div>
              </div>
            </el-card>
          </div>
        </div>

        <!-- Step 5: 英语必修 - 快班/慢班选择 -->
        <div v-if="currentStep === 4" class="step-content">
          <div class="selection-summary">
            <el-tag type="primary" size="large">专业: {{ getMajorLabel(selectedMajor) }}</el-tag>
            <el-tag v-if="selectedSubMajor" type="success" size="large">方向: {{ getSubMajorLabel(selectedSubMajor) }}</el-tag>
            <el-tag v-if="selectedClassType" type="warning" size="large">班级: {{ getClassTypeLabel(selectedClassType) }}</el-tag>
          </div>
          <h3 class="step-title">请选择英语班级类型</h3>
          <div class="option-grid two-col">
            <div
              class="option-card"
              :class="{ selected: selectedEnglishClass === 'fast' }"
              @click="selectEnglishClass('fast')"
            >
              <div class="option-icon">🚀</div>
              <div class="option-name">快班</div>
              <div class="option-desc">选择大学英语2、大学英语3 + 两门其他英语课程</div>
            </div>
            <div
              class="option-card"
              :class="{ selected: selectedEnglishClass === 'slow' }"
              @click="selectEnglishClass('slow')"
            >
              <div class="option-icon">🐢</div>
              <div class="option-name">慢班</div>
              <div class="option-desc">选择大学英语1、大学英语2、大学英语3 + 一门其他英语课程</div>
            </div>
          </div>
        </div>

        <!-- Step 6: 英语必修课程选择 -->
        <div v-if="currentStep === 5" class="step-content">
          <div class="selection-summary">
            <el-tag type="primary" size="large">专业: {{ getMajorLabel(selectedMajor) }}</el-tag>
            <el-tag v-if="selectedSubMajor" type="success" size="large">方向: {{ getSubMajorLabel(selectedSubMajor) }}</el-tag>
            <el-tag v-if="selectedClassType" type="warning" size="large">班级: {{ getClassTypeLabel(selectedClassType) }}</el-tag>
            <el-tag type="info" size="large">英语: {{ selectedEnglishClass === 'fast' ? '快班' : '慢班' }}</el-tag>
          </div>
          
          <div class="credit-scoreboard">
            <el-card class="scoreboard-card">
              <div class="scoreboard-content">
                <div class="score-item">
                  <span class="score-label">通识必修已选</span>
                  <span class="score-value">{{ selectedGeneralCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">英语必修已选</span>
                  <span class="score-value">{{ selectedEnglishCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">英语要求</span>
                  <span class="score-value requirement">8 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item total">
                  <span class="score-label">已选总计</span>
                  <span class="score-value">{{ totalSelectedCreditsWithEnglish }} 学分</span>
                </div>
              </div>
            </el-card>
            <el-alert
              v-if="selectedEnglishCredits !== 8"
              title="英语必修需选择4门课，共8学分"
              type="warning"
              :closable="false"
              show-icon
              size="small"
              class="credit-warning"
            />
            <el-alert
              v-else
              title="英语必修已满足8学分要求"
              type="success"
              :closable="false"
              show-icon
              size="small"
              class="credit-success"
            />
          </div>
          
          <div v-if="loading" class="loading-state">
            <el-icon class="is-loading"><Loading /></el-icon>
            <span>加载课程中...</span>
          </div>
          
          <div v-else-if="englishCourses.length === 0" class="empty-state">
            <el-empty description="暂无英语课程" />
          </div>
          
          <div v-else class="course-list">
            <el-card
              v-for="course in englishCourses"
              :key="course.id"
              class="course-card"
              :body-style="{ padding: '20px' }"
              :class="{ 'course-selected': englishCourseSelections[course.id] && englishCourseSelections[course.id].selected }"
            >
              <template #header>
                <div class="course-header">
                  <el-checkbox
                    v-model="englishCourseSelections[course.id].selected"
                    size="large"
                    class="course-checkbox"
                    :disabled="isFixedEnglishCourse(course.name)"
                  >
                    <h3 class="course-name">{{ course.name }}</h3>
                  </el-checkbox>
                  <div class="course-info">
                    <span class="credit">{{ course.credit }} 学分</span>
                    <span v-if="course.college" class="college">{{ course.college }}</span>
                    <el-tag v-if="isFixedEnglishCourse(course.name)" size="small" type="warning">必修</el-tag>
                  </div>
                </div>
              </template>
              
              <div class="course-content">
                <div class="course-description">{{ course.description || '暂无课程描述' }}</div>
                
                <!-- 教师选择 -->
                <div class="teacher-selection">
                  <h4>选择教师</h4>
                  <el-radio-group v-model="englishCourseSelections[course.id].teacherId" size="small">
                    <el-radio-button
                      v-for="(teacherId, index) in course.teacher_ids"
                      :key="teacherId"
                      :label="teacherId"
                    >
                      <span class="teacher-name">{{ course.teacher_names.split(',')[index] }}</span>
                      <span v-if="course.teacher_ratings[teacherId]" class="teacher-rating">
                        <el-rate v-model="course.teacher_ratings[teacherId]" disabled show-score score-template="{{ value }}" />
                      </span>
                    </el-radio-button>
                  </el-radio-group>
                </div>
                
                <!-- 学期选择 -->
                <div class="semester-selection">
                  <h4>修读学期</h4>
                  <el-select
                    v-model="englishCourseSelections[course.id].semester"
                    placeholder="请选择学期"
                    size="small"
                  >
                    <el-option
                      v-for="sem in studySemesters"
                      :key="sem.value"
                      :label="sem.label"
                      :value="sem.value"
                    />
                  </el-select>
                </div>
              </div>
            </el-card>
          </div>
        </div>

        <!-- Step 7: 体育必修课程选择 -->
        <div v-if="currentStep === 6" class="step-content">
          <div class="selection-summary">
            <el-tag type="primary" size="large">专业: {{ getMajorLabel(selectedMajor) }}</el-tag>
            <el-tag v-if="selectedSubMajor" type="success" size="large">方向: {{ getSubMajorLabel(selectedSubMajor) }}</el-tag>
            <el-tag v-if="selectedClassType" type="warning" size="large">班级: {{ getClassTypeLabel(selectedClassType) }}</el-tag>
          </div>
          
          <div class="credit-scoreboard">
            <el-card class="scoreboard-card">
              <div class="scoreboard-content">
                <div class="score-item">
                  <span class="score-label">通识必修已选</span>
                  <span class="score-value">{{ selectedGeneralCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">英语必修已选</span>
                  <span class="score-value">{{ selectedEnglishCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">体育必修已选</span>
                  <span class="score-value">{{ selectedPECredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">体育要求</span>
                  <span class="score-value requirement">4 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item total">
                  <span class="score-label">已选总计</span>
                  <span class="score-value">{{ totalSelectedCreditsWithPE }} 学分</span>
                </div>
              </div>
            </el-card>
            <el-alert
              v-if="selectedPECredits !== 4"
              title="体育必修需选择4门课，共4学分"
              type="warning"
              :closable="false"
              show-icon
              size="small"
              class="credit-warning"
            />
            <el-alert
              v-else
              title="体育必修已满足4学分要求"
              type="success"
              :closable="false"
              show-icon
              size="small"
              class="credit-success"
            />
          </div>
          
          <div v-if="loading" class="loading-state">
            <el-icon class="is-loading"><Loading /></el-icon>
            <span>加载课程中...</span>
          </div>
          
          <div v-else-if="peCourses.length === 0" class="empty-state">
            <el-empty description="暂无体育课程" />
          </div>
          
          <div v-else class="course-list">
            <el-card
              v-for="course in peCourses"
              :key="course.id"
              class="course-card"
              :body-style="{ padding: '20px' }"
              :class="{ 'course-selected': peCourseSelections[course.id] && peCourseSelections[course.id].selected }"
            >
              <template #header>
                <div class="course-header">
                  <el-checkbox
                    v-model="peCourseSelections[course.id].selected"
                    size="large"
                    class="course-checkbox"
                    :disabled="isFixedPECourse(course.name)"
                    @change="(val) => onPECourseSelectChange(course, val)"
                  >
                    <h3 class="course-name">{{ course.name }}</h3>
                  </el-checkbox>
                  <div class="course-info">
                    <span class="credit">{{ course.credit }} 学分</span>
                    <span v-if="course.college" class="college">{{ course.college }}</span>
                    <el-tag v-if="isFixedPECourse(course.name)" size="small" type="warning">必修</el-tag>
                    <el-tag v-if="isIntermediatePECourse(course.name)" size="small" type="info">需先修对应初级</el-tag>
                  </div>
                </div>
              </template>
              
              <div class="course-content">
                <div class="course-description">{{ course.description || '暂无课程描述' }}</div>
                
                <!-- 教师选择 -->
                <div class="teacher-selection">
                  <h4>选择教师</h4>
                  <el-radio-group v-model="peCourseSelections[course.id].teacherId" size="small">
                    <el-radio-button
                      v-for="(teacherId, index) in course.teacher_ids"
                      :key="teacherId"
                      :label="teacherId"
                    >
                      <span class="teacher-name">{{ course.teacher_names.split(',')[index] }}</span>
                      <span v-if="course.teacher_ratings[teacherId]" class="teacher-rating">
                        <el-rate v-model="course.teacher_ratings[teacherId]" disabled show-score score-template="{{ value }}" />
                      </span>
                    </el-radio-button>
                  </el-radio-group>
                </div>
                
                <!-- 学期选择 -->
                <div class="semester-selection">
                  <h4>修读学期</h4>
                  <el-select
                    v-model="peCourseSelections[course.id].semester"
                    placeholder="请选择学期"
                    size="small"
                  >
                    <el-option
                      v-for="sem in studySemesters"
                      :key="sem.value"
                      :label="sem.label"
                      :value="sem.value"
                    />
                  </el-select>
                </div>
              </div>
            </el-card>
          </div>
        </div>

        <!-- Step 8: 学科必修课程选择 -->
        <div v-if="currentStep === 7" class="step-content">
          <div class="selection-summary">
            <el-tag type="primary" size="large">专业: {{ getMajorLabel(selectedMajor) }}</el-tag>
            <el-tag v-if="selectedSubMajor" type="success" size="large">方向: {{ getSubMajorLabel(selectedSubMajor) }}</el-tag>
            <el-tag v-if="selectedClassType" type="warning" size="large">班级: {{ getClassTypeLabel(selectedClassType) }}</el-tag>
          </div>
          
          <div class="credit-scoreboard">
            <el-card class="scoreboard-card">
              <div class="scoreboard-content">
                <div class="score-item">
                  <span class="score-label">通识必修已选</span>
                  <span class="score-value">{{ selectedGeneralCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">英语必修已选</span>
                  <span class="score-value">{{ selectedEnglishCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">体育必修已选</span>
                  <span class="score-value">{{ selectedPECredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">学科必修已选</span>
                  <span class="score-value">{{ selectedAcademicCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item total">
                  <span class="score-label">已选总计</span>
                  <span class="score-value">{{ totalSelectedCredits }} 学分</span>
                </div>
              </div>
            </el-card>
          </div>
          
          <div v-if="loading" class="loading-state">
            <el-icon class="is-loading"><Loading /></el-icon>
            <span>加载课程中...</span>
          </div>
          
          <div v-else-if="academicCourses.length === 0" class="empty-state">
            <el-empty description="暂无学科必修课程" />
          </div>
          
          <div v-else class="course-list">
            <el-card
              v-for="course in academicCourses"
              :key="course.id"
              class="course-card"
              :body-style="{ padding: '20px' }"
            >
              <template #header>
                <div class="course-header">
                  <h3 class="course-name">{{ course.name }}</h3>
                  <div class="course-info">
                    <span class="credit">{{ course.credit }} 学分</span>
                    <span v-if="course.college" class="college">{{ course.college }}</span>
                  </div>
                </div>
              </template>
              
              <div class="course-content">
                <div class="course-description">{{ course.description || '暂无课程描述' }}</div>
                
                <!-- 教师选择 -->
                <div class="teacher-selection">
                  <h4>选择教师</h4>
                  <el-radio-group v-model="academicCourseSelections[course.id].teacherId" size="small">
                    <el-radio-button
                      v-for="(teacherId, index) in course.teacher_ids"
                      :key="teacherId"
                      :label="teacherId"
                    >
                      <span class="teacher-name">{{ course.teacher_names.split(',')[index] }}</span>
                      <span v-if="course.teacher_ratings[teacherId]" class="teacher-rating">
                        <el-rate v-model="course.teacher_ratings[teacherId]" disabled show-score score-template="{{ value }}" />
                      </span>
                    </el-radio-button>
                  </el-radio-group>
                </div>
                
                <!-- 学期选择 -->
                <div class="semester-selection">
                  <h4>修读学期</h4>
                  <el-select
                    v-model="academicCourseSelections[course.id].semester"
                    placeholder="请选择学期"
                    size="small"
                  >
                    <el-option
                      v-for="sem in studySemesters"
                      :key="sem.value"
                      :label="sem.label"
                      :value="sem.value"
                    />
                  </el-select>
                </div>
              </div>
            </el-card>
          </div>
        </div>

        <!-- Step 9: 专业必修课程选择 -->
        <div v-if="currentStep === 8" class="step-content">
          <div class="selection-summary">
            <el-tag type="primary" size="large">专业: {{ getMajorLabel(selectedMajor) }}</el-tag>
            <el-tag v-if="selectedSubMajor" type="success" size="large">方向: {{ getSubMajorLabel(selectedSubMajor) }}</el-tag>
            <el-tag v-if="selectedClassType" type="warning" size="large">班级: {{ getClassTypeLabel(selectedClassType) }}</el-tag>
          </div>
          
          <div class="credit-scoreboard">
            <el-card class="scoreboard-card">
              <div class="scoreboard-content">
                <div class="score-item">
                  <span class="score-label">通识必修已选</span>
                  <span class="score-value">{{ selectedGeneralCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">英语必修已选</span>
                  <span class="score-value">{{ selectedEnglishCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">体育必修已选</span>
                  <span class="score-value">{{ selectedPECredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">学科必修已选</span>
                  <span class="score-value">{{ selectedAcademicCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">专业必修已选</span>
                  <span class="score-value">{{ selectedMajorRequiredCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item total">
                  <span class="score-label">已选总计</span>
                  <span class="score-value">{{ totalSelectedCreditsWithMajor }} 学分</span>
                </div>
              </div>
            </el-card>
          </div>
          
          <div v-if="loading" class="loading-state">
            <el-icon class="is-loading"><Loading /></el-icon>
            <span>加载课程中...</span>
          </div>
          
          <div v-else-if="majorRequiredCourses.length === 0" class="empty-state">
            <el-empty description="暂无专业必修课程" />
          </div>
          
          <div v-else class="course-list">
            <el-card
              v-for="course in majorRequiredCourses"
              :key="course.id"
              class="course-card"
              :body-style="{ padding: '20px' }"
            >
              <template #header>
                <div class="course-header">
                  <h3 class="course-name">{{ course.name }}</h3>
                  <div class="course-info">
                    <span class="credit">{{ course.credit }} 学分</span>
                    <span v-if="course.college" class="college">{{ course.college }}</span>
                  </div>
                </div>
              </template>
              
              <div class="course-content">
                <div class="course-description">{{ course.description || '暂无课程描述' }}</div>
                
                <!-- 教师选择 -->
                <div class="teacher-selection">
                  <h4>选择教师</h4>
                  <el-radio-group v-model="majorRequiredCourseSelections[course.id].teacherId" size="small">
                    <el-radio-button
                      v-for="(teacherId, index) in course.teacher_ids"
                      :key="teacherId"
                      :label="teacherId"
                    >
                      <span class="teacher-name">{{ course.teacher_names.split(',')[index] }}</span>
                      <span v-if="course.teacher_ratings[teacherId]" class="teacher-rating">
                        <el-rate v-model="course.teacher_ratings[teacherId]" disabled show-score score-template="{{ value }}" />
                      </span>
                    </el-radio-button>
                  </el-radio-group>
                </div>
                
                <!-- 学期选择 -->
                <div class="semester-selection">
                  <h4>修读学期</h4>
                  <el-select
                    v-model="majorRequiredCourseSelections[course.id].semester"
                    placeholder="请选择学期"
                    size="small"
                  >
                    <el-option
                      v-for="sem in studySemesters"
                      :key="sem.value"
                      :label="sem.label"
                      :value="sem.value"
                    />
                  </el-select>
                </div>
              </div>
            </el-card>
          </div>
        </div>

        <!-- Step 10: 专业选修课程选择 -->
        <div v-if="currentStep === 9" class="step-content">
          <div class="selection-summary">
            <el-tag type="primary" size="large">专业: {{ getMajorLabel(selectedMajor) }}</el-tag>
            <el-tag v-if="selectedSubMajor" type="success" size="large">方向: {{ getSubMajorLabel(selectedSubMajor) }}</el-tag>
            <el-tag v-if="selectedClassType" type="warning" size="large">班级: {{ getClassTypeLabel(selectedClassType) }}</el-tag>
          </div>
          
          <div class="credit-scoreboard">
            <el-card class="scoreboard-card">
              <div class="scoreboard-content">
                <div class="score-item">
                  <span class="score-label">通识必修已选</span>
                  <span class="score-value">{{ selectedGeneralCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">英语必修已选</span>
                  <span class="score-value">{{ selectedEnglishCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">体育必修已选</span>
                  <span class="score-value">{{ selectedPECredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">学科必修已选</span>
                  <span class="score-value">{{ selectedAcademicCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">专业必修已选</span>
                  <span class="score-value">{{ selectedMajorRequiredCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">专业选修已选</span>
                  <span class="score-value">{{ selectedMajorElectiveCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">选修要求</span>
                  <span class="score-value requirement">{{ electiveCreditRequirement }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item total">
                  <span class="score-label">已选总计</span>
                  <span class="score-value">{{ totalSelectedCreditsWithElective }} 学分</span>
                </div>
              </div>
            </el-card>
            <el-alert
              v-if="selectedMajorElectiveCredits < electiveCreditRequirement"
              title="专业选修学分未达到修读要求"
              type="warning"
              :closable="false"
              show-icon
              size="small"
              class="credit-warning"
            />
            <el-alert
              v-else
              title="专业选修学分已达到修读要求"
              type="success"
              :closable="false"
              show-icon
              size="small"
              class="credit-success"
            />
          </div>
          
          <div v-if="loading" class="loading-state">
            <el-icon class="is-loading"><Loading /></el-icon>
            <span>加载课程中...</span>
          </div>
          
          <div v-else-if="majorElectiveCourses.length === 0" class="empty-state">
            <el-empty description="暂无专业选修课程" />
          </div>
          
          <div v-else class="course-list">
            <el-card
              v-for="course in majorElectiveCourses"
              :key="course.id"
              class="course-card"
              :body-style="{ padding: '20px' }"
              :class="{ 'course-selected': majorElectiveCourseSelections[course.id] && majorElectiveCourseSelections[course.id].selected }"
            >
              <template #header>
                <div class="course-header">
                  <el-checkbox
                    v-model="majorElectiveCourseSelections[course.id].selected"
                    size="large"
                    class="course-checkbox"
                  >
                    <h3 class="course-name">{{ course.name }}</h3>
                  </el-checkbox>
                  <div class="course-info">
                    <span class="credit">{{ course.credit }} 学分</span>
                    <span v-if="course.college" class="college">{{ course.college }}</span>
                  </div>
                </div>
              </template>
              
              <div class="course-content">
                <div class="course-description">{{ course.description || '暂无课程描述' }}</div>
                
                <!-- 教师选择 -->
                <div class="teacher-selection">
                  <h4>选择教师</h4>
                  <el-radio-group v-model="majorElectiveCourseSelections[course.id].teacherId" size="small">
                    <el-radio-button
                      v-for="(teacherId, index) in course.teacher_ids"
                      :key="teacherId"
                      :label="teacherId"
                    >
                      <span class="teacher-name">{{ course.teacher_names.split(',')[index] }}</span>
                      <span v-if="course.teacher_ratings[teacherId]" class="teacher-rating">
                        <el-rate v-model="course.teacher_ratings[teacherId]" disabled show-score score-template="{{ value }}" />
                      </span>
                    </el-radio-button>
                  </el-radio-group>
                </div>
                
                <!-- 学期选择 -->
                <div class="semester-selection">
                  <h4>修读学期</h4>
                  <el-select
                    v-model="majorElectiveCourseSelections[course.id].semester"
                    placeholder="请选择学期"
                    size="small"
                  >
                    <el-option
                      v-for="sem in studySemesters"
                      :key="sem.value"
                      :label="sem.label"
                      :value="sem.value"
                    />
                  </el-select>
                </div>
              </div>
            </el-card>
          </div>
        </div>

        <!-- Step 11 (ai_exp): 人工智能（实验）提示页面 -->
        <div v-if="currentStep === 10 && selectedMajor === 'ai_exp'" class="step-content">
          <div class="selection-summary">
            <el-tag type="primary" size="large">专业: {{ getMajorLabel(selectedMajor) }}</el-tag>
            <el-tag v-if="selectedSubMajor" type="success" size="large">方向: {{ getSubMajorLabel(selectedSubMajor) }}</el-tag>
            <el-tag v-if="selectedClassType" type="warning" size="large">班级: {{ getClassTypeLabel(selectedClassType) }}</el-tag>
          </div>
          
          <div class="credit-scoreboard">
            <el-card class="scoreboard-card">
              <div class="scoreboard-content">
                <div class="score-item">
                  <span class="score-label">通识必修已选</span>
                  <span class="score-value">{{ selectedGeneralCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">英语必修已选</span>
                  <span class="score-value">{{ selectedEnglishCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">体育必修已选</span>
                  <span class="score-value">{{ selectedPECredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">学科必修已选</span>
                  <span class="score-value">{{ selectedAcademicCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item total">
                  <span class="score-label">已选总计</span>
                  <span class="score-value">{{ totalSelectedCredits }} 学分</span>
                </div>
              </div>
            </el-card>
          </div>
          
          <div class="coming-soon-container">
            <el-result icon="warning" title="培养方案未出完整版本" sub-title="人工智能（实验）培养方案未出完整版本，敬请期待">
              <template #extra>
                <el-button type="primary" @click="resetSelection">重新选择</el-button>
              </template>
            </el-result>
          </div>
        </div>

        <!-- Step 11: 实践课选择 -->
        <div v-if="currentStep === 10 && selectedMajor !== 'ai_exp'" class="step-content">
          <div class="selection-summary">
            <el-tag type="primary" size="large">专业: {{ getMajorLabel(selectedMajor) }}</el-tag>
            <el-tag v-if="selectedSubMajor" type="success" size="large">方向: {{ getSubMajorLabel(selectedSubMajor) }}</el-tag>
            <el-tag v-if="selectedClassType" type="warning" size="large">班级: {{ getClassTypeLabel(selectedClassType) }}</el-tag>
          </div>
          
          <div class="credit-scoreboard">
            <el-card class="scoreboard-card">
              <div class="scoreboard-content">
                <div class="score-item">
                  <span class="score-label">通识必修已选</span>
                  <span class="score-value">{{ selectedGeneralCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">英语必修已选</span>
                  <span class="score-value">{{ selectedEnglishCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">体育必修已选</span>
                  <span class="score-value">{{ selectedPECredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">学科必修已选</span>
                  <span class="score-value">{{ selectedAcademicCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">专业必修已选</span>
                  <span class="score-value">{{ selectedMajorRequiredCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">专业选修已选</span>
                  <span class="score-value">{{ selectedMajorElectiveCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">实践课已选</span>
                  <span class="score-value">{{ selectedPracticeCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item total">
                  <span class="score-label">已选总计</span>
                  <span class="score-value">{{ totalSelectedCreditsWithPractice }} 学分</span>
                </div>
              </div>
            </el-card>
          </div>
          
          <div v-if="loading" class="loading-state">
            <el-icon class="is-loading"><Loading /></el-icon>
            <span>加载课程中...</span>
          </div>
          
          <div v-else-if="practiceCourses.length === 0" class="empty-state">
            <el-empty description="暂无实践课程" />
          </div>
          
          <div v-else class="course-list">
            <el-card
              v-for="course in practiceCourses"
              :key="course.id"
              class="course-card"
              :body-style="{ padding: '20px' }"
              :class="{ 'course-selected': practiceCourseSelections[course.id] && practiceCourseSelections[course.id].selected }"
            >
              <template #header>
                <div class="course-header">
                  <el-checkbox
                    v-model="practiceCourseSelections[course.id].selected"
                    size="large"
                    class="course-checkbox"
                  >
                    <h3 class="course-name">{{ course.name }}</h3>
                  </el-checkbox>
                  <div class="course-info">
                    <span class="credit">{{ course.credit }} 学分</span>
                    <span v-if="course.college" class="college">{{ course.college }}</span>
                  </div>
                </div>
              </template>
              
              <div class="course-content">
                <div class="course-description">{{ course.description || '暂无课程描述' }}</div>
                
                <!-- 教师选择 -->
                <div class="teacher-selection">
                  <h4>选择教师</h4>
                  <el-radio-group v-model="practiceCourseSelections[course.id].teacherId" size="small">
                    <el-radio-button
                      v-for="(teacherId, index) in course.teacher_ids"
                      :key="teacherId"
                      :label="teacherId"
                    >
                      <span class="teacher-name">{{ course.teacher_names.split(',')[index] }}</span>
                      <span v-if="course.teacher_ratings[teacherId]" class="teacher-rating">
                        <el-rate v-model="course.teacher_ratings[teacherId]" disabled show-score score-template="{{ value }}" />
                      </span>
                    </el-radio-button>
                  </el-radio-group>
                </div>
                
                <!-- 学期选择 -->
                <div class="semester-selection">
                  <h4>修读学期</h4>
                  <el-select
                    v-model="practiceCourseSelections[course.id].semester"
                    placeholder="请选择学期"
                    size="small"
                  >
                    <el-option
                      v-for="sem in studySemesters"
                      :key="sem.value"
                      :label="sem.label"
                      :value="sem.value"
                    />
                  </el-select>
                </div>
              </div>
            </el-card>
          </div>
        </div>

        <!-- Step 12: 通识选修课程选择 -->
        <div v-if="currentStep === 11" class="step-content">
          <div class="selection-summary">
            <el-tag type="primary" size="large">专业: {{ getMajorLabel(selectedMajor) }}</el-tag>
            <el-tag v-if="selectedSubMajor" type="success" size="large">方向: {{ getSubMajorLabel(selectedSubMajor) }}</el-tag>
            <el-tag v-if="selectedClassType" type="warning" size="large">班级: {{ getClassTypeLabel(selectedClassType) }}</el-tag>
          </div>
          
          <div class="credit-scoreboard">
            <el-card class="scoreboard-card">
              <div class="scoreboard-content">
                <div class="score-item">
                  <span class="score-label">通识必修已选</span>
                  <span class="score-value">{{ selectedGeneralCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">英语必修已选</span>
                  <span class="score-value">{{ selectedEnglishCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">体育必修已选</span>
                  <span class="score-value">{{ selectedPECredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">学科必修已选</span>
                  <span class="score-value">{{ selectedAcademicCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">专业必修已选</span>
                  <span class="score-value">{{ selectedMajorRequiredCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">专业选修已选</span>
                  <span class="score-value">{{ selectedMajorElectiveCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">实践课已选</span>
                  <span class="score-value">{{ selectedPracticeCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">通识选修已选</span>
                  <span class="score-value">{{ selectedGeneralElectiveCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">通识选修要求</span>
                  <span class="score-value requirement">至少 9 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">艺术审美要求</span>
                  <span class="score-value requirement">至少 2 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">四史课程</span>
                  <span class="score-value requirement">至少 1 门</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">创新创业</span>
                  <span class="score-value requirement">至少 1 门</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item total">
                  <span class="score-label">已选总计</span>
                  <span class="score-value">{{ totalSelectedCreditsWithGeneralElective }} 学分</span>
                </div>
              </div>
            </el-card>
            <el-alert
              v-if="!generalElectiveRequirementsMet"
              title="通识选修未满足要求"
              type="warning"
              :closable="false"
              show-icon
              size="small"
              class="credit-warning"
            />
            <el-alert
              v-else
              title="通识选修已满足要求"
              type="success"
              :closable="false"
              show-icon
              size="small"
              class="credit-success"
            />
          </div>
          
          <div v-if="loading" class="loading-state">
            <el-icon class="is-loading"><Loading /></el-icon>
            <span>加载课程中...</span>
          </div>
          
          <div v-else-if="generalElectiveCourses.length === 0" class="empty-state">
            <el-empty description="暂无通识选修课程" />
          </div>
          
          <!-- 分类筛选器 -->
          <div v-if="generalElectiveCourses.length > 0" class="category-filter">
            <span class="filter-label">分类筛选：</span>
            <el-radio-group v-model="generalElectiveCategoryFilter" size="small">
              <el-radio-button label="">全部 ({{ generalElectiveCourses.length }})</el-radio-button>
              <el-radio-button label="四史类">四史类 ({{ categoryCount('四史类') }})</el-radio-button>
              <el-radio-button label="艺术审美类">艺术审美类 ({{ categoryCount('艺术审美类') }})</el-radio-button>
              <el-radio-button label="创新创业类">创新创业类 ({{ categoryCount('创新创业类') }})</el-radio-button>
              <el-radio-button label="其他类">其他类 ({{ categoryCount('其他类') }})</el-radio-button>
            </el-radio-group>
          </div>
          
          <div v-if="generalElectiveCourses.length > 0" class="course-list">
            <el-card
              v-for="course in filteredGeneralElectiveCourses"
              :key="course.id"
              class="course-card"
              :body-style="{ padding: '20px' }"
              :class="{ 'course-selected': generalElectiveCourseSelections[course.id] && generalElectiveCourseSelections[course.id].selected }"
            >
              <template #header>
                <div class="course-header">
                  <el-checkbox
                    v-model="generalElectiveCourseSelections[course.id].selected"
                    size="large"
                    class="course-checkbox"
                    :disabled="isFixedGeneralElective(course.name)"
                    @change="(val) => onGeneralElectiveChange(course, val)"
                  >
                    <h3 class="course-name">{{ course.name }}</h3>
                  </el-checkbox>
                  <div class="course-info">
                    <span class="credit">{{ course.credit }} 学分</span>
                    <el-tag v-if="isFixedGeneralElective(course.name)" size="small" type="warning">必修</el-tag>
                    <el-tag v-if="isArtCourse(course)" size="small" type="success">艺术审美</el-tag>
                    <el-tag v-if="isHistoryCourse(course)" size="small" type="info">四史</el-tag>
                    <el-tag v-if="isInnovationCourse(course)" size="small" type="primary">创新创业</el-tag>
                    <el-tag v-if="isPlaceholderCourse(course.name)" size="small" type="warning">通识选修</el-tag>
                  </div>
                </div>
              </template>
              
              <div class="course-content">
                <div class="course-description">{{ course.description || '暂无课程描述' }}</div>
                
                <!-- 教师选择 -->
                <div class="teacher-selection">
                  <h4>选择教师</h4>
                  <el-radio-group v-model="generalElectiveCourseSelections[course.id].teacherId" size="small">
                    <el-radio-button
                      v-for="(teacherId, index) in course.teacher_ids"
                      :key="teacherId"
                      :label="teacherId"
                    >
                      <span class="teacher-name">{{ course.teacher_names.split(',')[index] }}</span>
                      <span v-if="course.teacher_ratings[teacherId]" class="teacher-rating">
                        <el-rate v-model="course.teacher_ratings[teacherId]" disabled show-score score-template="{{ value }}" />
                      </span>
                    </el-radio-button>
                  </el-radio-group>
                </div>
                
                <!-- 学期选择 -->
                <div class="semester-selection">
                  <h4>修读学期</h4>
                  <el-select
                    v-model="generalElectiveCourseSelections[course.id].semester"
                    placeholder="请选择学期"
                    size="small"
                  >
                    <el-option
                      v-for="sem in studySemesters"
                      :key="sem.value"
                      :label="sem.label"
                      :value="sem.value"
                    />
                  </el-select>
                </div>

                <!-- x学分通识选修课：选择修读数量 -->
                <div v-if="isPlaceholderCourse(course.name)" class="quantity-selection">
                  <h4>修读数量</h4>
                  <el-input-number
                    v-model="generalElectiveCourseSelections[course.id].quantity"
                    :min="0"
                    :max="9"
                    size="small"
                    @change="(val) => onPlaceholderQuantityChange(course, val)"
                  />
                  <span class="quantity-hint">选择修读门数（每门{{ course.credit }}学分）</span>
                </div>
              </div>
            </el-card>
          </div>
        </div>

        <!-- Step 13: 个性课程选择 -->
        <div v-if="currentStep === 12" class="step-content">
          <div class="selection-summary">
            <el-tag type="primary" size="large">专业: {{ getMajorLabel(selectedMajor) }}</el-tag>
            <el-tag v-if="selectedSubMajor" type="success" size="large">方向: {{ getSubMajorLabel(selectedSubMajor) }}</el-tag>
            <el-tag v-if="selectedClassType" type="warning" size="large">班级: {{ getClassTypeLabel(selectedClassType) }}</el-tag>
          </div>
          
          <div class="credit-scoreboard">
            <el-card class="scoreboard-card">
              <div class="scoreboard-content">
                <div class="score-item">
                  <span class="score-label">通识必修已选</span>
                  <span class="score-value">{{ selectedGeneralCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">英语必修已选</span>
                  <span class="score-value">{{ selectedEnglishCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">体育必修已选</span>
                  <span class="score-value">{{ selectedPECredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">学科必修已选</span>
                  <span class="score-value">{{ selectedAcademicCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">专业必修已选</span>
                  <span class="score-value">{{ selectedMajorRequiredCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">专业选修已选</span>
                  <span class="score-value">{{ selectedMajorElectiveCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">实践课已选</span>
                  <span class="score-value">{{ selectedPracticeCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">通识选修已选</span>
                  <span class="score-value">{{ selectedGeneralElectiveCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">个性课程已选</span>
                  <span class="score-value">{{ selectedIndividualCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">个性课程要求</span>
                  <span class="score-value requirement">至少 6 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item total">
                  <span class="score-label">已选总计</span>
                  <span class="score-value">{{ totalSelectedCreditsWithIndividual }} 学分</span>
                </div>
              </div>
            </el-card>
            <el-alert
              v-if="!individualRequirementsMet"
              title="个性课程未满足要求"
              type="warning"
              :closable="false"
              show-icon
              size="small"
              class="credit-warning"
            />
            <el-alert
              v-else
              title="个性课程已满足要求"
              type="success"
              :closable="false"
              show-icon
              size="small"
              class="credit-success"
            />
          </div>
          
          <div v-if="loading" class="loading-state">
            <el-icon class="is-loading"><Loading /></el-icon>
            <span>加载课程中...</span>
          </div>
          
          <div v-else-if="individualCourses.length === 0" class="empty-state">
            <el-empty description="暂无个性课程" />
          </div>
          
          <div v-if="individualCourses.length > 0" class="course-list">
            <el-card
              v-for="course in individualCourses"
              :key="course.id"
              class="course-card"
              :body-style="{ padding: '20px' }"
              :class="{ 'course-selected': individualCourseSelections[course.id] && individualCourseSelections[course.id].selected }"
            >
              <template #header>
                <div class="course-header">
                  <el-checkbox
                    v-model="individualCourseSelections[course.id].selected"
                    size="large"
                    class="course-checkbox"
                    @change="(val) => onIndividualCourseChange(course, val)"
                  >
                    <h3 class="course-name">{{ course.name }}</h3>
                  </el-checkbox>
                  <div class="course-info">
                    <span class="credit">{{ course.credit }} 学分</span>
                    <el-tag v-if="isPlaceholderIndividualCourse(course.name)" size="small" type="warning">个性课</el-tag>
                  </div>
                </div>
              </template>
              
              <div class="course-content">
                <div class="course-description">{{ course.description || '暂无课程描述' }}</div>
                
                <!-- 教师选择 -->
                <div class="teacher-selection">
                  <h4>选择教师</h4>
                  <el-radio-group v-model="individualCourseSelections[course.id].teacherId" size="small">
                    <el-radio-button
                      v-for="(teacherId, index) in course.teacher_ids"
                      :key="teacherId"
                      :label="teacherId"
                    >
                      <span class="teacher-name">{{ course.teacher_names.split(',')[index] }}</span>
                      <span v-if="course.teacher_ratings[teacherId]" class="teacher-rating">
                        <el-rate v-model="course.teacher_ratings[teacherId]" disabled show-score score-template="{{ value }}" />
                      </span>
                    </el-radio-button>
                  </el-radio-group>
                </div>
                
                <!-- 学期选择 -->
                <div class="semester-selection">
                  <h4>修读学期</h4>
                  <el-select
                    v-model="individualCourseSelections[course.id].semester"
                    placeholder="请选择学期"
                    size="small"
                  >
                    <el-option
                      v-for="sem in studySemesters"
                      :key="sem.value"
                      :label="sem.label"
                      :value="sem.value"
                    />
                  </el-select>
                </div>

                <!-- x学分个性课：选择修读数量 -->
                <div v-if="isPlaceholderIndividualCourse(course.name)" class="quantity-selection">
                  <h4>修读数量</h4>
                  <el-input-number
                    v-model="individualCourseSelections[course.id].quantity"
                    :min="0"
                    :max="9"
                    size="small"
                    @change="(val) => onIndividualPlaceholderQuantityChange(course, val)"
                  />
                  <span class="quantity-hint">选择修读门数（每门{{ course.credit }}学分）</span>
                </div>
              </div>
            </el-card>
          </div>
        </div>

        <!-- Step 14: 选课总结 -->
        <div v-if="currentStep === 13" class="step-content">
          <div class="selection-summary">
            <el-tag type="primary" size="large">专业: {{ getMajorLabel(selectedMajor) }}</el-tag>
            <el-tag v-if="selectedSubMajor" type="success" size="large">方向: {{ getSubMajorLabel(selectedSubMajor) }}</el-tag>
            <el-tag v-if="selectedClassType" type="warning" size="large">班级: {{ getClassTypeLabel(selectedClassType) }}</el-tag>
          </div>
          
          <div class="summary-credit-total">
            <el-card class="scoreboard-card">
              <div class="scoreboard-content">
                <div class="score-item total">
                  <span class="score-label">选课总计</span>
                  <span class="score-value">{{ totalSelectedCreditsWithIndividual }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">通识必修</span>
                  <span class="score-value">{{ selectedGeneralCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">英语必修</span>
                  <span class="score-value">{{ selectedEnglishCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">体育必修</span>
                  <span class="score-value">{{ selectedPECredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">学科必修</span>
                  <span class="score-value">{{ selectedAcademicCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">专业必修</span>
                  <span class="score-value">{{ selectedMajorRequiredCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">专业选修</span>
                  <span class="score-value">{{ selectedMajorElectiveCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">实践课</span>
                  <span class="score-value">{{ selectedPracticeCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">通识选修</span>
                  <span class="score-value">{{ selectedGeneralElectiveCredits }} 学分</span>
                </div>
                <div class="score-divider"></div>
                <div class="score-item">
                  <span class="score-label">个性课程</span>
                  <span class="score-value">{{ selectedIndividualCredits }} 学分</span>
                </div>
              </div>
            </el-card>
          </div>
          
          <div class="summary-table-wrapper">
            <h3 class="summary-title">选课清单</h3>
            <el-table :data="summaryCourses" border stripe style="width: 100%" max-height="500">
              <el-table-column type="index" label="序号" width="60" />
              <el-table-column prop="category" label="课程类别" width="100" />
              <el-table-column prop="name" label="课程名称" min-width="200" />
              <el-table-column prop="teacher" label="授课教师" width="120" />
              <el-table-column prop="semester" label="修读学期" width="120" />
              <el-table-column prop="credit" label="学分" width="80" />
            </el-table>
          </div>
        </div>

        <!-- 导航按钮 -->
        <div v-if="currentStep > 0 && currentStep < 3" class="nav-buttons">
          <el-button @click="goBack">上一步</el-button>
        </div>
        <div v-if="currentStep === 3" class="nav-buttons">
          <el-button @click="goBack">上一步</el-button>
          <el-button type="primary" @click="goToEnglishClassSelection">下一步</el-button>
        </div>
        <div v-if="currentStep === 4" class="nav-buttons">
          <el-button @click="goBack">上一步</el-button>
        </div>
        <div v-if="currentStep === 5" class="nav-buttons">
          <el-button @click="goBack">上一步</el-button>
          <el-button type="primary" @click="loadPECourses">下一步</el-button>
        </div>
        <div v-if="currentStep === 6" class="nav-buttons">
          <el-button @click="goBack">上一步</el-button>
          <el-button type="primary" @click="loadAcademicCourses">下一步</el-button>
        </div>
        <div v-if="currentStep === 7" class="nav-buttons">
          <el-button @click="goBack">上一步</el-button>
          <el-button type="primary" @click="handleAfterAcademic">下一步</el-button>
        </div>
        <div v-if="currentStep === 8" class="nav-buttons">
          <el-button @click="goBack">上一步</el-button>
          <el-button type="primary" @click="loadMajorElectiveCourses">下一步</el-button>
        </div>
        <div v-if="currentStep === 9" class="nav-buttons">
          <el-button @click="goBack">上一步</el-button>
          <el-button type="primary" @click="loadPracticeCourses">下一步</el-button>
        </div>
        <div v-if="currentStep === 10" class="nav-buttons">
          <el-button @click="goBack">上一步</el-button>
          <el-button type="primary" @click="loadGeneralElectiveCourses">下一步</el-button>
        </div>
        <div v-if="currentStep === 11" class="nav-buttons">
          <el-button @click="goBack">上一步</el-button>
          <el-button type="primary" @click="loadIndividualCourses">下一步</el-button>
        </div>
        <div v-if="currentStep === 12" class="nav-buttons">
          <el-button @click="goBack">上一步</el-button>
          <el-button type="primary" @click="goToSummary">下一步</el-button>
        </div>
        <div v-if="currentStep === 13" class="nav-buttons">
          <el-button @click="goBack">上一步</el-button>
          <el-button type="primary" @click="exportSummary">导出选课单</el-button>
          <el-button type="success" @click="resetSelection">重新选择</el-button>
        </div>
      </el-card>
    </el-main>
  </div>
</template>

<script>
import request from '@/api'
import { Loading } from '@element-plus/icons-vue'

export default {
  components: {
    Loading
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
      mainBgStyle: {
        background: 'rgba(255, 255, 255, 0.8)',
        backdropFilter: 'blur(20px) saturate(180%)',
        borderRadius: '16px',
        boxShadow: '0 8px 32px rgba(31, 38, 135, 0.1)',
        border: '1px solid rgba(255, 255, 255, 0.3)',
        minHeight: 'calc(100vh - 80px)',
        padding: '20px'
      },
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
      studySemesters: [
        { value: '大一上', label: '大一上' },
        { value: '大一下', label: '大一下' },
        { value: '大二上', label: '大二上' },
        { value: '大二下', label: '大二下' },
        { value: '大三上', label: '大三上' },
        { value: '大三下', label: '大三下' },
        { value: '大四上', label: '大四上' },
        { value: '大四下', label: '大四下' }
      ]
    }
  },
  mounted() {
    this.username = localStorage.getItem('username')
  },
  computed: {
    selectedGeneralCredits() {
      let total = 0
      this.generalCourses.forEach(course => {
        if (this.generalCourseSelections[course.id] && this.generalCourseSelections[course.id].selected) {
          total += parseFloat(course.credit) || 0
        }
      })
      return total
    },
    selectedAcademicCredits() {
      let total = 0
      this.academicCourses.forEach(course => {
        if (this.academicCourseSelections[course.id] && this.academicCourseSelections[course.id].selected) {
          total += parseFloat(course.credit) || 0
        }
      })
      return total
    },
    selectedMajorRequiredCredits() {
      let total = 0
      this.majorRequiredCourses.forEach(course => {
        if (this.majorRequiredCourseSelections[course.id] && this.majorRequiredCourseSelections[course.id].selected) {
          total += parseFloat(course.credit) || 0
        }
      })
      return total
    },
    selectedMajorElectiveCredits() {
      let total = 0
      this.majorElectiveCourses.forEach(course => {
        if (this.majorElectiveCourseSelections[course.id] && this.majorElectiveCourseSelections[course.id].selected) {
          total += parseFloat(course.credit) || 0
        }
      })
      return total
    },
    electiveCreditRequirement() {
      const requirementMap = {
        'computer': 23.5,
        'software': 20.5,
        'big_data': 22.5,
        'ai': 24.5,
        'software_exp': 21,
        'ai_exp': 21
      }
      if (this.selectedSubMajor) {
        return requirementMap[this.selectedSubMajor] || 0
      }
      return requirementMap[this.selectedMajor] || 0
    },
    selectedEnglishCredits() {
      let total = 0
      this.englishCourses.forEach(course => {
        if (this.englishCourseSelections[course.id] && this.englishCourseSelections[course.id].selected) {
          total += parseFloat(course.credit) || 0
        }
      })
      return total
    },
    selectedPECredits() {
      let total = 0
      this.peCourses.forEach(course => {
        if (this.peCourseSelections[course.id] && this.peCourseSelections[course.id].selected) {
          total += parseFloat(course.credit) || 0
        }
      })
      return total
    },
    totalSelectedCredits() {
      return this.selectedGeneralCredits + this.selectedEnglishCredits + this.selectedPECredits + this.selectedAcademicCredits
    },
    totalSelectedCreditsWithEnglish() {
      return this.selectedGeneralCredits + this.selectedEnglishCredits
    },
    totalSelectedCreditsWithPE() {
      return this.selectedGeneralCredits + this.selectedEnglishCredits + this.selectedPECredits
    },
    totalSelectedCreditsWithMajor() {
      return this.selectedGeneralCredits + this.selectedEnglishCredits + this.selectedPECredits + this.selectedAcademicCredits + this.selectedMajorRequiredCredits
    },
    selectedPracticeCredits() {
      let total = 0
      this.practiceCourses.forEach(course => {
        if (this.practiceCourseSelections[course.id] && this.practiceCourseSelections[course.id].selected) {
          total += parseFloat(course.credit) || 0
        }
      })
      return total
    },
    totalSelectedCreditsWithElective() {
      return this.selectedGeneralCredits + this.selectedEnglishCredits + this.selectedPECredits + this.selectedAcademicCredits + this.selectedMajorRequiredCredits + this.selectedMajorElectiveCredits
    },
    totalSelectedCreditsWithPractice() {
      return this.selectedGeneralCredits + this.selectedEnglishCredits + this.selectedPECredits + this.selectedAcademicCredits + this.selectedMajorRequiredCredits + this.selectedMajorElectiveCredits + this.selectedPracticeCredits
    },
    selectedGeneralElectiveCredits() {
      let total = 0
      this.generalElectiveCourses.forEach(course => {
        const sel = this.generalElectiveCourseSelections[course.id]
        if (sel) {
          if (this.isPlaceholderCourse(course.name)) {
            total += (parseFloat(course.credit) || 0) * (sel.quantity || 0)
          } else if (sel.selected) {
            total += parseFloat(course.credit) || 0
          }
        }
      })
      return total
    },
    selectedArtCredits() {
      let total = 0
      this.generalElectiveCourses.forEach(course => {
        const sel = this.generalElectiveCourseSelections[course.id]
        if (sel && sel.selected && this.isArtCourse(course)) {
          total += parseFloat(course.credit) || 0
        }
      })
      return total
    },
    selectedHistoryCount() {
      let count = 0
      this.generalElectiveCourses.forEach(course => {
        const sel = this.generalElectiveCourseSelections[course.id]
        if (sel && sel.selected && this.isHistoryCourse(course)) {
          count++
        }
      })
      return count
    },
    selectedInnovationCount() {
      let count = 0
      this.generalElectiveCourses.forEach(course => {
        const sel = this.generalElectiveCourseSelections[course.id]
        if (sel && sel.selected && this.isInnovationCourse(course)) {
          count++
        }
      })
      return count
    },
    generalElectiveRequirementsMet() {
      return this.selectedGeneralElectiveCredits >= 9 &&
        this.selectedArtCredits >= 2 &&
        this.selectedHistoryCount >= 1 &&
        this.selectedInnovationCount >= 1
    },
    totalSelectedCreditsWithGeneralElective() {
      return this.selectedGeneralCredits + this.selectedEnglishCredits + this.selectedPECredits + this.selectedAcademicCredits + this.selectedMajorRequiredCredits + this.selectedMajorElectiveCredits + this.selectedPracticeCredits + this.selectedGeneralElectiveCredits
    },
    selectedIndividualCredits() {
      let total = 0
      this.individualCourses.forEach(course => {
        const sel = this.individualCourseSelections[course.id]
        if (sel) {
          if (this.isPlaceholderIndividualCourse(course.name)) {
            total += (parseFloat(course.credit) || 0) * (sel.quantity || 0)
          } else if (sel.selected) {
            total += parseFloat(course.credit) || 0
          }
        }
      })
      return total
    },
    individualRequirementsMet() {
      return this.selectedIndividualCredits >= 6
    },
    totalSelectedCreditsWithIndividual() {
      return this.selectedGeneralCredits + this.selectedEnglishCredits + this.selectedPECredits + this.selectedAcademicCredits + this.selectedMajorRequiredCredits + this.selectedMajorElectiveCredits + this.selectedPracticeCredits + this.selectedGeneralElectiveCredits + this.selectedIndividualCredits
    },
    summaryCourses() {
      const courses = []
      const semesterMap = {
        1: '第1学期', 2: '第2学期', 3: '第3学期', 4: '第4学期',
        5: '第5学期', 6: '第6学期', 7: '第7学期', 8: '第8学期'
      }
      const addCourse = (course, sel, category) => {
        if (!sel || !sel.selected) return
        const teacherNames = course.teacher_names ? course.teacher_names.split(',') : []
        const teacherIds = course.teacher_ids || []
        let teacherName = ''
        if (sel.teacherId && teacherIds.length > 0) {
          const idx = teacherIds.indexOf(sel.teacherId)
          teacherName = idx >= 0 && teacherNames[idx] ? teacherNames[idx] : ''
        }
        if (this.isPlaceholderCourse(course.name) || this.isPlaceholderIndividualCourse(course.name)) {
          const qty = sel.quantity || 0
          for (let i = 0; i < qty; i++) {
            courses.push({
              category: category,
              name: course.name + (qty > 1 ? ` (${i + 1})` : ''),
              teacher: teacherName || '待定',
              semester: semesterMap[sel.semester] || `第${sel.semester}学期`,
              credit: course.credit
            })
          }
        } else {
          courses.push({
            category: category,
            name: course.name,
            teacher: teacherName || '待定',
            semester: semesterMap[sel.semester] || `第${sel.semester}学期`,
            credit: course.credit
          })
        }
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
    filteredGeneralElectiveCourses() {
      if (!this.generalElectiveCategoryFilter) {
        return this.generalElectiveCourses
      }
      return this.generalElectiveCourses.filter(course => {
        return course.topic_category === this.generalElectiveCategoryFilter
      })
    }
  },
  methods: {
    selectMajor(value) {
      this.selectedMajor = value
      if (value === 'computer_category') {
        this.currentStep = 1
      } else {
        this.currentStep = 3
        this.loadGeneralCourses()
      }
    },
    selectSubMajor(value) {
      this.selectedSubMajor = value
      if (value === 'big_data') {
        this.currentStep = 3
        this.loadGeneralCourses()
      } else {
        this.currentStep = 2
      }
    },
    selectClassType(value) {
      this.selectedClassType = value
      this.currentStep = 3
      this.loadGeneralCourses()
    },
    async loadGeneralCourses() {
      this.loading = true
      try {
        const response = await request.get('/courses', {
          params: {
            course_type: '通识必修'
          }
        })
        this.generalCourses = response
        this.initGeneralCourseSelections()
      } catch (error) {
        console.error('加载课程失败:', error)
        this.$message.error('加载课程失败，请稍后重试')
      } finally {
        this.loading = false
      }
    },
    goToEnglishClassSelection() {
      this.currentStep = 4
    },
    selectEnglishClass(value) {
      this.selectedEnglishClass = value
      this.loadEnglishCourses()
    },
    async loadEnglishCourses() {
      this.loading = true
      try {
        const response = await request.get('/courses', {
          params: {
            course_type: '英语必修',
            major_id: 1
          }
        })
        this.englishCourses = response
        this.initEnglishCourseSelections()
        this.currentStep = 5
      } catch (error) {
        console.error('加载英语课程失败:', error)
        this.$message.error('加载英语课程失败，请稍后重试')
      } finally {
        this.loading = false
      }
    },
    initEnglishCourseSelections() {
      this.englishCourseSelections = {}
      const isFast = this.selectedEnglishClass === 'fast'
      this.englishCourses.forEach(course => {
        const firstTeacherId = course.teacher_ids && course.teacher_ids.length > 0 ? course.teacher_ids[0] : null
        
        let defaultSemester = this.studySemesters[0].value
        if (course.major_study_semesters) {
          if (course.major_study_semesters[1] && course.major_study_semesters[1].length > 0) {
            defaultSemester = course.major_study_semesters[1][0]
          }
        }
        
        // 快班：大学英语2、大学英语3 固定选中；其他课程默认不选
        // 慢班：大学英语1、大学英语2、大学英语3 固定选中；其他课程默认不选
        let selected = false
        if (isFast) {
          if (course.name === '大学英语2' || course.name === '大学英语3') {
            selected = true
          }
        } else {
          if (course.name === '大学英语1' || course.name === '大学英语2' || course.name === '大学英语3') {
            selected = true
          }
        }
        
        this.englishCourseSelections[course.id] = {
          teacherId: firstTeacherId,
          semester: defaultSemester,
          selected: selected
        }
      })
    },
    isFixedEnglishCourse(courseName) {
      if (this.selectedEnglishClass === 'fast') {
        return courseName === '大学英语2' || courseName === '大学英语3'
      } else {
        return courseName === '大学英语1' || courseName === '大学英语2' || courseName === '大学英语3'
      }
    },
    async loadPECourses() {
      this.loading = true
      try {
        const response = await request.get('/courses', {
          params: {
            course_type: '体育必修',
            major_id: 1
          }
        })
        this.peCourses = response
        this.initPECourseSelections()
        this.currentStep = 6
      } catch (error) {
        console.error('加载体育课程失败:', error)
        this.$message.error('加载体育课程失败，请稍后重试')
      } finally {
        this.loading = false
      }
    },
    initPECourseSelections() {
      this.peCourseSelections = {}
      this.peCourses.forEach(course => {
        const firstTeacherId = course.teacher_ids && course.teacher_ids.length > 0 ? course.teacher_ids[0] : null
        let defaultSemester = this.studySemesters[0].value
        if (course.major_study_semesters) {
          if (course.major_study_semesters[1] && course.major_study_semesters[1].length > 0) {
            defaultSemester = course.major_study_semesters[1][0]
          }
        }
        let selected = false
        if (course.name === '基础体育' || course.name === '基础体育2') {
          selected = true
        }
        this.peCourseSelections[course.id] = {
          teacherId: firstTeacherId,
          semester: defaultSemester,
          selected: selected
        }
      })
    },
    isFixedPECourse(courseName) {
      return courseName === '基础体育' || courseName === '基础体育2'
    },
    isIntermediatePECourse(courseName) {
      return courseName.startsWith('中级')
    },
    getPrimaryNameFromIntermediate(intermediateName) {
      return intermediateName.replace('中级', '初级')
    },
    onPECourseSelectChange(course, val) {
      if (val && this.isIntermediatePECourse(course.name)) {
        const primaryName = this.getPrimaryNameFromIntermediate(course.name)
        const hasPrimary = this.peCourses.some(c => c.name === primaryName)
        if (!hasPrimary) {
          this.$message.warning(`请先选择「${primaryName}」课程`)
          this.peCourseSelections[course.id].selected = false
          return
        }
        const primarySelected = this.peCourses.some(c => c.name === primaryName && this.peCourseSelections[c.id] && this.peCourseSelections[c.id].selected)
        if (!primarySelected) {
          this.$message.warning(`请先选择「${primaryName}」课程`)
          this.peCourseSelections[course.id].selected = false
          return
        }
      }
    },
    async loadAcademicCourses() {
      this.loading = true
      try {
        // 计算机类专业的学科必修课程按照"计算机类"获取
        let majorId = this.getBackendMajorId()
        if (this.selectedMajor === 'computer_category') {
          majorId = 8 // 计算机类的专业ID
        }
        const response = await request.get('/courses', {
          params: {
            course_type: '学科必修',
            major_id: majorId
          }
        })
        this.academicCourses = response
        this.initAcademicCourseSelections(majorId)
        this.currentStep = 7
      } catch (error) {
        console.error('加载课程失败:', error)
        this.$message.error('加载课程失败，请稍后重试')
      } finally {
        this.loading = false
      }
    },
    initAcademicCourseSelections(majorId) {
      this.academicCourseSelections = {}
      this.academicCourses.forEach(course => {
        // 为每门课初始化选择
        const firstTeacherId = course.teacher_ids && course.teacher_ids.length > 0 ? course.teacher_ids[0] : null
        
        // 确定默认学期：优先使用建议修读学期
        let defaultSemester = this.studySemesters[0].value
        if (course.major_study_semesters) {
          // 使用传入的majorId（计算机类情况下为8）
          if (majorId && course.major_study_semesters[majorId] && course.major_study_semesters[majorId].length > 0) {
            defaultSemester = course.major_study_semesters[majorId][0]
          } else if (course.major_study_semesters[1] && course.major_study_semesters[1].length > 0) {
            // 公共课（ID:1）是所有专业公用的
            defaultSemester = course.major_study_semesters[1][0]
          }
        }
        
        this.academicCourseSelections[course.id] = {
          teacherId: firstTeacherId,
          semester: defaultSemester,
          selected: true // 默认全选
        }
      })
    },
    handleAfterAcademic() {
      if (this.selectedMajor === 'ai_exp') {
        this.currentStep = 10
      } else {
        this.loadMajorRequiredCourses()
      }
    },
    async loadMajorRequiredCourses() {
      this.loading = true
      try {
        let majorId = this.getBackendMajorId()
        const response = await request.get('/courses', {
          params: {
            course_type: '专业必修',
            major_id: majorId,
            major_course_type: '必修'
          }
        })
        this.majorRequiredCourses = response
        this.initMajorRequiredCourseSelections(majorId)
        this.currentStep = 8
      } catch (error) {
        console.error('加载专业必修课程失败:', error)
        this.$message.error('加载专业必修课程失败，请稍后重试')
      } finally {
        this.loading = false
      }
    },
    initMajorRequiredCourseSelections(majorId) {
      this.majorRequiredCourseSelections = {}
      this.majorRequiredCourses.forEach(course => {
        const firstTeacherId = course.teacher_ids && course.teacher_ids.length > 0 ? course.teacher_ids[0] : null
        
        let defaultSemester = this.studySemesters[0].value
        if (course.major_study_semesters) {
          if (majorId && course.major_study_semesters[majorId] && course.major_study_semesters[majorId].length > 0) {
            defaultSemester = course.major_study_semesters[majorId][0]
          } else if (course.major_study_semesters[1] && course.major_study_semesters[1].length > 0) {
            defaultSemester = course.major_study_semesters[1][0]
          }
        }
        
        this.majorRequiredCourseSelections[course.id] = {
          teacherId: firstTeacherId,
          semester: defaultSemester,
          selected: true
        }
      })
    },
    async loadMajorElectiveCourses() {
      this.loading = true
      try {
        let majorId = this.getBackendMajorId()
        const response = await request.get('/courses', {
          params: {
            course_type: '专业选修',
            major_id: majorId,
            major_course_type: '选修'
          }
        })
        this.majorElectiveCourses = response
        this.initMajorElectiveCourseSelections(majorId)
        this.currentStep = 9
      } catch (error) {
        console.error('加载专业选修课程失败:', error)
        this.$message.error('加载专业选修课程失败，请稍后重试')
      } finally {
        this.loading = false
      }
    },
    initMajorElectiveCourseSelections(majorId) {
      this.majorElectiveCourseSelections = {}
      this.majorElectiveCourses.forEach(course => {
        const firstTeacherId = course.teacher_ids && course.teacher_ids.length > 0 ? course.teacher_ids[0] : null
        
        let defaultSemester = this.studySemesters[0].value
        if (course.major_study_semesters) {
          if (majorId && course.major_study_semesters[majorId] && course.major_study_semesters[majorId].length > 0) {
            defaultSemester = course.major_study_semesters[majorId][0]
          } else if (course.major_study_semesters[1] && course.major_study_semesters[1].length > 0) {
            defaultSemester = course.major_study_semesters[1][0]
          }
        }
        
        this.majorElectiveCourseSelections[course.id] = {
          teacherId: firstTeacherId,
          semester: defaultSemester,
          selected: false
        }
      })
    },
    async loadPracticeCourses() {
      this.loading = true
      try {
        let majorId = this.getBackendMajorId()
        const response = await request.get('/courses', {
          params: {
            course_type: '实践课',
            major_id: majorId,
            major_course_type: '必修'
          }
        })
        // 对计算机(2)和软件(3)专业，根据班级类型过滤 topic_category
        let filteredCourses = response
        if (this.selectedClassType && (majorId === 2 || majorId === 3)) {
          const classTypeLabel = this.selectedClassType === 'excellence' ? '卓越工程师' : '普通班'
          filteredCourses = response.filter(course => {
            if (!course.topic_category) return false
            const categories = course.topic_category.split(',').map(c => c.trim())
            return categories.includes(classTypeLabel)
          })
        }
        this.practiceCourses = filteredCourses
        this.initPracticeCourseSelections(majorId)
        this.currentStep = 10
      } catch (error) {
        console.error('加载实践课程失败:', error)
        this.$message.error('加载实践课程失败，请稍后重试')
      } finally {
        this.loading = false
      }
    },
    initPracticeCourseSelections(majorId) {
      this.practiceCourseSelections = {}
      this.practiceCourses.forEach(course => {
        const firstTeacherId = course.teacher_ids && course.teacher_ids.length > 0 ? course.teacher_ids[0] : null
        
        let defaultSemester = this.studySemesters[0].value
        if (course.major_study_semesters) {
          if (majorId && course.major_study_semesters[majorId] && course.major_study_semesters[majorId].length > 0) {
            defaultSemester = course.major_study_semesters[majorId][0]
          } else if (course.major_study_semesters[1] && course.major_study_semesters[1].length > 0) {
            defaultSemester = course.major_study_semesters[1][0]
          }
        }
        
        this.practiceCourseSelections[course.id] = {
          teacherId: firstTeacherId,
          semester: defaultSemester,
          selected: true
        }
      })
    },
    async loadGeneralElectiveCourses() {
      this.loading = true
      try {
        const response = await request.get('/courses', {
          params: {
            course_type: '通识选修',
            major_id: 1
          }
        })
        this.generalElectiveCourses = response
        this.initGeneralElectiveCourseSelections()
        this.currentStep = 11
      } catch (error) {
        console.error('加载通识选修课程失败:', error)
        this.$message.error('加载通识选修课程失败，请稍后重试')
      } finally {
        this.loading = false
      }
    },
    initGeneralElectiveCourseSelections() {
      this.generalElectiveCourseSelections = {}
      this.generalElectiveCourses.forEach(course => {
        const firstTeacherId = course.teacher_ids && course.teacher_ids.length > 0 ? course.teacher_ids[0] : null
        let defaultSemester = this.studySemesters[0].value
        if (course.major_study_semesters) {
          if (course.major_study_semesters[1] && course.major_study_semesters[1].length > 0) {
            defaultSemester = course.major_study_semesters[1][0]
          }
        }
        let selected = false
        if (this.isFixedGeneralElective(course.name)) {
          selected = true
        }
        this.generalElectiveCourseSelections[course.id] = {
          teacherId: firstTeacherId,
          semester: defaultSemester,
          selected: selected,
          quantity: 0
        }
      })
    },
    isFixedGeneralElective(courseName) {
      return courseName === '当代大学生国家安全教育(GX)'
    },
    isArtCourse(course) {
      return course.topic_category === '艺术审美类'
    },
    isHistoryCourse(course) {
      return course.topic_category === '四史类'
    },
    isInnovationCourse(course) {
      return course.topic_category === '创新创业类'
    },
    isPlaceholderCourse(courseName) {
      return courseName.includes('学分通识选修课')
    },
    onGeneralElectiveChange(course, val) {
      if (!val && this.isFixedGeneralElective(course.name)) {
        this.generalElectiveCourseSelections[course.id].selected = true
      }
    },
    onPlaceholderQuantityChange(course, val) {
      if (val > 0) {
        this.generalElectiveCourseSelections[course.id].selected = true
      } else {
        this.generalElectiveCourseSelections[course.id].selected = false
      }
    },
    categoryCount(category) {
      return this.generalElectiveCourses.filter(c => c.topic_category === category).length
    },
    async loadIndividualCourses() {
      this.loading = true
      try {
        const response = await request.get('/courses', {
          params: {
            course_type: '个性课程',
            major_id: 1
          }
        })
        this.individualCourses = response
        this.initIndividualCourseSelections()
        this.currentStep = 12
      } catch (error) {
        console.error('加载个性课程失败:', error)
        this.$message.error('加载个性课程失败，请稍后重试')
      } finally {
        this.loading = false
      }
    },
    initIndividualCourseSelections() {
      this.individualCourseSelections = {}
      this.individualCourses.forEach(course => {
        const firstTeacherId = course.teacher_ids && course.teacher_ids.length > 0 ? course.teacher_ids[0] : null
        let defaultSemester = this.studySemesters[0].value
        if (course.major_study_semesters) {
          if (course.major_study_semesters[1] && course.major_study_semesters[1].length > 0) {
            defaultSemester = course.major_study_semesters[1][0]
          }
        }
        this.individualCourseSelections[course.id] = {
          teacherId: firstTeacherId,
          semester: defaultSemester,
          selected: false,
          quantity: 0
        }
      })
    },
    isPlaceholderIndividualCourse(courseName) {
      return courseName.includes('学分个性课')
    },
    onIndividualCourseChange(course, val) {
    },
    onIndividualPlaceholderQuantityChange(course, val) {
      if (val > 0) {
        this.individualCourseSelections[course.id].selected = true
      } else {
        this.individualCourseSelections[course.id].selected = false
      }
    },
    goToSummary() {
      this.currentStep = 13
    },
    exportSummary() {
      const semesterMap = {
        1: '第1学期', 2: '第2学期', 3: '第3学期', 4: '第4学期',
        5: '第5学期', 6: '第6学期', 7: '第7学期', 8: '第8学期'
      }
      let text = '===== 选课清单 =====\n\n'
      text += `专业: ${this.getMajorLabel(this.selectedMajor)}\n`
      if (this.selectedSubMajor) text += `方向: ${this.getSubMajorLabel(this.selectedSubMajor)}\n`
      if (this.selectedClassType) text += `班级: ${this.getClassTypeLabel(this.selectedClassType)}\n`
      text += `总学分: ${this.totalSelectedCreditsWithIndividual}\n\n`
      text += '序号\t课程类别\t课程名称\t授课教师\t修读学期\t学分\n'
      text += '-\t-\t-\t-\t-\t-\n'
      this.summaryCourses.forEach((c, i) => {
        text += `${i + 1}\t${c.category}\t${c.name}\t${c.teacher}\t${c.semester}\t${c.credit}\n`
      })
      text += '\n===== 学分明细 =====\n'
      text += `通识必修: ${this.selectedGeneralCredits} 学分\n`
      text += `英语必修: ${this.selectedEnglishCredits} 学分\n`
      text += `体育必修: ${this.selectedPECredits} 学分\n`
      text += `学科必修: ${this.selectedAcademicCredits} 学分\n`
      text += `专业必修: ${this.selectedMajorRequiredCredits} 学分\n`
      text += `专业选修: ${this.selectedMajorElectiveCredits} 学分\n`
      text += `实践课: ${this.selectedPracticeCredits} 学分\n`
      text += `通识选修: ${this.selectedGeneralElectiveCredits} 学分\n`
      text += `个性课程: ${this.selectedIndividualCredits} 学分\n`
      text += `总计: ${this.totalSelectedCreditsWithIndividual} 学分\n`
      const blob = new Blob([text], { type: 'text/plain;charset=utf-8' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `选课清单_${this.getMajorLabel(this.selectedMajor)}.txt`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    },
    initGeneralCourseSelections() {
      this.generalCourseSelections = {}
      this.generalCourses.forEach(course => {
        // 为每门课初始化选择
        const firstTeacherId = course.teacher_ids && course.teacher_ids.length > 0 ? course.teacher_ids[0] : null
        
        // 确定默认学期：通识必修从公共课专业抽取（只使用建议修读学期）
        let defaultSemester = this.studySemesters[0].value
        if (course.major_study_semesters) {
          // 公共课（ID:1）是所有专业公用的，直接从公共课专业抽取
          if (course.major_study_semesters[1] && course.major_study_semesters[1].length > 0) {
            defaultSemester = course.major_study_semesters[1][0]
          }
        }
        
        this.generalCourseSelections[course.id] = {
          teacherId: firstTeacherId,
          semester: defaultSemester,
          selected: true // 默认全选
        }
      })
    },
    getBackendMajorId() {
      // 映射前端专业选择到后端专业ID（云端数据库实际ID）
      const majorMap = {
        'computer_category': 8, // 计算机类
        'ai': 5, // 人工智能
        'software_exp': 6, // 软件（实验）
        'ai_exp': 7 // 人工智能（实验）
      }
      const subMajorMap = {
        'computer': 2, // 计算机
        'software': 3, // 软件
        'big_data': 4 // 大数据
      }
      
      if (this.selectedSubMajor) {
        return subMajorMap[this.selectedSubMajor]
      }
      return majorMap[this.selectedMajor] || 8
    },
    isPolicyCourse(courseName) {
      return courseName.includes('形势与政策')
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
    },
    goBack() {
      if (this.currentStep === 1) {
        this.currentStep = 0
        this.selectedMajor = null
      } else if (this.currentStep === 2) {
        this.currentStep = 1
        this.selectedSubMajor = null
      } else if (this.currentStep === 3) {
        if (this.selectedClassType) {
          this.currentStep = 2
          this.selectedClassType = null
        } else if (this.selectedSubMajor) {
          this.currentStep = 1
          this.selectedSubMajor = null
        } else {
          this.currentStep = 0
          this.selectedMajor = null
        }
        this.generalCourses = []
        this.generalCourseSelections = {}
      } else if (this.currentStep === 4) {
        this.currentStep = 3
        this.selectedEnglishClass = null
      } else if (this.currentStep === 5) {
        this.currentStep = 4
        this.englishCourses = []
        this.englishCourseSelections = {}
      } else if (this.currentStep === 6) {
        this.currentStep = 5
        this.peCourses = []
        this.peCourseSelections = {}
      } else if (this.currentStep === 7) {
        this.currentStep = 6
        this.academicCourses = []
        this.academicCourseSelections = {}
      } else if (this.currentStep === 8) {
        this.currentStep = 7
        this.majorRequiredCourses = []
        this.majorRequiredCourseSelections = {}
      } else if (this.currentStep === 9) {
        this.currentStep = 8
        this.majorElectiveCourses = []
        this.majorElectiveCourseSelections = {}
      } else if (this.currentStep === 10) {
        if (this.selectedMajor === 'ai_exp') {
          this.currentStep = 7
        } else {
          this.currentStep = 9
          this.practiceCourses = []
          this.practiceCourseSelections = {}
        }
      } else if (this.currentStep === 11) {
        this.currentStep = 10
        this.generalElectiveCourses = []
        this.generalElectiveCourseSelections = {}
      } else if (this.currentStep === 12) {
        this.currentStep = 11
        this.individualCourses = []
        this.individualCourseSelections = {}
      } else if (this.currentStep === 13) {
        this.currentStep = 12
      }
    },
    getMajorLabel(value) {
      const m = this.majors.find(x => x.value === value)
      return m ? m.label : value
    },
    getSubMajorLabel(value) {
      const m = this.subMajors.find(x => x.value === value)
      return m ? m.label : value
    },
    getClassTypeLabel(value) {
      const m = this.classTypes.find(x => x.value === value)
      return m ? m.label : value
    },
    goHome() {
      const role = localStorage.getItem('role')
      if (role === 'admin' || role === 'superadmin') {
        this.$router.push('/admin')
      } else {
        this.$router.push('/student')
      }
    },
    handleLogout() {
      this.$confirm('确定要退出模拟选课吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        localStorage.clear()
        this.$router.push('/login')
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.85);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
  padding: 0 20px;
}

.header h2 {
  font-size: 20px;
  color: #333;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.main {
  padding: 10px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
}

.step-content {
  padding: 15px 0;
  min-height: 300px;
}

.step-title {
  text-align: center;
  font-size: 22px;
  color: #333;
  margin-bottom: 20px;
  font-weight: normal;
}

/* 统一按钮样式 */
:deep(.el-button--primary) {
  background: rgba(0, 136, 255, 0.78) !important;
  border: none !important;
  border-radius: 20px !important;
  padding: 15px 20px !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  transition: all 0.3s ease !important;
}

:deep(.el-button--primary:hover:not(:disabled)) {
  background: rgba(0, 136, 255, 0.91) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 2px 8px rgba(0, 136, 255, 0.3) !important;
}

:deep(.el-button--danger) {
  background: rgba(255, 69, 69, 0.78) !important;
  border: none !important;
  border-radius: 20px !important;
  padding: 15px 20px !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  transition: all 0.3s ease !important;
}

:deep(.el-button--danger:hover:not(:disabled)) {
  background: rgba(255, 69, 69, 0.91) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 2px 8px rgba(255, 69, 69, 0.3) !important;
}

:deep(.el-button--default) {
  border: 1px solid #dcdfe6 !important;
  border-radius: 20px !important;
  padding: 15px 20px !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  transition: all 0.3s ease !important;
}

:deep(.el-button--default:hover:not(:disabled)) {
  border-color: #409eff !important;
  color: #409eff !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.2) !important;
}

.option-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.option-grid.two-col {
  grid-template-columns: repeat(2, 1fr);
  max-width: 500px;
}

.option-card {
  background: rgba(255, 255, 255, 0.75);
  border: 2px solid rgba(200, 200, 200, 0.5);
  border-radius: 16px;
  padding: 30px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.option-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 136, 255, 0.15);
  border-color: rgba(0, 136, 255, 0.4);
}

.option-card.selected {
  border-color: #0088ff;
  background: rgba(0, 136, 255, 0.08);
  box-shadow: 0 8px 24px rgba(0, 136, 255, 0.2);
}

.option-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.option-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.option-desc {
  font-size: 13px;
  color: #999;
  margin-top: 8px;
}

.nav-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  padding: 20px 0;
}

.selection-summary {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 20px;
  padding: 15px;
  background: rgba(0, 136, 255, 0.05);
  border-radius: 12px;
}

.credit-scoreboard {
  margin-bottom: 20px;
}

.scoreboard-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  color: white;
  border: none !important;
}

.scoreboard-card :deep(.el-card__body) {
  padding: 15px;
}

.scoreboard-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

.score-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.score-item.total {
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 16px;
  border-radius: 8px;
}

.score-label {
  font-size: 14px;
  opacity: 0.9;
}

.score-value {
  font-size: 20px;
  font-weight: bold;
}

.score-divider {
  width: 1px;
  height: 40px;
  background: rgba(255, 255, 255, 0.3);
}

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  gap: 10px;
  font-size: 16px;
  color: #666;
}

.empty-state {
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.course-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

@media screen and (max-width: 1024px) {
  .course-list {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media screen and (max-width: 768px) {
  .course-list {
    grid-template-columns: 1fr;
  }
}

.course-card {
  background: rgba(255, 255, 255, 0.75) !important;
  border: 1px solid rgba(200, 200, 200, 0.5) !important;
  border-radius: 16px !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
}

.course-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.course-name {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.course-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 5px;
}

.credit {
  background: rgba(0, 136, 255, 0.1);
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  color: #0088ff;
}

.college {
  font-size: 12px;
  color: #999;
}

.course-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.course-description {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

.teacher-selection,
.semester-selection {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.teacher-selection h4,
.semester-selection h4 {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.teacher-selection :deep(.el-radio-group) {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.teacher-selection :deep(.el-radio-button) {
  margin-bottom: 8px;
  border-radius: 16px !important;
}

.teacher-name {
  margin-right: 8px;
  white-space: nowrap;
}

.teacher-rating {
  display: inline-flex;
  align-items: center;
  margin-left: 4px;
}

.teacher-rating :deep(.el-rate) {
  font-size: 12px;
}

.teacher-rating :deep(.el-rate__text) {
  font-size: 12px;
  margin-left: 4px;
}

@media screen and (max-width: 768px) {
  .option-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .option-card {
    padding: 20px 15px;
  }

  .option-icon {
    font-size: 36px;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .course-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .course-info {
    align-items: flex-start;
  }

  .nav-buttons {
    flex-direction: column;
    align-items: center;
  }
}

.course-checkbox {
  flex: 1;
}

.course-checkbox :deep(.el-checkbox__label) {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.course-selected {
  border-color: #0088ff !important;
  background: rgba(0, 136, 255, 0.05) !important;
  box-shadow: 0 4px 16px rgba(0, 136, 255, 0.15) !important;
}

.score-value.requirement {
  color: #ffd700;
}

.credit-warning {
  margin-top: 10px;
}

.credit-success {
  margin-top: 10px;
}

.quantity-selection {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed #e8e8e8;
}

.quantity-selection h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #666;
}

.quantity-hint {
  margin-left: 10px;
  font-size: 12px;
  color: #999;
}

.category-filter {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  padding: 12px 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e8e8e8;
}

.filter-label {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  white-space: nowrap;
}

.summary-credit-total {
  margin-bottom: 20px;
}

.summary-title {
  margin: 0 0 16px 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.summary-table-wrapper {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e8e8e8;
}

.multi-row-steps {
  display: flex;
  flex-wrap: nowrap;
  gap: 4px 0;
  width: 100%;
  max-width: 100%;
  overflow-x: auto;
}
.multi-row-steps::-webkit-scrollbar {
  display: none;
}
.multi-row-steps {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.multi-row-steps .el-step {
  flex: 0 0 7.14%;
  min-width: 0;
}
.multi-row-steps .el-step__title {
  font-size: 12px;
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
