<template>
  <div style="margin:8px" @keyup.enter="search">
    <el-input v-model="input" placeholder="请输入关键字检索" class="input-with-select" style="margin-bottom:15px">
      <el-select slot="prepend" v-model="select" placeholder="请选择检索方式">
        <el-option label="图谱检索" value="1" />
        <el-option label="百科检索" value="2" />
      </el-select>
      <el-button slot="append" icon="el-icon-search" @click="search" />
    </el-input>
    <el-row v-if="info.name != '' && select==='1'" class="search-result" :gutter="10" style="margin-bottom:15px">
      <el-col :span="12">
        <el-card shadow="hover" style="height:540px">
          <h3>设备信息</h3>
          <p><b>设备名称：</b><span>{{ info.name }}</span></p>
          <p><b>设备简介：</b><span>{{ info.intro }}</span></p>
          <el-row :gutter="10">
            <el-col :span="12">
              <el-card shadow="hover" align="center">
                <p><b>设备图片</b></p>
                <el-image v-if="imgsrc != ''" :src="require('../dashboard/' + imgsrc)" style="height:260px" />
                <p v-else>暂无设备图片</p>
              </el-card>
            </el-col>
            <el-col :span="12" align="center">
              <el-card shadow="hover">
                <p><b>设备VR模型</b></p>
                <iframe src="/static/test3d-part1ofTransformer-dry-type.html" scrolling="no" frameborder="0" style="width:100%;height:260px;" />
              </el-card>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover" style="height: 540px">
          <div ref="graph" class="test" style="height: 500px" />
        </el-card>
      </el-col>
    </el-row>
    <el-table
      v-if="info.name != '' && select==='1'"
      :data="tableData"
      style="width: 100%"
      :row-class-name="tableRowClassName"
    >
      <el-table-column
        prop="缺陷"
        label="常见缺陷"
      />
      <el-table-column
        prop="危害"
        label="缺陷危害"
      />
      <el-table-column
        prop="等级"
        label="缺陷等级"
      />
      <el-table-column
        prop="措施"
        label="对应措施"
        :show-overflow-tooltip="true"
        :formatter="stateFormat"
      />
    </el-table>
    <el-row v-else-if="info.name != '' && select === '2'" height="100%">
      <iframe id="baiduAPI" :src="'https://www.baidu.com/s?wd=' + input" />
    </el-row>
  </div>
</template>

<script>
import { get_search } from '../../api/search'
export default {
  name: 'Index',
  data() {
    return {
      select: '1',
      input: '',
      info: {
        name: '',
        intro: '',
        img: ''
      },
      graph: {
        nodes: [],
        links: []
      },
      tableData: [],
      myChart: {},
      imgsrc: '',
      time: 0,
      contentLength: 10
    }
  },
  mounted() {
    this.init_myecharts()
  },
  methods: {
    search() {
      if (this.select === '1') {
        get_search({
          name: this.input
        }).then((res) => {
          this.info.name = res.node.name
          this.info.intro = res.node.introduction === 'None' ? '暂未设备介绍' : res.node.introduction
          this.graph.nodes = res.graph.nodes
          this.graph.links = res.graph.links
          this.imgsrc = res.imgsrc
          this.tableData = res.tableData
          setTimeout(() => {
            this.update_myecharts()
          }, 0)
        })
      } else {
        // 调用百度百科API
        this.info.name = this.input
      }
    },
    tableRowClassName({ row, rowIndex }) {
      const level = row.等级
      if (level === '危急') {
        return 'urgent-row'
      } else if (level === '严重') {
        return 'serious-row'
      } else if (level === '一般') {
        return 'general-row'
      }
    },
    init_myecharts() {
    },
    update_myecharts() {
      if (this.time === 0) {
        this.time += 1
        this.myChart = this.$echarts.init(this.$refs.graph)
      }
      var data = this.graph.nodes
      var links = this.graph.links
      var categories = [{ name: '设备' }, { name: '缺陷' }, { name: '图片' }, { name: '危害' }, { name: '成因' }, { name: '措施' }, { name: '设备型号' }, { name: '状态量' }, { name: '缺陷分类' }, { name: '分类依据' }, { name: '判断依据' }]
      data.forEach(function(data) {
        data.category = categories[data.classof - 1].name
        data.label = {
          normal: {
            show: true,
            position: 'top'
          }
        }
        data.symbolSize = 20
      })
      links.forEach(function(links) {
        links.label = {
          show: true,
          position: 'middle',
          formatter: links.name
        }
      })
      for (var i = 0; i < data.length; i++) {
        if (data[i].classof === 3) {
          var symbolImg = 'image://' + require('../dashboard/' + data[i].imgsrc)
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
      var option = {
        title: {
          text: '设备子图',
          top: 'top',
          left: 'left'
        },
        tooltip: {
          show: true,
          style: {
            width: 50,
            height: 50
          }
        },
        toolbar: {
          show: true,
          feature: {
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
          data: ['设备', '缺陷', '图片', '危害', '成因', '措施', '设备型号', '状态量', '缺陷分类', '分类依据', '判断依据']
        },
        series: [{
          type: 'graph',
          layout: 'force',
          zoom: 0.8,
          force: {
            // initLayout: 'circular',
            edgeLength: 200,
            repulsion: 200,
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
          edgeSymbolSize: 10
        }]
      }
      // 使用刚指定的配置项和数据显示图表。
      this.myChart.setOption(option)
    }
  }
}
</script>
<style>
  .el-select .el-input {
    width: 180px;
  }
  .input-with-select .el-input-group__prepend {
    background-color: #fff;
  }
  .el-table .urgent-row {
    background: rgb(247, 161, 161);
  }
  .el-table .serious-row {
    background: rgb(235, 241, 179);
  }
  .el-table .general-row {
    background: rgb(166, 247, 197);
  }
</style>
