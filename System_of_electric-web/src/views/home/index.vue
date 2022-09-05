<template>
  <div style="margin:8px">
    <el-row style="margin-bottom:8px">
      <iframe id="iframePano" src="/static/vtour/tour.html" height="400" width="100%" />
    </el-row>
    <div>
      <h2 style="text-align:center">—— 系统功能 ——</h2>
    </div>
    <el-row :gutter="25" style="margin-left:20px; margin-right:20px">
      <el-col :span="8" align="middle">
        <el-card shadow="hover" style="height:200px">
          <div>
            <img src="./产业链图谱.png" style="display:flex; margin:8%" height="70px">
          </div>
          <el-link type="primary" @click="gotoGraph"><h3>多模态知识图谱</h3></el-link>
          <!-- <p>多模态知识图谱以及图谱统计信息展示</p> -->
        </el-card>
      </el-col>
      <el-col :span="8" align="middle">
        <el-card shadow="hover" style="height:200px">
          <img src="./变压器.png" style="display: flex; margin:8%" height="70px">
          <el-link type="primary" @click="gotoSearch"><h3>设备信息检索</h3></el-link>
          <!-- <p>设备信息及常见缺陷查询</p> -->
        </el-card>
      </el-col>
      <el-col :span="8" align="middle">
        <el-card shadow="hover" style="height:200px">
          <img src="./缺陷检测查询.png" style="display: flex; margin:8%" height="70px">
          <el-link type="primary" @click="gotoTable"><h3>缺陷事件预警</h3></el-link>
          <!-- <p>文本报告缺陷预警</p> -->
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'Index',
  data() {
    return {
    }
  },
  mounted() {
    this.initPano()
  },
  methods: {
    initPano() {
      // var path = '/static/vtour/tour_testingserver.exe'
    },
    gotoGraph() {
      this.$router.push({
        name: '图谱展示页'
      })
    },
    gotoSearch() {
      this.$router.push({
        name: '设备信息检索'
      })
    },
    gotoTable() {
      this.$router.push({
        name: '缺陷预测'
      })
    }
  }
}
</script>
