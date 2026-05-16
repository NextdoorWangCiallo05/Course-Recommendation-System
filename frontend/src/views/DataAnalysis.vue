<template>
  <div class="data-analysis">
    <div class="header">
      <div class="header-left">
        <img src="/images/logo.png" class="logo" alt="logo">
        <h2>选课推荐系统 - 数据分析</h2>
      </div>
      <div class="header-right">
        <n-text depth="3" class="welcome-text">欢迎, {{ username }}</n-text>
        <n-button type="primary" size="small" @click="goBack">{{ backText }}</n-button>
      </div>
    </div>
    <div class="main">
      <div class="charts-grid">
        <n-card class="chart-card chart-card-tall" title="教师评分排行">
          <div class="chart-wrapper-scroll">
            <div class="chart-inner" :style="{ height: teacherChartHeight + 'px' }">
              <v-chart :option="teacherRatingOption" autoresize />
            </div>
          </div>
        </n-card>
        <n-card class="chart-card" title="课程性质分布">
          <div class="chart-wrapper">
            <v-chart :option="courseTypeOption" autoresize />
          </div>
        </n-card>
        <n-card class="chart-card" title="各专业课程数量">
          <div class="chart-wrapper">
            <v-chart :option="majorCourseOption" autoresize />
          </div>
        </n-card>
        <n-card class="chart-card chart-card-wide" title="学分统计">
          <div class="credit-summary">
            <div class="credit-chart">
              <v-chart :option="creditOption" autoresize style="height: 260px" />
            </div>
            <div class="credit-table">
              <n-data-table :columns="creditColumns" :data="creditByType" size="small" :bordered="false" :single-line="false" />
            </div>
          </div>
        </n-card>
      </div>
    </div>
  </div>
</template>

<script>
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, PieChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import VChart from 'vue-echarts'
import { defineComponent, h } from 'vue'
import { useMessage } from 'naive-ui'
import request from '@/api'

use([CanvasRenderer, BarChart, PieChart, GridComponent, TooltipComponent, LegendComponent])

