!macro customInit
    # 安装程序初始化时执行的脚本
    MessageBox MB_OK "欢迎安装 ClassManer!"
!macEndInit

!macro customInstall
    # 主要安装过程完成后执行的脚本
    CreateDirectory "$INSTDIR\data"
    WriteIniStr "$INSTDIR\data\config.ini" "Settings" "InstallPath" "$INSTDIR"
    
    # 创建开始菜单快捷方式的额外选项
    CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\卸载程序.lnk" "$INSTDIR\Uninstall.exe"
!macEndInstall

!macro customUnInstall
    # 卸载时执行的脚本
    RMDir /r "$INSTDIR\data"
    Delete "$SMPROGRAMS\${PRODUCT_NAME}\卸载程序.lnk"
!macEndUnInstall
