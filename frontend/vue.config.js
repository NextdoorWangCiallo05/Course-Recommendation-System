const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true
      }
    },
    client: {
      overlay: false
    }
  },
  configureWebpack: {
    optimization: {
      splitChunks: {
        cacheGroups: {
          vendor: {
            name: 'chunk-vendor',
            test: /[\\/]node_modules[\\/]/,
            priority: 10,
            chunks: 'initial'
          },
          naiveui: {
            name: 'chunk-naiveui',
            test: /[\\/]node_modules[\\/]naive-ui[\\/]/,
            priority: 20,
            chunks: 'async'
          },
          echarts: {
            name: 'chunk-echarts',
            test: /[\\/]node_modules[\\/]echarts[\\/]/,
            priority: 20,
            chunks: 'async'
          },
          commons: {
            name: 'chunk-commons',
            minChunks: 3,
            priority: 5,
            reuseExistingChunk: true
          }
        }
      }
    }
  },
  chainWebpack: config => {
    config.when(process.env.NODE_ENV === 'production', config => {
      config.optimization.minimize(true)
      config.optimization.minimizer('terser').tap(args => {
        args[0].terserOptions = {
          compress: {
            drop_console: true,
            drop_debugger: true
          },
          output: {
            comments: false
          }
        }
        return args
      })
    })
    config.plugins.delete('prefetch')
  }
})
