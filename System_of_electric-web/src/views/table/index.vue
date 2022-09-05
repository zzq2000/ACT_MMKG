<template>
  <div class="app-container">
    <div style="margin: 20px 0;" />
    <h3>缺陷文本输入</h3>
    <el-row :gutter="60">
      <el-col :span="16">
        <h5>输入报告文本</h5>
        <el-input
          v-model="textarea"
          type="textarea"
          :autosize="{ minRows: 8, maxRows: 8}"
          placeholder="请输入文本"
          style="margin-bottom: 15px"
        />
        <el-button type="primary" @click="onSubmit()">
          提交
        </el-button>
        <el-button @click="refresh()">
          重置
        </el-button>
      </el-col>
      <el-col :span="8">
        <h5>或上传报告文件</h5>
        <el-upload
          class="upload-demo"
          drag
          action="https://jsonplaceholder.typicode.com/posts/"
          multiple
        >
          <i class="el-icon-upload" />
          <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          <div slot="tip" class="el-upload__tip">上传txt/word/pdf文件，且不超过500kb</div>
        </el-upload>
      </el-col>
    </el-row>
    <h3>缺陷事件检测结果</h3>
    <el-table
      v-loading="loading"
      element-loading-text="正在检测中"
      element-loading-spinner="el-icon-loading"
      :data="tableData"
      style="width: 100%"
      stripe
    >
      <el-table-column
        prop="ID"
        label="ID"
        width="50"
      />
      <el-table-column
        prop="缺陷文本"
        label="缺陷文本"
      />
      <el-table-column
        prop="缺陷触发词"
        label="缺陷触发词"
        width="200"
      />
      <el-table-column
        prop="缺陷分类"
        label="缺陷分类"
        width="200"
      />
    </el-table>
  </div>
</template>

<script>
import { get_detection } from '../../api/table'
export default {
  data() {
    return {
      list: null,
      listLoading: true,
      textarea: '',
      tableData: [],
      loading: false
    }
  },
  methods: {
    onSubmit() {
      this.loading = true
      get_detection({
        text: this.textarea
      }).then((res) => {
        this.tableData = res.tableData
        this.loading = false
      })
    },
    refresh() {
      this.textarea = ''
      this.tableData = []
    }
  }
}
</script>
