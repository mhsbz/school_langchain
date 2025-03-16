const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  // Vue 3兼容模式配置
  chainWebpack: config => {
    config.resolve.alias.set('vue', '@vue/compat')
    
    config.module
      .rule('vue')
      .use('vue-loader')
      .tap(options => {
        return {
          ...options,
          compilerOptions: {
            compatConfig: {
              MODE: 2
            }
          }
        }
      })
  }
})
