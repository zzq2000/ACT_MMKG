<template>
  <div :class="className" :style="{height:height,width:width}" :data="data" />
</template>

<script>
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
      type: Array,
      default: () => {
        return []
      }
    }
  },
  data() {
    return {
      chart: null
    }
  },
  watch: {
    data(oldVal, newVal) {
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
          text: '关系类型数量分布',
          top: 'top',
          left: 'left'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{b} : {c} ({d}%)'
        },
        // legend: {
        //   left: 'center',
        //   bottom: '10',
        //   data: ['设备', '缺陷', '图片', '危害', '成因', '措施', '设备型号', '状态量', '缺陷分类', '分类依据', '判断依据']
        // },
        series: [
          {
            name: '关系类型数量',
            type: 'pie',
            roseType: 'radius',
            radius: [15, 95],
            center: ['50%', '60%'],
            data: this.data,
            animationEasing: 'cubicInOut',
            animationDuration: 2000
          }
        ]
      })
    },
    initChart() {
      this.chart = this.$echarts.init(this.$el, 'macarons')
      this.updateChart
    }
  }
}
</script>
