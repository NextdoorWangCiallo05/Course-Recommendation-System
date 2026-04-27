<template>
  <div class="dashboard">
    <el-header class="header">
      <h2 v-if="adminMode">选课推荐系统 - 管理员后台</h2>
      <h2 v-else>选课推荐系统</h2>
      <div class="user-info">
        <span>欢迎, {{ username }}</span>
        <el-button v-if="!adminMode" type="warning" size="small" @click="openSimulatedSelection">模拟选课</el-button>
        <el-button v-if="!adminMode" type="primary" size="small" @click="openFeedback">反馈</el-button>
        <el-button v-if="!adminMode" type="success" size="small" @click="goToUserCenter">用户中心</el-button>
        <el-button v-if="isAdmin" type="primary" size="small" class="purple-btn" @click="toggleAdminMode">{{ adminMode ? '返回学生端' : '管理面板' }}</el-button>
        <el-button type="danger" size="small" @click="handleLogout">退出</el-button>
      </div>
    </el-header>
    <el-container class="main" v-if="adminMode" :style="mainBgStyle">
      <el-aside width="200px">
        <el-menu
          :default-active="activeMenu"
          @select="handleMenuSelect"
          background-color="transparent"
          text-color="#333"
          active-text-color="#0088ff"
        >
          <el-menu-item index="courses">课程管理</el-menu-item>
          <el-menu-item index="evaluations">评价管理</el-menu-item>
          <el-menu-item index="feedback">用户反馈</el-menu-item>
          <el-menu-item v-if="isSuperAdmin" index="users">账户管理</el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>
        <div v-if="activeMenu === 'courses'">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>课程列表</span>
                <div>
                  <el-button type="primary" @click="openCourseDialog">添加课程</el-button>
                  <el-button type="danger" @click="batchDeleteCourses" :disabled="selectedCourses.length === 0">批量删除</el-button>
                  <el-button v-if="isSuperAdmin" type="danger" @click="clearAllData">清空所有数据</el-button>
                </div>
              </div>
            </template>
            <el-form :inline="true" class="search-form">
              <el-form-item label="搜索">
                <el-input v-model="searchKeyword" placeholder="搜索课程名" clearable @input="filterCourses" style="width: 200px;" />
              </el-form-item>
              <el-form-item label="教师搜索">
                <el-input v-model="teacherKeyword" placeholder="搜索教师名（支持拼音缩写）" clearable @input="filterCourses" style="width: 180px;" />
              </el-form-item>
              <el-form-item label="专业">
                <el-select v-model="searchMajor" placeholder="全部专业" clearable @change="loadCourses" style="width: 150px;">
                  <el-option v-for="m in majors" :key="m.id" :label="m.name" :value="m.id" />
                </el-select>
              </el-form-item>
              <el-form-item label="开课学院">
                <el-select v-model="searchCollege" placeholder="全部学院" clearable @change="filterCourses" style="width: 150px;">
                  <el-option v-for="college in colleges" :key="college" :label="college" :value="college" />
                </el-select>
              </el-form-item>
              <el-form-item label="课程性质">
                <el-select v-model="courseTypeFilter" multiple placeholder="全部课程性质" clearable @change="filterCourses" style="width: 200px;">
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
              <el-form-item label="必修/选修" v-if="searchMajor">
                <el-select v-model="majorCourseTypeFilter" placeholder="全部" clearable @change="filterCourses" style="width: 120px;">
                  <el-option label="必修" value="必修" />
                  <el-option label="选修" value="选修" />
                </el-select>
              </el-form-item>
              <el-form-item label="排序">
                <el-select v-model="sortOrder" @change="loadCourses" style="width: 120px;">
                  <el-option label="升序" value="asc" />
                  <el-option label="降序" value="desc" />
                </el-select>
              </el-form-item>
            </el-form>
            <el-table :data="courses" border stripe style="width: 100%" @selection-change="handleCourseSelectionChange">
              <el-table-column type="selection" width="50" />
              <el-table-column prop="order_num" label="序号" width="70" />
              <el-table-column prop="name" label="课程名" min-width="120" />
              <el-table-column prop="credit" label="学分" width="60" />
              <el-table-column prop="college" label="开课学院" min-width="100" />
              <el-table-column prop="assessment_method" label="考核方式" width="100" />
              <el-table-column label="主题类别" width="120">
                <template #default="{ row }">
                  <span v-if="row.topic_category">{{ row.topic_category }}</span>
                  <span v-else style="color: #909399;">-</span>
                </template>
              </el-table-column>
              <el-table-column prop="major_names" label="专业" min-width="80" />
              <el-table-column prop="teacher_names" label="教师" min-width="100" />
              <el-table-column label="课程性质" width="100">
                <template #default="{ row }">
                  <span>{{ row.course_types ? row.course_types.join('、') : (row.course_type || '') }}</span>
                </template>
              </el-table-column>
              <el-table-column label="开课学期" width="90">
                <template #default="{ row }">
                  <span>{{ row.semesters ? row.semesters.join('、') : '' }}</span>
                </template>
              </el-table-column>
              <el-table-column label="评分" min-width="150">
                <template #default="{ row }">
                  <div v-if="row.teacher_ratings && Object.keys(row.teacher_ratings).length > 0">
                    <div v-for="(rating, teacherId) in row.teacher_ratings" :key="teacherId">
                        <span>{{ getTeacherName(row, teacherId) }}: </span>
                        <el-rate :model-value="rating" disabled show-score style="width: 120px;" />
                      </div>
                  </div>
                  <div v-else>
                    <el-rate :model-value="row.avg_rating" disabled show-score style="width: 120px;" />
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="140" fixed="right">
                <template #default="{ row }">
                  <div class="table-actions">
                    <el-button type="primary" size="small" @click="editCourse(row)">编辑</el-button>
                    <el-button type="danger" size="small" @click="deleteCourse(row.id)">删除</el-button>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </div>
        <div v-if="activeMenu === 'evaluations'">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>评价列表</span>
                <div>
                  <el-button type="primary" @click="showEvalDialog = true">添加评价</el-button>
                  <el-button v-if="isSuperAdmin" type="danger" @click="clearEvaluations">清空评价</el-button>
                </div>
              </div>
            </template>
            <el-form :inline="true" class="search-form">
              <el-form-item label="课程名">
                <el-input v-model="evalCourseKeyword" placeholder="搜索课程名" clearable @input="filterEvaluations" style="width: 200px;" />
              </el-form-item>
              <el-form-item label="教师名">
                <el-input v-model="evalTeacherKeyword" placeholder="搜索教师名（支持拼音缩写）" clearable @input="filterEvaluations" style="width: 200px;" />
              </el-form-item>
            </el-form>
            <el-table :data="filteredEvaluations" border stripe style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="course_name" label="课程" width="150" />
              <el-table-column prop="teacher_name" label="教师" width="120" />
              <el-table-column prop="rating" label="星级" width="200">
                <template #default="{ row }">
                  <el-rate v-model="row.rating" disabled show-score style="width: 160px;" />
                </template>
              </el-table-column>
              <el-table-column prop="comment" label="评语" />
              <el-table-column prop="created_at" label="时间" width="180" />
              <el-table-column label="操作" width="150">
                <template #default="{ row }">
                  <div class="table-actions">
                    <el-button type="primary" size="small" @click="editEvaluation(row)">编辑</el-button>
                    <el-button type="danger" size="small" @click="deleteEvaluation(row.id)">删除</el-button>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </div>
        <div v-if="activeMenu === 'feedback'">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>用户反馈列表</span>
              </div>
            </template>
            <el-table :data="feedbacks" border stripe style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="username" label="用户" width="150" />
              <el-table-column prop="content" label="反馈内容" />
              <el-table-column prop="created_at" label="提交时间" width="180" />
              <el-table-column label="操作" width="100">
                <template #default="{ row }">
                  <el-button type="danger" size="small" @click="handleDeleteFeedback(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </div>
        <div v-if="activeMenu === 'preview'">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>学生端预览</span>
              </div>
            </template>
            <el-form :inline="true" class="search-form">
              <el-form-item label="搜索">
                <el-input v-model="previewSearchKeyword" placeholder="搜索课程名" clearable @input="filterPreviewCourses" style="width: 200px;" />
              </el-form-item>
              <el-form-item label="专业分类">
                <el-select v-model="previewSelectedMajor" placeholder="全部专业" clearable @change="onPreviewMajorChange" style="width: 200px;">
                  <el-option v-for="m in majors" :key="m.id" :label="m.name" :value="m.id" />
                </el-select>
              </el-form-item>
              <el-form-item label="开课学院">
                <el-select v-model="previewSelectedCollege" placeholder="全部学院" clearable @change="filterPreviewCourses" style="width: 200px;">
                  <el-option v-for="college in previewColleges" :key="college" :label="college" :value="college" />
                </el-select>
              </el-form-item>
              <el-form-item label="课程性质">
                <el-select v-model="previewSelectedCourseType" multiple placeholder="全部课程性质" clearable @change="loadPreviewCourses" style="width: 220px;">
                  <el-option label="学科必修" value="学科必修" />
                  <el-option label="专业必修" value="专业必修" />
                  <el-option label="专业选修" value="专业选修" />
                  <el-option label="实践课" value="实践课" />
                  <el-option label="英语必修" value="英语必修" />
                  <el-option label="体育必修" value="体育必修" />
                </el-select>
              </el-form-item>
              <el-form-item v-if="previewSelectedMajor" label="必修/选修">
                <el-select v-model="previewSelectedMajorCourseType" placeholder="全部" clearable @change="loadPreviewCourses" style="width: 150px;">
                  <el-option label="必修" value="必修" />
                  <el-option label="选修" value="选修" />
                </el-select>
              </el-form-item>
              <el-form-item label="教师搜索">
                <el-input v-model="previewTeacherKeyword" placeholder="搜索教师名（支持拼音缩写）" clearable @input="filterPreviewCourses" style="width: 180px;" />
              </el-form-item>
            </el-form>
            <el-row :gutter="20">
              <el-col v-for="course in previewCourses" :key="course.id" :xs="24" :sm="12" :md="8" :lg="6">
                <el-card class="preview-course-card" shadow="hover" @click="showPreviewDetail(course)">
                  <div class="preview-card-header">
                    <span class="preview-course-name">{{ course.name }}</span>
                  </div>
                  <div class="preview-card-tags">
                    <el-tag type="info" size="small">{{ course.major_names }}</el-tag>
                    <el-tag v-if="previewSelectedMajor && course.major_course_types && course.major_course_types[previewSelectedMajor]"
                      :type="course.major_course_types[previewSelectedMajor] === '必修' ? 'danger' : 'success'" size="small">
                      {{ course.major_course_types[previewSelectedMajor] }}
                    </el-tag>
                  </div>
                  <div class="preview-card-body">
                    <p><strong>学分:</strong> {{ course.credit }}</p>
                    <p v-if="course.college"><strong>开课学院:</strong> {{ course.college }}</p>
                    <p><strong>考核方式:</strong> {{ course.assessment_method || '闭卷笔试' }}</p>
                    <p><strong>教师:</strong> {{ course.teacher_names }}</p>
                    <p><strong>课程性质:</strong> {{ course.course_types ? course.course_types.join('、') : (course.course_type || '') }}</p>
                    <p><strong>开课学期:</strong> {{ course.semesters ? course.semesters.join('、') : '' }}</p>
                    <p v-if="previewSelectedMajor && course.major_study_semesters && course.major_study_semesters[previewSelectedMajor] && course.major_study_semesters[previewSelectedMajor].length > 0">
                      <strong>建议修读学期:</strong> {{ course.major_study_semesters[previewSelectedMajor].join('、') }}
                    </p>
                    <div v-if="course.teacher_ratings && Object.keys(course.teacher_ratings).length > 0" class="preview-ratings">
                      <div v-for="(rating, teacherId) in course.teacher_ratings" :key="teacherId" class="preview-rating-item">
                        <span>{{ getPreviewTeacherName(teacherId) }}: </span>
                        <el-rate :model-value="rating" disabled show-score text-color="#ff9900" style="width: 120px;" />
                        <span style="margin-left: 30px; color: #909399; font-size: 12px;">({{ course.teacher_evaluation_counts?.[teacherId] || 0 }}人评价)</span>
                      </div>
                    </div>
                    <p v-else><strong>评分:</strong> 暂无评价</p>
                    <p class="preview-course-desc" :title="course.description">
                      <strong>概述:</strong> {{ course.description || '暂无介绍' }}
                    </p>
                  </div>
                </el-card>
              </el-col>
            </el-row>
            <el-empty v-if="previewCourses.length === 0" description="暂无课程" />
          </el-card>
        </div>

        <el-dialog v-model="showPreviewDetailDialog" :title="selectedPreviewCourse ? selectedPreviewCourse.name : ''" width="600px">
          <el-descriptions :column="1" border v-if="selectedPreviewCourse">
            <el-descriptions-item label="学分">{{ selectedPreviewCourse.credit }}</el-descriptions-item>
            <el-descriptions-item label="开课学院" v-if="selectedPreviewCourse.college">{{ selectedPreviewCourse.college }}</el-descriptions-item>
            <el-descriptions-item label="考核方式">{{ selectedPreviewCourse.assessment_method || '闭卷笔试' }}</el-descriptions-item>
            <el-descriptions-item label="专业">
              <div>
                <span>{{ selectedPreviewCourse.major_names }}</span>
                <el-tag v-if="previewSelectedMajor && selectedPreviewCourse.major_course_types && selectedPreviewCourse.major_course_types[previewSelectedMajor]"
                  size="small" :type="selectedPreviewCourse.major_course_types[previewSelectedMajor] === '必修' ? 'danger' : 'success'" style="margin-left: 10px;">
                  {{ selectedPreviewCourse.major_course_types[previewSelectedMajor] }}
                </el-tag>
              </div>
            </el-descriptions-item>
            <el-descriptions-item label="授课教师">{{ selectedPreviewCourse.teacher_names }}</el-descriptions-item>
            <el-descriptions-item label="课程性质">{{ selectedPreviewCourse.course_types ? selectedPreviewCourse.course_types.join('、') : (selectedPreviewCourse.course_type || '') }}</el-descriptions-item>
            <el-descriptions-item label="开课学期">{{ selectedPreviewCourse.semesters ? selectedPreviewCourse.semesters.join('、') : '' }}</el-descriptions-item>
            <el-descriptions-item v-if="previewSelectedMajor && selectedPreviewCourse.major_study_semesters && selectedPreviewCourse.major_study_semesters[previewSelectedMajor] && selectedPreviewCourse.major_study_semesters[previewSelectedMajor].length > 0" label="建议修读学期">
              {{ selectedPreviewCourse.major_study_semesters[previewSelectedMajor].join('、') }}
            </el-descriptions-item>
            <el-descriptions-item v-if="selectedPreviewCourse.teacher_ratings && Object.keys(selectedPreviewCourse.teacher_ratings).length > 0" label="教师评分" :span="1">
              <div v-for="(rating, teacherId) in selectedPreviewCourse.teacher_ratings" :key="teacherId" style="margin-bottom: 5px;">
                <span>{{ getPreviewTeacherName(teacherId) }}: </span>
                <el-rate :model-value="rating" disabled show-score text-color="#FF8D28" style="width: 120px;" />
                <span style="margin-left: 30px; color: #909399; font-size: 12px;">({{ selectedPreviewCourse.teacher_evaluation_counts?.[teacherId] || 0 }}人评价)</span>
              </div>
            </el-descriptions-item>
            <el-descriptions-item v-else label="评分">暂无评价</el-descriptions-item>
            <el-descriptions-item label="课程概述">{{ selectedPreviewCourse.description || '暂无介绍' }}</el-descriptions-item>
          </el-descriptions>
        </el-dialog>
      </el-main>
    </el-container>

    <el-main class="main" v-if="!adminMode" :style="mainBgStyle">
      <el-card>
        <template #header>
          <div class="card-header card-header-tabs">
            <el-tabs v-model="mainSearchMode" @tab-change="handleMainTabChange">
              <el-tab-pane label="课程检索" name="course"></el-tab-pane>
              <el-tab-pane label="教师检索（计算机学院）" name="cs_course"></el-tab-pane>
            </el-tabs>
          </div>
        </template>
        <div v-if="mainSearchMode === 'course'">
          <el-form :inline="true" class="search-form">
            <el-form-item label="搜索">
              <el-input v-model="adminSearchKeyword" placeholder="搜索课程名" clearable @input="filterAdminCourses" style="width: 200px;" />
            </el-form-item>
            <el-form-item label="专业分类">
              <el-select v-model="adminSelectedMajor" placeholder="全部专业" clearable @change="onAdminMajorChange" style="width: 200px;">
                <el-option v-for="m in majors" :key="m.id" :label="m.name" :value="m.id" />
              </el-select>
            </el-form-item>
            <el-form-item label="开课学院">
              <el-select v-model="adminSelectedCollege" placeholder="全部学院" clearable @change="filterAdminCourses" style="width: 200px;">
                <el-option v-for="college in adminColleges" :key="college" :label="college" :value="college" />
              </el-select>
            </el-form-item>
            <el-form-item label="课程性质">
              <el-select v-model="adminSelectedCourseType" multiple placeholder="全部课程性质" clearable @change="loadAdminCourses" style="width: 220px;">
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
            <el-form-item v-if="adminSelectedMajor" label="必修/选修">
              <el-select v-model="adminSelectedMajorCourseType" placeholder="全部" clearable @change="loadAdminCourses" style="width: 150px;">
                <el-option label="必修" value="必修" />
                <el-option label="选修" value="选修" />
              </el-select>
            </el-form-item>
            <el-form-item label="教师搜索">
              <el-input v-model="adminTeacherKeyword" placeholder="搜索教师名" clearable @input="filterAdminCourses" style="width: 150px;" />
            </el-form-item>
          </el-form>
          <el-row :gutter="20">
            <el-col v-for="course in paginatedAdminCourses" :key="course.id" :xs="24" :sm="12" :md="8" :lg="6">
              <el-card class="course-card" shadow="hover" @click="showAdminCourseDetail(course)">
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
                  <p v-if="adminSelectedMajor && course.major_study_semesters && course.major_study_semesters[adminSelectedMajor] && course.major_study_semesters[adminSelectedMajor].length > 0">
                    <strong>建议修读学期:</strong> {{ course.major_study_semesters[adminSelectedMajor].join('、') }}
                  </p>
                  <p v-if="adminSelectedMajor && course.major_course_types && course.major_course_types[adminSelectedMajor]">
                    <strong>对本专业:</strong> {{ course.major_course_types[adminSelectedMajor] }}
                  </p>
                  <div v-if="course.teacher_ratings && Object.keys(course.teacher_ratings).length > 0">
                    <div v-for="(rating, teacherId) in course.teacher_ratings" :key="teacherId" style="margin-left: 20px;">
                      <span>{{ getAdminTeacherName(teacherId) }}: </span>
                      <el-rate :model-value="rating" disabled show-score text-color="#FF8D28" style="width: 120px;" />
                      <span style="margin-left: 30px; color: #909399; font-size: 12px;">({{ course.teacher_evaluation_counts?.[teacherId] || 0 }}人评价)</span>
                    </div>
                  </div>
                </div>
                <div class="card-actions">
                  <el-button type="primary" size="small" @click.stop="showAdminCourseDetail(course)">查看详情</el-button>
                </div>
              </el-card>
            </el-col>
          </el-row>
          <el-empty v-if="adminCourses.length === 0" description="暂无课程" />
          <el-pagination
            v-if="adminCourses.length > adminPageSize"
            v-model:current-page="adminCurrentPage"
            :page-size="adminPageSize"
            :total="adminCourses.length"
            layout="prev, pager, next"
            style="margin-top: 20px; justify-content: center;"
            @update:current-page="handleAdminPageChange"
          />
        </div>
        <div v-if="mainSearchMode === 'cs_course'">
          <el-form :inline="true" class="search-form">
            <el-form-item label="搜索教师">
              <el-input v-model="csTeacherKeyword" placeholder="搜索教师名" clearable @input="filterCsTeachers" style="width: 200px;" />
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
            <el-col v-for="teacher in filteredCsTeachers" :key="teacher.id" :xs="24" :sm="12" :md="8" :lg="6">
              <el-card class="course-card teacher-card" shadow="hover">
                <template #header>
                  <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="course-name teacher-name">👨‍🏫 {{ teacher.name }}</span>
                    <el-button type="primary" size="small" @click.stop="openAdminTeacherEvaluate(teacher)">评价老师</el-button>
                  </div>
                </template>
                <div class="course-info">
                  <p style="font-weight: bold; margin-bottom: 10px;">📚 授课列表：</p>
                  <div class="teacher-courses-list">
                    <div v-for="course in getTeacherCourses(teacher.id)" :key="course.id" class="teacher-course-item" @click="showAdminCourseDetail(course)">
                      <div style="width: 100%;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                          <span class="course-name-small">{{ course.name }}</span>
                          <el-tag size="small" type="info">{{ course.credit }}学分</el-tag>
                        </div>
                        <div v-if="getTeacherCourseRating(teacher.id, course.id)" style="margin-top: 5px; font-size: 12px; color: #909399;">
                          <el-rate :model-value="getTeacherCourseRating(teacher.id, course.id).avg" disabled show-score text-color="#ff9900" style="--el-rate-font-size: 14px;" />
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
        </div>
      </el-card>
    </el-main>

    <el-dialog v-model="showAdminDetailDialog" :title="selectedAdminCourse?.name" width="600px">
      <div v-if="selectedAdminCourse" class="detail-content">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="课程名">{{ selectedAdminCourse.name }}</el-descriptions-item>
          <el-descriptions-item label="学分">{{ selectedAdminCourse.credit }}</el-descriptions-item>
          <el-descriptions-item label="开课学院" v-if="selectedAdminCourse.college">{{ selectedAdminCourse.college }}</el-descriptions-item>
          <el-descriptions-item label="考核方式">{{ selectedAdminCourse.assessment_method || '闭卷笔试' }}</el-descriptions-item>
          <el-descriptions-item label="专业">
            <div v-for="major_id in selectedAdminCourse.major_ids" :key="major_id" style="margin-bottom: 5px;">
              <span>{{ getMajorName(major_id) }}:</span>
              <el-tag size="small" :type="selectedAdminCourse.major_course_types && selectedAdminCourse.major_course_types[major_id] === '必修' ? 'danger' : 'success'">
                {{ selectedAdminCourse.major_course_types && selectedAdminCourse.major_course_types[major_id] || '必修' }}
              </el-tag>
            </div>
          </el-descriptions-item>
          <el-descriptions-item label="授课教师">{{ selectedAdminCourse.teacher_names }}</el-descriptions-item>
          <el-descriptions-item label="课程性质">{{ selectedAdminCourse.course_types ? selectedAdminCourse.course_types.join('、') : (selectedAdminCourse.course_type || '') }}</el-descriptions-item>
          <el-descriptions-item label="开课学期">{{ selectedAdminCourse.semesters ? selectedAdminCourse.semesters.join('、') : '' }}</el-descriptions-item>
          <el-descriptions-item v-if="selectedAdminCourse.major_study_semesters && selectedAdminCourse.major_ids" label="建议修读学期">
            <div v-for="major_id in selectedAdminCourse.major_ids" :key="major_id" style="margin-bottom: 5px;">
              <span v-if="selectedAdminCourse.major_study_semesters[major_id] && selectedAdminCourse.major_study_semesters[major_id].length > 0">
                {{ getMajorName(major_id) }}: {{ selectedAdminCourse.major_study_semesters[major_id].join('、') }}
              </span>
            </div>
          </el-descriptions-item>
          <el-descriptions-item v-if="selectedAdminCourse.teacher_ratings && Object.keys(selectedAdminCourse.teacher_ratings).length > 0" label="教师评分" :span="1">
            <div v-for="(rating, teacherId) in selectedAdminCourse.teacher_ratings" :key="teacherId" style="margin-bottom: 10px;">
              <span>{{ getAdminTeacherName(teacherId) }}: </span>
              <el-rate :model-value="rating" disabled show-score style="width: 120px;" />
              <span style="margin-left: 30px; color: #909399; font-size: 12px;">({{ selectedAdminCourse.teacher_evaluation_counts?.[teacherId] || 0 }}人评价)</span>
            </div>
          </el-descriptions-item>
          <el-descriptions-item v-else label="评分">
            暂无评价
          </el-descriptions-item>
          <el-descriptions-item label="课程概述">{{ selectedAdminCourse.description || '暂无介绍' }}</el-descriptions-item>
        </el-descriptions>
        <h4 style="margin-top: 20px; margin-bottom: 10px;">教师评价</h4>
        <div v-if="adminCourseEvaluations.length > 0">
          <div v-for="item in adminCourseEvaluations" :key="item.id" class="eval-item">
            <div class="eval-header">
              <span class="eval-teacher">{{ item.teacher_name }}</span>
              <el-rate v-model="item.rating" disabled style="width: 120px;" />
            </div>
            <p class="eval-comment">{{ item.comment }}</p>
            <p class="eval-time">{{ item.created_at }}</p>
          </div>
        </div>
        <el-empty v-else description="暂无评价" :image-size="60" />
        <div style="margin-top: 20px;">
          <h4 style="margin-bottom: 10px;">添加评价</h4>
          <el-form :model="adminEvalForm" label-width="80px">
            <el-form-item label="教师">
              <el-select v-model="adminEvalForm.teacher_id" placeholder="请选择教师" :disabled="!selectedAdminCourse">
                <el-option v-for="(teacher_id, index) in selectedAdminCourse?.teacher_ids" :key="teacher_id" :label="selectedAdminCourse.teacher_names.split(',')[index]" :value="teacher_id" />
              </el-select>
            </el-form-item>
            <el-form-item label="评分">
              <el-rate v-model="adminEvalForm.rating" style="width: 150px;" />
            </el-form-item>
            <el-form-item label="评语">
              <el-input v-model="adminEvalForm.comment" type="textarea" :rows="3" placeholder="请输入评语..." />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="addAdminEvaluation">提交评价</el-button>
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
        <el-button type="primary" @click="submitAdminTeacherEval">提交评价</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showAdminFeedbackDialog" title="用户反馈" width="500px">
      <div>
        <h4 style="margin-bottom: 10px;">我的反馈记录</h4>
        <div v-for="fb in myFeedbacks" :key="fb.id" class="feedback-item">
          <p class="feedback-content">{{ fb.content }}</p>
          <div class="feedback-footer">
            <span class="feedback-time">{{ fb.created_at }}</span>
            <el-button type="danger" size="small" @click="deleteAdminFeedback(fb)">删除</el-button>
          </div>
        </div>
        <el-empty v-if="myFeedbacks.length === 0" description="暂无反馈记录" />
      </div>
      <el-input v-model="adminFeedbackContent" type="textarea" :rows="4" placeholder="请输入您的反馈内容..." />
      <template #footer>
        <el-button @click="showAdminFeedbackDialog = false">取消</el-button>
        <el-button type="primary" @click="submitAdminFeedback">提交</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showCourseDialog" title="添加课程" width="500px" @opened="clearForm">
      <el-form :model="courseForm" label-width="80px" autocomplete="off">
        <el-form-item label="课程名">
          <el-input v-model="courseForm.name" placeholder="请输入课程名" autocomplete="off" />
        </el-form-item>
        <el-form-item label="学分">
          <el-input-number v-model="courseForm.credit" :min="0.5" :max="10" :step="0.5" />
        </el-form-item>
        <el-form-item label="开课学院">
          <el-input v-model="courseForm.college" placeholder="请输入开课学院" autocomplete="off" />
        </el-form-item>
        <el-form-item label="考核方式">
          <el-input v-model="courseForm.assessment_method" placeholder="请输入考核方式" autocomplete="off" />
        </el-form-item>
        <el-form-item label="序号">
          <el-input-number v-model="courseForm.order_num" :min="0" />
        </el-form-item>
        <el-form-item label="专业">
          <el-select v-model="courseForm.major_ids" multiple placeholder="请选择专业（可多选）" style="width: 100%;" autocomplete="off">
            <el-option v-for="m in majors" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
          <div v-if="courseForm.major_ids.length > 0" style="margin-top: 10px;">
            <div v-for="major_id in courseForm.major_ids" :key="major_id" style="margin-bottom: 10px; padding: 8px; background: #f5f7fa; border-radius: 4px;">
              <div style="margin-bottom: 5px;">
                <span>{{ getMajorName(major_id) }}：</span>
                <el-select v-model="courseForm.major_course_types[major_id]" placeholder="选择课程性质" style="width: 150px;" autocomplete="off">
                  <el-option label="必修" value="必修" />
                  <el-option label="选修" value="选修" />
                </el-select>
              </div>
              <div>
                <span style="font-size: 12px; color: #909399;">修读学期：</span>
                <el-select v-model="courseForm.major_study_semesters[major_id]" multiple placeholder="选择修读学期" style="width: 100%;" autocomplete="off">
                  <el-option label="大一上" value="大一上" />
                  <el-option label="大一下" value="大一下" />
                  <el-option label="大二上" value="大二上" />
                  <el-option label="大二下" value="大二下" />
                  <el-option label="大三上" value="大三上" />
                  <el-option label="大三下" value="大三下" />
                  <el-option label="大四上" value="大四上" />
                  <el-option label="大四下" value="大四下" />
                </el-select>
              </div>
            </div>
          </div>
        </el-form-item>
        <el-form-item label="教师">
          <el-input v-model="courseForm.teacher_names" placeholder="请输入教师姓名（多个用逗号分隔）" autocomplete="off" />
        </el-form-item>
        <el-form-item label="课程性质">
          <el-select v-model="courseForm.course_types" multiple placeholder="请选择课程性质（可多选）" style="width: 100%;">
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
        <el-form-item v-if="courseForm.course_types.includes('通识选修')" label="主题类别">
          <el-select v-model="courseFormTopicCategory" placeholder="请选择主题类别" style="width: 100%;">
            <el-option label="四史类" value="四史类" />
            <el-option label="创新创业类" value="创新创业类" />
            <el-option label="其他类" value="其他类" />
            <el-option label="艺术审美类" value="艺术审美类" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="courseForm.course_types.includes('实践课')" label="主题类别">
          <el-select v-model="courseFormTopicCategory" multiple placeholder="请选择主题类别（可多选）" style="width: 100%;">
            <el-option label="普通班" value="普通班" />
            <el-option label="卓越工程师" value="卓越工程师" />
          </el-select>
        </el-form-item>
        <el-form-item label="开课学期">
          <el-select v-model="courseForm.semesters" multiple placeholder="请选择开课学期（可多选）" style="width: 100%;">
            <el-option label="秋季" value="秋季" />
            <el-option label="春季" value="春季" />
          </el-select>
        </el-form-item>
        <el-form-item label="概述">
          <el-input v-model="courseForm.description" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCourseDialog = false">取消</el-button>
        <el-button type="primary" @click="addCourse">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showEvalDialog" title="添加评价" width="500px">
      <el-form :model="evalForm" label-width="80px">
        <el-form-item label="课程">
          <el-select v-model="evalForm.course_id" placeholder="请选择课程" @change="updateTeachers">
            <el-option v-for="c in courses" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="教师">
          <el-select v-model="evalForm.teacher_id" placeholder="请选择教师" :disabled="!evalForm.course_id">
            <el-option v-for="t in courseTeachers" :key="t.id" :label="t.name" :value="t.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="星级">
          <el-rate v-model="evalForm.rating" style="width: 200px;" />
        </el-form-item>
        <el-form-item label="评语">
          <el-input v-model="evalForm.comment" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEvalDialog = false">取消</el-button>
        <el-button type="primary" @click="addEvaluation">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showEditEvalDialog" title="编辑评价" width="500px">
      <el-form :model="editEvalForm" label-width="80px">
        <el-form-item label="课程">
          <span>{{ editEvalForm.course_name }}</span>
        </el-form-item>
        <el-form-item label="教师">
          <span>{{ editEvalForm.teacher_name }}</span>
        </el-form-item>
        <el-form-item label="星级">
          <el-rate v-model="editEvalForm.rating" style="width: 200px;" />
        </el-form-item>
        <el-form-item label="评语">
          <el-input v-model="editEvalForm.comment" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditEvalDialog = false">取消</el-button>
        <el-button type="primary" @click="saveEvaluation">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showEditCourseDialog" title="编辑课程" width="500px">
      <el-form :model="editCourseForm" label-width="80px" autocomplete="off">
        <el-form-item label="课程名">
          <el-input v-model="editCourseForm.name" placeholder="请输入课程名" autocomplete="off" />
        </el-form-item>
        <el-form-item label="学分">
          <el-input-number v-model="editCourseForm.credit" :min="0.5" :max="10" :step="0.5" />
        </el-form-item>
        <el-form-item label="开课学院">
          <el-input v-model="editCourseForm.college" placeholder="请输入开课学院" autocomplete="off" />
        </el-form-item>
        <el-form-item label="考核方式">
          <el-input v-model="editCourseForm.assessment_method" placeholder="请输入考核方式" autocomplete="off" />
        </el-form-item>
        <el-form-item label="序号">
          <el-input-number v-model="editCourseForm.order_num" :min="0" />
        </el-form-item>
        <el-form-item label="专业">
          <el-select v-model="editCourseForm.major_ids" multiple placeholder="请选择专业（可多选）" style="width: 100%;" autocomplete="off">
            <el-option v-for="m in majors" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
          <div v-if="editCourseForm.major_ids.length > 0" style="margin-top: 10px;">
            <div v-for="major_id in editCourseForm.major_ids" :key="major_id" style="margin-bottom: 10px; padding: 8px; background: #f5f7fa; border-radius: 4px;">
              <div style="margin-bottom: 5px;">
                <span>{{ getMajorName(major_id) }}：</span>
                <el-select v-model="editCourseForm.major_course_types[major_id]" placeholder="选择课程性质" style="width: 150px;" autocomplete="off">
                  <el-option label="必修" value="必修" />
                  <el-option label="选修" value="选修" />
                </el-select>
              </div>
              <div>
                <span style="font-size: 12px; color: #909399;">修读学期：</span>
                <el-select v-model="editCourseForm.major_study_semesters[major_id]" multiple placeholder="选择修读学期" style="width: 100%;" autocomplete="off">
                  <el-option label="大一上" value="大一上" />
                  <el-option label="大一下" value="大一下" />
                  <el-option label="大二上" value="大二上" />
                  <el-option label="大二下" value="大二下" />
                  <el-option label="大三上" value="大三上" />
                  <el-option label="大三下" value="大三下" />
                  <el-option label="大四上" value="大四上" />
                  <el-option label="大四下" value="大四下" />
                </el-select>
              </div>
            </div>
          </div>
        </el-form-item>
        <el-form-item label="教师">
          <el-input v-model="editCourseForm.teacher_names" placeholder="请输入教师姓名（多个用逗号分隔）" autocomplete="off" />
        </el-form-item>
        <el-form-item label="课程性质">
          <el-select v-model="editCourseForm.course_types" multiple placeholder="请选择课程性质（可多选）" style="width: 100%;">
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
        <el-form-item v-if="editCourseForm.course_types.includes('通识选修')" label="主题类别">
          <el-select v-model="editCourseFormTopicCategory" placeholder="请选择主题类别" style="width: 100%;">
            <el-option label="四史类" value="四史类" />
            <el-option label="创新创业类" value="创新创业类" />
            <el-option label="其他类" value="其他类" />
            <el-option label="艺术审美类" value="艺术审美类" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="editCourseForm.course_types.includes('实践课')" label="主题类别">
          <el-select v-model="editCourseFormTopicCategory" multiple placeholder="请选择主题类别（可多选）" style="width: 100%;">
            <el-option label="普通班" value="普通班" />
            <el-option label="卓越工程师" value="卓越工程师" />
          </el-select>
        </el-form-item>
        <el-form-item label="开课学期">
          <el-select v-model="editCourseForm.semesters" multiple placeholder="请选择开课学期（可多选）" style="width: 100%;">
            <el-option label="秋季" value="秋季" />
            <el-option label="春季" value="春季" />
          </el-select>
        </el-form-item>
        <el-form-item label="概述">
          <el-input v-model="editCourseForm.description" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditCourseDialog = false">取消</el-button>
        <el-button type="primary" @click="saveCourse">保存</el-button>
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
      activeMenu: 'courses',
      majors: [],
      teachers: [],
      courses: [],
      allCourses: [],
      evaluations: [],
      feedbacks: [],
      searchMajor: null,
      searchCollege: null,
      colleges: [],
      majorCourseTypeFilter: null,
      courseTypeFilter: [],
      searchKeyword: '',
      teacherKeyword: '',
      sortOrder: 'asc',
      csCourses: [],
      csAllCourses: [],
      csTeachers: [],
      csSearchMode: 'course',
      csCourseKeyword: '',
      csTeacherKeyword: '',
      csSelectedTeacher: null,
      csCourseTypeFilter: [],
      csSortOrder: 'asc',
      showTeacherEvalDialog: false,
      selectedTeacherForEval: null,
      teacherEvalForm: { course_id: null, rating: 5, comment: '' },
      showCourseDialog: false,
      showEvalDialog: false,
      showEditEvalDialog: false,
      showEditCourseDialog: false,
      courseForm: { name: '', credit: 3.0, college: '', assessment_method: '闭卷笔试', topic_category: '', order_num: 0, major_ids: [], major_course_types: {}, major_study_semesters: {}, teacher_names: '', course_types: [], semesters: [], description: '' },
      editCourseForm: { id: null, name: '', credit: 3.0, college: '', assessment_method: '闭卷笔试', topic_category: '', order_num: 0, major_ids: [], major_course_types: {}, major_study_semesters: {}, teacher_names: '', course_types: [], semesters: [], description: '' },
      evalForm: { course_id: null, teacher_id: null, rating: 5, comment: '' },
      editEvalForm: { id: null, course_id: null, course_name: '', teacher_id: null, teacher_name: '', rating: 5, comment: '' },
      courseTeachers: [],
      evalCourseKeyword: '',
      evalTeacherKeyword: '',
      previewCourses: [],
      previewAllCourses: [],
      previewSelectedMajor: null,
      previewSelectedCollege: null,
      previewColleges: [],
      previewSelectedCourseType: [],
      previewSelectedMajorCourseType: null,
      previewSearchKeyword: '',
      previewTeacherKeyword: '',
      showPreviewDetailDialog: false,
      selectedPreviewCourse: null,
      adminMode: false,
      adminCourses: [],
      adminAllCourses: [],
      mainSearchMode: 'course',
      adminSelectedMajor: null,
      adminSelectedCollege: null,
      adminColleges: [],
      adminSelectedCourseType: [],
      adminSelectedMajorCourseType: null,
      adminSearchKeyword: '',
      adminTeacherKeyword: '',
      showAdminDetailDialog: false,
      selectedAdminCourse: null,
      adminCourseEvaluations: [],
      adminEvalForm: { teacher_id: null, rating: 5, comment: '' },
      showAdminFeedbackDialog: false,
      adminFeedbackContent: '',
      myFeedbacks: [],
      isRefreshing: false,
      selectedCourses: [],
      adminCurrentPage: 1,
      adminPageSize: 12
    }
  },
  async mounted() {
    this.username = localStorage.getItem('username')
    const adminMode = localStorage.getItem('adminMode')
    if (adminMode === 'true') {
      this.adminMode = true
    }
    await this.loadMajors()
    await this.loadTeachers()
    await this.loadCourses()
    await this.loadEvaluations()
    await this.loadAdminCourses()
    await this.loadMyFeedbacks()
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
    isAdmin() {
      const role = localStorage.getItem('role')
      return role === 'admin' || role === 'superadmin'
    },
    isSuperAdmin() {
      return localStorage.getItem('role') === 'superadmin'
    },
    courseFormTopicCategory: {
      get() {
        if (this.courseForm.course_types.includes('实践课')) {
          return this.courseForm.topic_category ? this.courseForm.topic_category.split(',') : []
        }
        return this.courseForm.topic_category
      },
      set(val) {
        if (Array.isArray(val)) {
          this.courseForm.topic_category = val.join(',')
        } else {
          this.courseForm.topic_category = val
        }
      }
    },
    editCourseFormTopicCategory: {
      get() {
        if (this.editCourseForm.course_types.includes('实践课')) {
          return this.editCourseForm.topic_category ? this.editCourseForm.topic_category.split(',') : []
        }
        return this.editCourseForm.topic_category
      },
      set(val) {
        if (Array.isArray(val)) {
          this.editCourseForm.topic_category = val.join(',')
        } else {
          this.editCourseForm.topic_category = val
        }
      }
    },
    filteredEvaluations() {
      let filtered = this.evaluations || []
      if (this.evalCourseKeyword) {
        const keyword = this.evalCourseKeyword.toLowerCase()
        filtered = filtered.filter(e => e.course_name && e.course_name.toLowerCase().includes(keyword))
      }
      if (this.evalTeacherKeyword) {
        const keyword = this.evalTeacherKeyword.toLowerCase()
        filtered = filtered.filter(e => {
          if (e.teacher_name) {
            const nameMatch = e.teacher_name.toLowerCase().includes(keyword)
            const pinyinMatch = e.teacher_pinyin && e.teacher_pinyin.toLowerCase().includes(keyword)
            return nameMatch || pinyinMatch
          }
          return false
        })
      }
      return filtered
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
    paginatedAdminCourses() {
      const start = (this.adminCurrentPage - 1) * this.adminPageSize
      return this.adminCourses.slice(start, start + this.adminPageSize)
    }
  },
  methods: {
    handleAdminPageChange() {
      // 分页变化时滚动到顶部
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },
    async handleRefresh() {
      if (this.isRefreshing) return
      this.isRefreshing = true
      await this.loadMajors()
      await this.loadTeachers()
      await this.loadCourses()
      await this.loadEvaluations()
      setTimeout(() => {
        this.isRefreshing = false
        ElMessage.success('刷新成功')
      }, 500)
    },
    handleCourseSelectionChange(val) {
      this.selectedCourses = val
    },
    async batchDeleteCourses() {
      if (this.selectedCourses.length === 0) return
      
      const courseIds = this.selectedCourses.map(course => course.id)
      
      try {
        await ElMessageBox.confirm(
          `确定要删除选中的 ${this.selectedCourses.length} 门课程吗？此操作不可恢复。`,
          '警告',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        for (const courseId of courseIds) {
          await request.delete(`/courses/${courseId}`)
        }
        
        ElMessage.success(`成功删除 ${this.selectedCourses.length} 门课程`)
        clearCache('/courses')
        await this.loadCourses()
        this.selectedCourses = []
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量删除失败')
        }
      }
    },
    goToUserCenter() {
      this.$router.push('/user-center')
    },
    handleMenuSelect(index) {
      if (index === 'users') {
        this.$router.push('/user-management')
      } else if (index === 'feedback') {
        this.activeMenu = index
        this.loadFeedbacks()
      } else if (index === 'preview') {
        this.activeMenu = index
        this.loadPreviewCourses()
      } else {
        this.activeMenu = index
      }
    },
    async loadMajors() {
      this.majors = await request.get('/majors')
    },
    async loadTeachers() {
      this.teachers = await request.get('/teachers')
    },
    async loadCourses() {
      const params = { sort: this.sortOrder, sort_by: 'order_num' }
      if (this.searchMajor) {
        params.major_id = this.searchMajor
      }
      this.allCourses = await request.get('/courses', { params })
      this.updateColleges()
      this.filterCourses()
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
    openAdminTeacherEvaluate(teacher) {
      this.selectedTeacherForEval = teacher
      this.teacherEvalForm = { course_id: null, rating: 5, comment: '' }
      this.showTeacherEvalDialog = true
    },
    async submitAdminTeacherEval() {
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
    async loadFeedbacks() {
      this.feedbacks = await request.get('/feedbacks')
    },
    filterCourses() {
      let filtered = this.allCourses || []
      if (this.searchCollege) {
        filtered = filtered.filter(c => c.college === this.searchCollege)
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
      if (this.searchMajor && this.majorCourseTypeFilter) {
        filtered = filtered.filter(c => {
          const type = c.major_course_types && c.major_course_types[this.searchMajor]
          return type === this.majorCourseTypeFilter
        })
      }
      if (this.courseTypeFilter && this.courseTypeFilter.length > 0) {
        filtered = filtered.filter(c => {
          if (!c.course_types || c.course_types.length === 0) return false
          return this.courseTypeFilter.some(t => c.course_types.includes(t))
        })
      }
      this.courses = filtered
    },
    async loadEvaluations() {
      this.evaluations = await request.get('/evaluations')
    },
    clearForm() {
      this.$nextTick(() => {
        this.courseForm = { name: '', credit: 3.0, college: '', assessment_method: '闭卷笔试', topic_category: '', order_num: 0, major_ids: [], major_course_types: {}, major_study_semesters: {}, teacher_names: '', course_types: [], semesters: [], description: '' }
      })
    },
    openCourseDialog() {
      this.courseForm = { name: '', credit: 3.0, college: '', assessment_method: '闭卷笔试', topic_category: '', order_num: 0, major_ids: [], major_course_types: {}, major_study_semesters: {}, teacher_names: '', course_types: [], semesters: [], description: '' }
      this.showCourseDialog = true
    },
    async addCourse() {
      if (!this.courseForm.name || this.courseForm.major_ids.length === 0 || !this.courseForm.teacher_names || this.courseForm.course_types.length === 0 || this.courseForm.semesters.length === 0) {
        ElMessage.warning('请填写完整信息')
        return
      }
      try {
        await request.post('/courses', this.courseForm)
        ElMessage.success('添加成功')
        clearCache('/courses')
        this.showCourseDialog = false
        this.courseForm = { name: '', credit: 3.0, college: '', assessment_method: '闭卷笔试', topic_category: '', order_num: 0, major_ids: [], major_course_types: {}, major_study_semesters: {}, teacher_names: '', course_types: [], semesters: [], description: '' }
        await this.loadTeachers()
        await this.loadCourses()
      } catch (error) {
        ElMessage.error('添加失败: ' + (error.response?.data?.msg || error.message))
      }
    },
    async deleteCourse(id) {
      try {
        await ElMessageBox.confirm('确定要删除这门课程吗？', '提示', {
          type: 'warning',
          confirmButtonText: '确定',
          cancelButtonText: '取消'
        })
        await request.delete(`/courses/${id}`)
        ElMessage.success('删除成功')
        await this.loadCourses()
      } catch {
      }
    },
    editCourse(course) {
      this.editCourseForm = {
        id: course.id,
        name: course.name,
        credit: course.credit,
        college: course.college || '',
        assessment_method: course.assessment_method || '闭卷笔试',
        topic_category: course.topic_category || '',
        order_num: course.order_num || 0,
        major_ids: course.major_ids || [],
        major_course_types: course.major_course_types || {},
        major_study_semesters: course.major_study_semesters || {},
        teacher_names: course.teacher_names || '',
        course_types: course.course_types || (course.course_type ? [course.course_type] : []),
        semesters: course.semesters || [],
        description: course.description || ''
      }
      this.showEditCourseDialog = true
    },
    async saveCourse() {
      if (!this.editCourseForm.name || this.editCourseForm.major_ids.length === 0 || !this.editCourseForm.teacher_names || this.editCourseForm.course_types.length === 0 || this.editCourseForm.semesters.length === 0) {
        ElMessage.warning('请填写完整信息')
        return
      }
      try {
        await request.put(`/courses/${this.editCourseForm.id}`, this.editCourseForm)
        ElMessage.success('更新成功')
        clearCache('/courses')
        this.showEditCourseDialog = false
        await this.loadTeachers()
        await this.loadCourses()
      } catch (error) {
        ElMessage.error('更新失败: ' + (error.response?.data?.msg || error.message))
      }
    },
    getTeacherName(row, teacherId) {
      // 查找教师姓名
      if (!row.teacher_ids || !row.teacher_names) {
        return '未知教师'
      }
      const teacherIndex = row.teacher_ids.findIndex(id => id == teacherId)
      if (teacherIndex !== -1) {
        const teacherNames = row.teacher_names.split(',')
        return teacherNames[teacherIndex] || '未知教师'
      }
      return '未知教师'
    },
    getMajorName(majorId) {
      // 查找专业名称
      const major = this.majors.find(m => m.id === Number(majorId))
      return major ? major.name : '未知专业'
    },
    updateTeachers(courseId) {
      const course = this.courses.find(c => c.id === courseId)
      if (course) {
        this.courseTeachers = course.teacher_ids.map((id, index) => ({
          id: id,
          name: course.teacher_names.split(',')[index]
        }))
        this.evalForm.teacher_id = null
      } else {
        this.courseTeachers = []
        this.evalForm.teacher_id = null
      }
    },
    async addEvaluation() {
      if (!this.evalForm.course_id || !this.evalForm.teacher_id || !this.evalForm.rating) {
        ElMessage.warning('请填写完整信息')
        return
      }
      await request.post('/evaluations', this.evalForm)
      ElMessage.success('添加成功')
      this.showEvalDialog = false
      this.evalForm = { course_id: null, teacher_id: null, rating: 5, comment: '' }
      this.courseTeachers = []
      await this.loadEvaluations()
      await this.loadCourses()
    },
    editEvaluation(evaluation) {
      this.editEvalForm = {
        id: evaluation.id,
        course_id: evaluation.course_id,
        course_name: evaluation.course_name,
        teacher_id: evaluation.teacher_id,
        teacher_name: evaluation.teacher_name,
        rating: evaluation.rating,
        comment: evaluation.comment
      }
      this.showEditEvalDialog = true
    },
    async saveEvaluation() {
      await request.put(`/evaluations/${this.editEvalForm.id}`, {
        rating: this.editEvalForm.rating,
        comment: this.editEvalForm.comment
      })
      ElMessage.success('更新成功')
      this.showEditEvalDialog = false
      await this.loadEvaluations()
      await this.loadCourses()
    },
    async deleteEvaluation(id) {
      try {
        await ElMessageBox.confirm('确定要删除这条评价吗？', '提示', {
          type: 'warning',
          confirmButtonText: '确定',
          cancelButtonText: '取消'
        })
        await request.delete(`/evaluations/${id}`)
        ElMessage.success('删除成功')
        await this.loadEvaluations()
        await this.loadCourses()
      } catch {
      }
    },
    async clearCourses() {
      try {
        await ElMessageBox.confirm('确定要清空所有课程吗？此操作不可恢复！', '警告', {
          type: 'danger',
          confirmButtonText: '确定',
          cancelButtonText: '取消'
        })
        await request.delete('/courses/clear')
        ElMessage.success('所有课程已清空')
        await this.loadCourses()
        await this.loadEvaluations()
      } catch {
      }
    },
    async clearEvaluations() {
      try {
        await ElMessageBox.confirm('确定要清空所有评价吗？此操作不可恢复！', '警告', {
          type: 'danger',
          confirmButtonText: '确定',
          cancelButtonText: '取消'
        })
        await request.delete('/evaluations/clear')
        ElMessage.success('所有评价已清空')
        await this.loadEvaluations()
        await this.loadCourses()
      } catch {
      }
    },
    async clearAllData() {
      try {
        const confirmed = confirm('确定要清空所有数据吗？这将删除所有课程、教师、专业和评价！此操作不可恢复！')
        if (!confirmed) {
          return
        }
        console.log('开始清空所有数据...')
        await request.delete('/clear-all')
        ElMessage.success('所有数据已清空！')
        await this.loadMajors()
        await this.loadTeachers()
        await this.loadCourses()
        await this.loadEvaluations()
      } catch (error) {
        console.error('清空数据失败:', error)
        ElMessage.error('清空失败: ' + (error.message || '未知错误'))
      }
    },
    async handleDeleteFeedback(row) {
      try {
        await ElMessageBox.confirm('确定要删除这条反馈吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        await request.delete(`/feedbacks/${row.id}`)
        ElMessage.success('删除成功')
        await this.loadFeedbacks()
      } catch {
      }
    },
    async loadPreviewCourses() {
      const params = { sort: 'asc', sort_by: 'order_num' }
      if (this.previewSelectedMajor) {
        params.major_id = this.previewSelectedMajor
      }
      if (this.previewSelectedCourseType && this.previewSelectedCourseType.length > 0) {
        params.course_type = this.previewSelectedCourseType.join(',')
      }
      if (this.previewSelectedMajor && this.previewSelectedMajorCourseType) {
        params.major_course_type = this.previewSelectedMajorCourseType
      }
      this.previewAllCourses = await request.get('/courses', { params })
      this.updatePreviewColleges()
      this.filterPreviewCourses()
    },
    updatePreviewColleges() {
      const collegeSet = new Set()
      if (this.previewAllCourses) {
        this.previewAllCourses.forEach(course => {
          if (course.college) {
            collegeSet.add(course.college)
          }
        })
      }
      this.previewColleges = Array.from(collegeSet).sort()
    },
    onPreviewMajorChange() {
      this.previewSelectedMajorCourseType = null
      this.loadPreviewCourses()
    },
    filterPreviewCourses() {
      let filtered = this.previewAllCourses || []
      if (this.previewSelectedCollege) {
        filtered = filtered.filter(c => c.college === this.previewSelectedCollege)
      }
      if (this.previewSearchKeyword) {
        const keyword = this.previewSearchKeyword.toLowerCase()
        filtered = filtered.filter(c => c.name.toLowerCase().includes(keyword))
      }
      if (this.previewTeacherKeyword) {
        const keyword = this.previewTeacherKeyword.toLowerCase()
        filtered = filtered.filter(c => {
          if (c.teacher_names) {
            const nameMatch = c.teacher_names.toLowerCase().includes(keyword)
            const pinyinMatch = c.teacher_pinyins && c.teacher_pinyins.toLowerCase().includes(keyword)
            return nameMatch || pinyinMatch
          }
          return false
        })
      }
      this.previewCourses = filtered
    },
    getPreviewTeacherName(teacherId) {
      const teacher = this.teachers.find(t => t.id === Number(teacherId))
      return teacher ? teacher.name : '未知教师'
    },
    showPreviewDetail(course) {
      this.selectedPreviewCourse = course
      this.showPreviewDetailDialog = true
    },
    toggleAdminMode() {
      this.adminMode = !this.adminMode
    },
    async loadAdminCourses() {
      const params = { sort: 'asc', sort_by: 'order_num' }
      if (this.adminSelectedMajor) {
        params.major_id = this.adminSelectedMajor
      }
      if (this.adminSelectedCourseType && this.adminSelectedCourseType.length > 0) {
        params.course_type = this.adminSelectedCourseType.join(',')
      }
      if (this.adminSelectedMajor && this.adminSelectedMajorCourseType) {
        params.major_course_type = this.adminSelectedMajorCourseType
      }
      this.adminAllCourses = await request.get('/courses', { params })
      this.updateAdminColleges()
      this.filterAdminCourses()
    },
    updateAdminColleges() {
      const collegeSet = new Set()
      if (this.adminAllCourses) {
        this.adminAllCourses.forEach(course => {
          if (course.college) {
            collegeSet.add(course.college)
          }
        })
      }
      this.adminColleges = Array.from(collegeSet).sort()
    },
    onAdminMajorChange() {
      this.adminSelectedMajorCourseType = null
      this.loadAdminCourses()
    },
    handleMainTabChange(tab) {
      if (tab === 'cs_course') {
        this.loadCsCourses()
      }
    },
    filterAdminCourses() {
      let filtered = this.adminAllCourses || []
      if (this.adminSelectedCollege) {
        filtered = filtered.filter(c => c.college === this.adminSelectedCollege)
      }
      if (this.adminSearchKeyword) {
        const keyword = this.adminSearchKeyword.toLowerCase()
        filtered = filtered.filter(c => c.name.toLowerCase().includes(keyword))
      }
      if (this.adminTeacherKeyword) {
        const keyword = this.adminTeacherKeyword.toLowerCase()
        filtered = filtered.filter(c => {
          if (c.teacher_names) {
            return c.teacher_names.toLowerCase().includes(keyword)
          }
          return false
        })
      }
      this.adminCourses = filtered
      this.adminCurrentPage = 1
    },
    async showAdminCourseDetail(course) {
      this.selectedAdminCourse = course
      this.showAdminDetailDialog = true
      this.adminCourseEvaluations = await request.get('/evaluations', { params: { course_id: course.id } })
      this.adminEvalForm = { teacher_id: null, rating: 5, comment: '' }
    },
    async addAdminEvaluation() {
      if (!this.adminEvalForm.teacher_id || !this.selectedAdminCourse) {
        ElMessage.warning('请选择教师')
        return
      }
      try {
        await request.post('/evaluations', {
          course_id: this.selectedAdminCourse.id,
          teacher_id: this.adminEvalForm.teacher_id,
          rating: this.adminEvalForm.rating,
          comment: this.adminEvalForm.comment
        })
        ElMessage.success('评价提交成功')
        this.adminEvalForm = { teacher_id: null, rating: 5, comment: '' }
        this.adminCourseEvaluations = await request.get('/evaluations', { params: { course_id: this.selectedAdminCourse.id } })
        await this.loadAdminCourses()
      } catch (e) {
        ElMessage.error(e.response?.data?.msg || '提交失败')
      }
    },
    getAdminTeacherName(teacherId) {
      const teacher = this.teachers.find(t => t.id === Number(teacherId))
      return teacher ? teacher.name : '未知教师'
    },
    async loadMyFeedbacks() {
      this.myFeedbacks = await request.get('/feedbacks')
    },
    openFeedback() {
      this.showAdminFeedbackDialog = true
    },
    openSimulatedSelection() {
      this.$router.push('/simulated-selection')
    },
    async submitAdminFeedback() {
      if (!this.adminFeedbackContent.trim()) {
        ElMessage.warning('反馈内容不能为空')
        return
      }
      try {
        await request.post('/feedbacks', { content: this.adminFeedbackContent })
        ElMessage.success('反馈提交成功')
        this.adminFeedbackContent = ''
        this.myFeedbacks = await request.get('/feedbacks')
      } catch (error) {
        ElMessage.error('提交失败: ' + (error.message || '未知错误'))
      }
    },
    async deleteAdminFeedback(fb) {
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
  background: transparent !important;
}

.main .el-card {
  background: rgba(255, 255, 255, 0.75) !important;
  box-shadow:
    0 8px 32px rgba(31, 38, 135, 0.08),
    inset 0 1px 2px rgba(255, 255, 255, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  border-radius: 16px !important;
}

.el-aside {
  background: rgba(255, 255, 255, 0.75) !important;
  box-shadow:
    0 8px 32px rgba(31, 38, 135, 0.1),
    inset 0 1px 2px rgba(255, 255, 255, 0.5) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  border-radius: 16px !important;
  margin: 80px 10px 20px 20px !important;
  position: sticky !important;
  top: 100px !important;
  height: calc(100vh - 120px) !important;
  overflow-y: auto !important;
}

.el-aside .el-menu {
  background: transparent !important;
  border-right: none !important;
}

.el-aside .el-menu-item {
  border-radius: 12px !important;
  margin: 4px 8px !important;
  transition: all 0.2s ease !important;
}

.el-aside .el-menu-item:hover {
  background: rgba(0, 136, 255, 0.08) !important;
  color: #0088ff !important;
}

.el-aside .el-menu-item.is-active {
  background: linear-gradient(135deg, rgba(0, 145, 255, 0.15), rgba(30, 110, 244, 0.15)) !important;
  color: #0088ff !important;
  font-weight: 500 !important;
}

.el-main {
  background: transparent;
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header-tabs {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 苹果风格分段控制器 - 液态玻璃效果 */
.card-header :deep(.el-tabs) {
  display: inline-flex;
  justify-content: center;
  background: rgba(0, 0, 0, 0.06);
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

.table-actions {
  display: flex;
  flex-direction: column;
  gap: 6px;
  align-items: stretch;
}

.table-actions .el-button {
  width: 100%;
  margin: 0 !important;
}

/* 表格行 hover 效果 */
:deep(.el-table__body tr:hover td) {
  background-color: rgba(0, 136, 255, 0.04) !important;
}

/* 表格斑马纹 */
:deep(.el-table__body tr.el-table__row--striped td) {
  background-color: rgba(0, 0, 0, 0.02) !important;
}

.course-tags {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.search-form {
  margin-bottom: 20px;
}

.preview-course-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.2s;
}

.preview-course-card:hover {
  transform: translateY(-4px);
}

.preview-card-header {
  padding: 12px 16px 8px;
  border-bottom: 1px solid #ebeef5;
}

.preview-course-name {
  font-weight: bold;
  font-size: 16px;
  color: #303133;
}

.preview-card-tags {
  padding: 8px 16px;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.preview-card-body {
  padding: 8px 16px 16px;
}

.preview-card-body p {
  margin: 6px 0;
  font-size: 13px;
  color: #606266;
  line-height: 1.5;
}

.preview-ratings {
  margin-top: 8px;
}

.preview-rating-item {
  display: flex;
  align-items: center;
  margin-bottom: 4px;
}

.preview-course-desc {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  white-space: normal;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px dashed #ebeef5;
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

.feedback-item {
  padding: 10px 0;
  border-bottom: 1px solid #ebeef5;
}

.feedback-item:last-child {
  border-bottom: none;
}

.feedback-content {
  margin: 0 0 8px;
  font-size: 14px;
}

.feedback-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.feedback-time {
  font-size: 12px;
  color: #909399;
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
  background: rgba(255, 255, 255, 0.7);
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

.user-info .el-button {
  font-size: 12px;
  padding: 15px 20px;
  border-radius: 20px !important;
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.06),
    inset 0 1px 2px rgba(255, 255, 255, 0.3) !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
}

/* 小按钮样式 */
:deep(.el-button--small) {
  padding: 15px 20px !important;
  font-size: 14px !important;
  border-radius: 20px !important;
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.06),
    inset 0 1px 2px rgba(255, 255, 255, 0.3) !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
}

/* 紫色按钮样式 */
:deep(.purple-btn) {
  background: rgba(203, 48, 224, 0.78) !important;
  border-color: rgba(203, 48, 224, 0.78) !important;
}

:deep(.purple-btn:hover:not(:disabled)) {
  background: rgba(203, 48, 224, 0.91) !important;
  border-color: rgba(203, 48, 224, 0.91) !important;
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
    font-size: 16px;
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
    flex-direction: column;
  }
  
  .el-aside {
    width: 100% !important;
    max-width: 100%;
    padding: 10px;
  }
  
  .el-menu {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    background: transparent !important;
  }
  
  .el-menu-item {
    flex: 1 1 auto;
    min-width: 80px;
    text-align: center;
    background: #545c64;
    border-radius: 6px;
    margin: 0 !important;
  }
  
  .el-main {
    padding: 10px;
  }
  
  .card-header {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }
  
  .card-header > div {
    display: flex;
    gap: 8px;
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
  
  .course-actions {
    flex-direction: column;
    gap: 8px;
    align-items: stretch;
  }
  
  .course-actions .el-button {
    font-size: 20px;
    padding: 15px 20px;
    width: 100%;
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
    align-items: stretch;
  }
  
  .teacher-actions .el-button {
    font-size: 20px;
    padding: 15px 20px;
    width: 100%;
  }
  
  .evaluation-item {
    padding: 15px;
  }
  
  .evaluation-content {
    font-size: 14px;
  }
  
  .feedback-item {
    padding: 15px;
  }
  
  .feedback-content {
    font-size: 14px;
  }
  
  .user-item {
    padding: 15px;
  }
  
  .user-info-detail {
    font-size: 14px;
  }
  
  .glass-btn {
    font-size: 12px;
    padding: 10px 20px;
    border-radius: 20px;
  }
}
</style>
