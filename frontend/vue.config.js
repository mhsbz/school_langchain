const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  lintOnSave: false,
  chainWebpack: config => {
    config.module.rules.delete('eslint')
  }
})