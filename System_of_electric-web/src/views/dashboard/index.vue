<template>
  <div style="margin:8px">
    <el-row class="home" :gutter="10" style="margin-bottom:4px">
      <el-col :span="16">
        <el-card shadow="hover" style="height:650px">
          <el-row class="title" style="height:0px;z-index:100">
            <!-- <el-col :span="12">
              <h3>多模态电力设备缺陷知识图谱</h3>
            </el-col> -->
            <el-col :span="24" style="text-align:right">
              <el-select v-model="graph_id" placeholder="图谱切换" style="width:28%">
                <el-option label="多模态电力设备缺陷知识图谱1" value="0" />
                <el-option label="多模态电力设备缺陷知识图谱2" value="1" />
                <el-option label="多模态电力设备缺陷知识图谱3" value="2" />
                <el-option label="多模态电力设备缺陷知识图谱4" value="3" />
              </el-select>
            </el-col>
          </el-row>
          <el-row style="height:650px">
            <div ref="graph" style="height:650px" />
          </el-row>
        </el-card>
      </el-col>
      <el-col :span="8">
        <div>
          <el-card shadow="hover" style="height:320px">
            <bar-chart :data="barChartData" />
          </el-card>
        </div>
        <div style="margin-top:10px">
          <el-card shadow="hover" style="height:320px">
            <pie-chart :data="pieChartData" />
          </el-card>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import BarChart from './components/BarChart.vue'
import PieChart from './components/PieChart.vue'
import { get_graph } from '../../api/graph'
export default {
  name: 'Index',
  components: { PieChart, BarChart },
  data() {
    return {
      graph_id: '0',
      myChart: {},
      time: 0,
      nodes: [],
      links: [],
      barChartData: {},
      pieChartData: []
    }
  },
  watch: {
    graph_id(newVal, oldVal) {
      // 检测graph_id，并根据其数据更新图谱
      this.getGraph()
    }
  },
  mounted() {
    this.initMyEcharts()
  },
  methods: {
    getGraph() {
      get_graph({
        id: this.graph_id
      }).then((res) => {
        this.nodes = res.nodes
        this.links = res.links
        this.barChartData = res.barChartData
        this.pieChartData = res.pieChartData
        this.updateMyecharts()
      })
    },
    initMyEcharts() {
      this.myChart = this.$echarts.init(this.$refs.graph)
      this.getGraph()
    },
    updateMyecharts() {
      this.myChart.showLoading()
      var data = this.nodes
      var links = this.links
      var categories = [{ name: '设备' }, { name: '缺陷' }, { name: '图片' }, { name: '危害' }, { name: '成因' }, { name: '措施' }, { name: '设备型号' }, { name: '状态量' }, { name: '缺陷分类' }, { name: '分类依据' }, { name: '判断依据' }]
      var categoriesSelected
      var graphZoom
      if (this.graph_id === '0' || this.graph_id === '1') {
        categoriesSelected = {
          '设备': true, '缺陷': true, '图片': true, '危害': true, '成因': true, '措施': true, '设备型号': true, '状态量': true, '缺陷分类': true, '分类依据': true, '判断依据': true
        }
        graphZoom = 2
      } else if (this.graph_id === '2') {
        categoriesSelected = {
          '设备': true, '缺陷': true, '图片': false, '危害': false, '成因': false, '措施': false, '设备型号': false, '状态量': false, '缺陷分类': false, '分类依据': false, '判断依据': false
        }
        graphZoom = 2
      } else {
        categoriesSelected = {
          '设备': true, '缺陷': true, '图片': true, '危害': false, '成因': false, '措施': false, '设备型号': false, '状态量': false, '缺陷分类': false, '分类依据': false, '判断依据': false
        }
        graphZoom = 2
      }
      // var graphId = this.graph_id
      data.forEach(function(data) {
        data.category = categories[data.classof - 1].name
        data.label = {
          normal: {
            show: true, // (data.name.length <= 5 && (graphId === '0' || graphId === '1'))
            position: 'middle'
          }
        }
        data.symbolSize = 50
      })
      links.forEach(function(links) {
        links.label = {
          show: false,
          position: 'middle',
          formatter: links.name
        }
      })
      for (var i = 0; i < data.length; i++) {
        if (data[i].classof === 3) {
          var symbolImg = 'image://' + require('./' + data[i].imgsrc)
          data[i].symbol = symbolImg
          data[i].symbolSize = 60
          data[i].symbolKeepAspect = true
        }
        if (data[i].introduction !== 'None') {
          data[i].value = '介绍：' + data[i].introduction
        } else if (data[i].content !== 'None') {
          data[i].value = '介绍：' + data[i].content
        }
      }
      // 指定图表的配置项和数据
      var option = {
        // title: {
        //   text: '电力设备缺陷知识图谱',
        //   top: 'top',
        //   left: 'left'
        // },
        tooltip: {
          show: true,
          textStyle: {
            width: 50,
            height: 50
          },
          formatter: function(x) {
            return x.value[50]
          }
        },
        toolbar: {
          show: true,
          featrue: {
            dataView: {
              show: true,
              readOnly: true
            },
            restore: {
              show: true
            },
            saveAsImage: {
              show: true
            }
          }
        },
        animationDuration: 2500,
        animationEasingUpdate: 'quinticInOut',
        legend: {
          orient: 'vertical',
          show: true,
          top: 'bottom',
          left: 'right',
          data: ['设备', '缺陷', '图片', '危害', '成因', '措施', '设备型号', '状态量', '缺陷分类', '分类依据', '判断依据'],
          selected: categoriesSelected
        },
        series: [{
          type: 'graph',
          layout: 'force',
          zoom: graphZoom,
          force: {
            // initLayout: 'circular',
            edgeLength: 150,
            repulsion: 100,
            gravity: 0
          },
          data: data,
          links: links,
          categories: categories,
          focusNodeAdjacency: true,
          roam: true,
          label: {
            show: true,
            normal: {
              position: 'right',
              formatter: '{b}'
            }
          },
          lineStyle: {
            color: 'source',
            curveness: 0
          },
          itemStyle: {
            normal: {
              borderColor: '#fff',
              borderWidth: 1,
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.3)'
            }
          },
          emphasis: {
            lineStyle: {
              width: 2
            }
          },
          edgeSymbol: ['', 'arrow'],
          edgeSymbolSize: 5
        }]
      }
      // 使用刚指定的配置项和数据显示图表。
      this.myChart.hideLoading()
      this.myChart.setOption(option)
    }
  }
}
</script>
