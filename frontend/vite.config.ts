import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { readFileSync } from 'fs'
import { resolve } from 'path'

// Vue export-helper 的源代码
const VUE_EXPORT_HELPER = `
export default (sfc, props) => {
  const target = sfc.__vccOpts || sfc;
  for (const [key, val] of props) {
    target[key] = val;
  }
  return target;
}
`

export default defineConfig({
  // 设置生产环境的基础路径（适配 Coze 平台）
  base: '/',
  resolve: {
    // 使用完整版 Vue（带编译器），支持模板字符串
    alias: {
      'vue': 'vue/dist/vue.esm-bundler.js'
    }
  },
  plugins: [
    vue({
      template: {
        compilerOptions: {
          isCustomElement: (tag) => tag.includes('-')
        }
      }
    }),
    // 使用自定义插件替换 Vite 的 env.mjs 和 client.mjs
    {
      name: 'fix-vite-hmr-variables',
      configureServer(server) {
        server.middlewares.use((req, res, next) => {
          // 直接提供 Vue export-helper 模块
          if (req.url?.includes('/@id/__x00__plugin-vue:export-helper')) {
            res.setHeader('Content-Type', 'application/javascript; charset=utf-8')
            res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            res.end(VUE_EXPORT_HELPER.trim())
            return
          }

          // 添加宽松的 CSP 头
          res.setHeader('Content-Security-Policy', "default-src 'self' 'unsafe-inline' 'unsafe-eval' http://localhost:* ws://localhost:*; script-src 'self' 'unsafe-inline' 'unsafe-eval' http://localhost:* ws://localhost:*; connect-src 'self' http://localhost:* ws://localhost:*")

          // 修复 env.mjs 中的 __DEFINES__
          if (req.url?.includes('/vite/dist/client/env.mjs')) {
            res.setHeader('Content-Type', 'application/javascript; charset=utf-8')
            const fixedEnv = readFileSync(resolve(__dirname, 'public/env.mjs'), 'utf-8')
            res.end(fixedEnv)
            return
          }

          // 修复 client.mjs 中的 HMR 变量
          if (req.url?.includes('/vite/dist/client/client.mjs')) {
            res.setHeader('Content-Type', 'application/javascript; charset=utf-8')
            const originalClient = readFileSync(
              resolve(__dirname, 'node_modules/.pnpm/vite@5.4.11/node_modules/vite/dist/client/client.mjs'),
              'utf-8'
            )

            // 替换所有需要定义的变量
            const fixedClient = originalClient
              .replace(/__HMR_CONFIG_NAME__/g, '"vite-hmr"')
              .replace(/__BASE__/g, '"/"')
              .replace(/__HMR_BASE__/g, '"/@hmr"')
              .replace(/__HMR_PORT__/g, '24678')
              .replace(/__HMR_HOSTNAME__/g, '"localhost"')
              .replace(/__HMR_PROTOCOL__/g, '"ws"')
              .replace(/__HMR_DIRECT_TARGET__/g, '""')
              .replace(/__HMR_ENABLE_OVERLAY__/g, 'true')
              .replace(/__HMR_TIMEOUT__/g, '30000')
              .replace(/__SERVER_HOST__/g, '""')

            res.end(fixedClient)
            return
          }

          next()
        })
      }
    },
    // 注入 HMR 变量到所有 HTML
    {
      name: 'inject-hmr-vars',
      transformIndexHtml(html) {
        // 检查是否已经注入过，避免重复
        if (html.includes('window.__HMR_CONFIG_NAME__')) {
          return html
        }

        // 在 </head> 之前插入 HMR 变量定义
        const hmrVarsScript = `<script>
window.__HMR_CONFIG_NAME__ = "vite-hmr";
window.__BASE__ = "/";
window.__DEFINES__ = { __VUE_OPTIONS_API__: true };
window.__HMR_BASE__ = "/@hmr";
window.__HMR_PORT__ = "24678";
window.__HMR_HOSTNAME__ = "localhost";
window.__HMR_PROTOCOL__ = "ws";
window.__HMR_DIRECT_TARGET__ = "";
window.__HMR_ENABLE_OVERLAY__ = true;
window.__HMR_TIMEOUT__ = "30000";
window.__SERVER_HOST__ = "";
</script>`
        return html.replace('</head>', hmrVarsScript + '</head>')
      }
    }
  ],
  server: {
    port: 5000,
    host: '0.0.0.0',
    strictPort: true,
    hmr: false, // 禁用 HMR 以避免连接问题
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true,
      }
    }
  },
  optimizeDeps: {
    // 强制预构建所有依赖，包括 @vitejs/plugin-vue
    include: [
      'vue',
      'vue-router',
      'pinia',
      '@vueup/vue-quill',
      '@vueuse/core',
      '@vitejs/plugin-vue'
    ],
    // 排除 fsevents，这是 macOS 专用的文件监视库，在 Linux 上会导致错误
    exclude: ['fsevents'],
  },
  clearScreen: false,
  define: {
    // 明确定义所有环境变量，避免 __DEFINES__ 错误
    __VUE_OPTIONS_API__: 'true',
    __VUE_PROD_DEVTOOLS__: 'false',
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: 'false',
  },
})