export default defineComponent({
  name: 'DataAnalysis',
  components: { VChart },
  setup() {
    const message = useMessage()
    return { message }
  },
  data() {
    return {
      username: localStorage.getItem('username') || '',
      role: localStorage.getItem('role') || '',
      teacherRatings: [],
      courseTypes: [],
      majorCourses: [],
      creditSummary: null
    }
  },
  computed: {
    backText() {
      return this.role === 'student' ? '返回主页' : '返回管理面板'
    },
    ratedTeachers() {
      return this.teacherRatings.filter(t => t.eval_count > 0).sort((a, b) => b.avg_rating - a.avg_rating)
    },
    teacherChartHeight() {
      return Math.max(350, this.ratedTeachers.length * 32 + 60)
    },
    creditByType() {
      return this.creditSummary?.type_credits || []
    },
    creditColumns() {
      return [
        { title: '课程性质', key: 'type' },
        { title: '门数', key: 'course_count', width: 80 },
        {
          title: '总学分',
          key: 'total_credits',
          width: 100,
          render: (row) => h('span', { style: 'color:#2080F0;font-weight:600' }, row.total_credits)
        }
      ]
    },
    teacherRatingOption() {
      const data = this.ratedTeachers.map(t => ({
        value: t.avg_rating,
        itemStyle: {
          color: {
            type: 'linear', x: 0, y: 0, x2: 1, y2: 0,
            colorStops: [
              { offset: 0, color: '#0091FF' },
              { offset: 1, color: '#1E6EF4' }
            ]
          }
        }
      })).reverse()
      return {
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' },
          formatter: (params) => {
            const p = params[0]
            const idx = this.ratedTeachers.length - 1 - p.dataIndex
            const t = this.ratedTeachers[idx]
            return `${t.name}<br/>评分: ${t.avg_rating} 分<br/>评价数: ${t.eval_count} 条`
          }
        },
        grid: { left: '3%', right: '12%', bottom: '10%', top: '3%', containLabel: true },
        xAxis: { type: 'value', max: 5, axisLabel: { formatter: '{value}' } },
        yAxis: { type: 'category', data: this.ratedTeachers.map(t => t.name).reverse(), axisLabel: { fontSize: 11 } },
        series: [{
          type: 'bar',
          data,
          barWidth: 20,
          label: { show: true, position: 'right', formatter: (p) => `${p.value}分` },
          markLine: { data: [{ type: 'average', name: '平均' }], label: { formatter: '平均 {c}' } }
        }]
      }
    },
    courseTypeOption() {
      const colors = ['#0091FF', '#36CBCB', '#F7B731', '#FF6B6B', '#A55EEA', '#2ED573']
      return {
        tooltip: { trigger: 'item', formatter: '{b}: {c}门 ({d}%)' },
        series: [{
          type: 'pie',
          radius: ['40%', '70%'],
          center: ['50%', '50%'],
          label: { formatter: '{b}\n{d}%', fontSize: 11 },
          data: this.courseTypes.map((t, i) => ({
            name: t.type, value: t.count,
            itemStyle: { color: colors[i % colors.length] }
          })),
          emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)' } }
        }]
      }
    },
    majorCourseOption() {
      return {
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        grid: { left: '3%', right: '4%', bottom: '3%', top: '5%', containLabel: true },
        xAxis: { type: 'category', data: this.majorCourses.map(m => m.major), axisLabel: { rotate: 30, fontSize: 11 } },
        yAxis: { type: 'value' },
        series: [{
          type: 'bar',
          data: this.majorCourses.map(m => ({
            value: m.count,
            itemStyle: {
              color: {
                type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [
                  { offset: 0, color: '#36CBCB' },
                  { offset: 1, color: '#0091FF' }
                ]
              }
            }
          })),
          barWidth: 30,
          label: { show: true, position: 'top' }
        }]
      }
    },
    creditOption() {
      const majors = this.creditSummary?.major_credits || []
      const colors = ['#0091FF', '#36CBCB', '#F7B731', '#FF6B6B', '#A55EEA']
      return {
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, formatter: (params) => {
          const p = params[0]
          return `${p.name}<br/>总学分: ${p.value} 分`
        }},
        grid: { left: '3%', right: '4%', bottom: '8%', top: '3%', containLabel: true },
        xAxis: { type: 'category', data: majors.map(m => m.major), axisLabel: { rotate: 25, fontSize: 11 } },
        yAxis: { type: 'value', name: '学分' },
        series: [{
          type: 'bar',
          data: majors.map((m, i) => ({
            value: m.total_credits,
            itemStyle: { color: colors[i % colors.length] }
          })),
          barWidth: 28,
          label: { show: true, position: 'top', formatter: (p) => `${p.value}分` }
        }]
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      try {
        const [ratings, types, majors, credits] = await Promise.all([
          request.get('/stats/teacher-ratings'),
          request.get('/stats/course-types'),
          request.get('/stats/major-courses'),
          request.get('/stats/credit-summary')
        ])
        this.teacherRatings = ratings
        this.courseTypes = types
        this.majorCourses = majors
        this.creditSummary = credits
      } catch (e) {
        this.message.error('获取数据失败')
      }
    },
    goBack() {
      this.$router.push(this.role === 'student' ? '/student' : '/admin')
    }
  }
})
</script>

<style scoped>
.data-analysis {
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
  gap: 15px;
}
.welcome-text {
  font-size: 14px;
}
.main {
  padding: 24px;
  min-height: calc(100vh - 64px);
}
.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  max-width: 1400px;
  margin: 0 auto;
}
@media (max-width: 900px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}
.chart-card-tall {
  grid-row: span 2;
}
.chart-wrapper {
  height: 350px;
  width: 100%;
}
.chart-wrapper-scroll {
  width: 100%;
  max-height: 720px;
  overflow-y: auto;
}
.chart-wrapper-scroll::-webkit-scrollbar {
  width: 6px;
}
.chart-wrapper-scroll::-webkit-scrollbar-thumb {
  background: rgba(0, 145, 255, 0.3);
  border-radius: 3px;
}
.chart-inner {
  width: 100%;
}
.chart-card-wide {
  grid-column: span 2;
}
.credit-summary {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}
.credit-chart {
  flex: 1;
  min-width: 0;
}
.credit-table {
  width: 320px;
  flex-shrink: 0;
}
@media (max-width: 900px) {
  .credit-summary {
    flex-direction: column;
  }
  .credit-table {
    width: 100%;
  }
  .chart-card-wide {
    grid-column: span 1;
  }
}
html.dark-mode .header {
  background: rgba(25, 25, 45, 0.85);
}
html.dark-mode .header h2 {
  color: #e8e8e8;
}
</style>
