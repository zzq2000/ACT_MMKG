<template>
  <div :class="className" :style="{height:height,width:width}" :data="data" />
</template>

<script>

const animationDuration = 2000

export default {
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '300px'
    },
    data: {
      type: Object,
      default: () => {
        return {}
      }
    }
  },
  data() {
    return {
      chart: null
    }
  },
  watch: {
    data(newVal, oldVal) {
      this.updateChart()
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    updateChart() {
      this.chart.setOption({
        title: {
          text: '节点类型数量统计',
          top: 'top',
          left: 'left'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: { // 坐标轴指示器，坐标轴触发有效
            type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        grid: {
          top: 45,
          left: '2%',
          right: '2%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [{
          type: 'category',
          data: this.data.xData,
          axisLabel: {
            interval: 0,
            fontSize: 16
          },
          axisTick: {
            alignWithLabel: true
          }
        }],
        yAxis: [{
          type: 'value',
          axisTick: {
            show: false
          }
        }],
        series: [{
          name: '个数',
          type: 'bar',
          stack: 'vistors',
          barWidth: '60%',
          data: this.data.yData,
          animationDuration
        }]
      })
    },
    initChart() {
      this.chart = this.$echarts.init(this.$el)
      this.updateChart()
    }
  }
}
</script>
