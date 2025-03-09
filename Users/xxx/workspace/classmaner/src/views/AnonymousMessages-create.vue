

const router = useRouter();
const apiBase = import.meta.env.VITE_API_BASE;

// 表单数据
const form = reactive({
  content: ''
});

// 加载状态
const isLoading = ref(false);

// wangEditor 实例
const editor = shallowRef(null);
const editorRef = ref(null);

onMounted(() => {

  // 使用正确的初始化方法
  editor.value = WangEditor.createEditor({
    selector: editorRef.value,
    config: {
      placeholder: '请输入留言内容...',
      onChange(editor) {
        form.content = editor.getHtml();
      }
    }
  });
});
