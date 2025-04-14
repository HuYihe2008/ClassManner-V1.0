// 控制应用生命周期和创建原生浏览器窗口的模组
const { app, BrowserWindow, Menu } = require('electron')
const path = require('path')

// 添加在 app.whenReady() 之前
app.commandLine.appendSwitch('disable-http-cache');
app.commandLine.appendSwitch('disable-gpu-vsync');
app.commandLine.appendSwitch('disable-software-rasterizer');

async function createWindow() {
  const win = new BrowserWindow({
    width: 1300,
    height: 800,
    show: false, // 先隐藏窗口
    webPreferences: {
      nodeIntegration: true, //开启true这一步很重要,目的是为了vue文件中可以引入node和electron相关的API
      contextIsolation: true, // 可以使用require方法
      enableRemoteModule: true, // 可以使用remote方法
    },
  });

  // 创建加载窗口
  const loadingWin = new BrowserWindow({
    width: 300,
    height: 200,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    webPreferences: {
      nodeIntegration: true
    }
  });

  // 加载简单的加载页面
  loadingWin.loadFile('loading.html');

  // 主窗口加载完成后显示
  win.once('ready-to-show', () => {
    loadingWin.destroy();
    win.show();
  });

  let env = 'pro2'
  // 配置热更新
  if (env == 'pro') {
    const elePath = path.join(__dirname, '../node_modules/electron')
    require('electron-reload')('../', {
      electron: require(elePath),
    })
    // 热更新监听窗口
    win.loadURL('http://localhost:5173')
    // 打开开发工具
    win.webContents.openDevTools()
  } else {
    // 生产环境中要加载文件，打包的版本
    Menu.setApplicationMenu(null)
    // 加载 index.html
    win.loadFile(path.resolve(__dirname, '../dist/index.html')) // 新增
  }

  // 修改加载完成的处理逻辑
  win.webContents.on('did-finish-load', () => {
    setTimeout(() => {
      win.show()
      // 触发一次路由跳转
      win.webContents.executeJavaScript('window.router.push("/")');
    }, 100)
  })

  // 添加错误处理
  win.webContents.on('did-fail-load', () => {
    console.error('Window failed to load')
    win.reload()
  })
}

// 这段程序将会在 Electron 结束初始化
// 和创建浏览器窗口的时候调用
// 部分 API 在 ready 事件触发后才能使用。
app.whenReady().then(() => {
  createWindow()

  app.on('activate', function () {
    // 通常在 macOS 上，当点击 dock 中的应用程序图标时，如果没有其他
    // 打开的窗口，那么程序会重新创建一个窗口。
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// 除了 macOS 外，当所有窗口都被关闭的时候退出程序。 因此，通常对程序和它们在
// 任务栏上的图标来说，应当保持活跃状态，直到用户使用 Cmd + Q 退出。
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})