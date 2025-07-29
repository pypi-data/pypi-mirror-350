import { h, ref, watch, computed, normalizeClass as _normalizeClass } from "vue";
import { createHighlighter } from "@shiki";
import { useClipboard } from "@instaui-tools/browser";


const highlighterTask = createHighlighter({
  themes: ["vitesse-dark", 'vitesse-light']
})
const getTransformersModule = transformersModuleGetter()


export default {
  props: ['code', 'language', 'theme', 'themes', 'transformers', 'lineNumbers'],
  setup(props) {
    const { transformers: transformerNames = [], themes = {
      light: 'vitesse-light',
      dark: 'vitesse-dark'
    } } = props;

    const highlightedCode = ref('');
    const realLanguage = computed(() => props.language || 'python')
    const realTheme = computed(() => props.theme || 'light')
    const realLineNumbers = computed(() => props.lineNumbers ?? true)
    const classes = computed(() => {
      return _normalizeClass([
        `language-${realLanguage.value}`,
        `theme-${realTheme.value}`,
        `shiki-code`,
        { 'line-numbers': realLineNumbers.value }
      ])
    })

    watch([() => props.code, realTheme], async ([code, _]) => {
      if (!code) {
        return;
      }
      code = code.trim()
      const highlighter = await highlighterTask;
      const transformers = await getTransformers(transformerNames)

      highlightedCode.value = await highlighter.codeToHtml(code, {
        themes,
        lang: realLanguage.value,
        transformers,
        defaultColor: realTheme.value,
        colorReplacements: {
          '#ffffff': '#f8f8f2'
        }
      });

    }, { immediate: true });


    // copy button
    const { copyButtonClick, btnClasses } = readyCopyButton(props)

    return () => h("div",
      { class: classes.value },
      [h("button", { class: btnClasses.value, title: "Copy Code", onClick: copyButtonClick }),
      h("span", { class: "lang", }, realLanguage.value),
      h('div', { innerHTML: highlightedCode.value, style: 'overflow:hidden;' })
      ]
    );
  }

}


function readyCopyButton(props) {
  const { copy, copied } = useClipboard({ source: props.code, legacy: true })

  const btnClasses = computed(() => {
    return _normalizeClass([
      "copy",
      { "copied": copied.value }
    ])
  })

  /**
   * 
   * @param {Event} e 
   */
  function copyButtonClick(e) {
    copy(props.code)

    watch(copied, (copied) => {
      if (!copied) {
        e.target.blur()
      }
    }, { once: true })
  }

  return {
    copyButtonClick,
    btnClasses,
  }
}


/**
 * 
 * @param {string[]} names 
 */
async function getTransformers(names) {
  if (names.length === 0) {
    return [];
  }

  const tfModule = await getTransformersModule()
  return names.map(name => {
    const realName = `transformer${name.charAt(0).toUpperCase() + name.slice(1)}`
    return tfModule[realName]()
  })
}


function transformersModuleGetter() {
  let module = null;

  return async () => {
    if (!module) {
      module = await import(`@shiki/transformers`)
    }
    return module;
  }
}
