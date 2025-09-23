<template>
  <div class="neo-baroque-prompt-selector">
    <div class="selector-header">
      <NeoBaroqueIcon symbol="❦" size="large" variant="gold" :glow="true" />
      <h3>选择你的AI助手</h3>
      <NeoBaroqueIcon symbol="❦" size="large" variant="gold" :glow="true" />
    </div>

    <div class="prompt-categories">
      <div
        v-for="(category, categoryName) in categorizedPrompts"
        :key="categoryName"
        class="prompt-category"
        :class="{ 'active': activeCategory === categoryName }"
        @click="activeCategory = categoryName"
      >
        <NeoBaroqueIcon
          :symbol="category.icon"
          size="medium"
          :variant="category.variant"
          :glow="activeCategory === categoryName"
        />
        <span>{{ category.name }}</span>
      </div>
    </div>

    <div class="prompt-options">
      <div
        v-for="prompt in categorizedPrompts[activeCategory]?.prompts || []"
        :key="prompt.value"
        class="prompt-option"
        :class="{
          'selected': selectedPrompt === prompt.value,
          'disabled': disabled
        }"
        @click="selectPrompt(prompt.value)"
      >
        <div class="prompt-option-header">
          <NeoBaroqueIcon
            :symbol="prompt.icon"
            size="large"
            :variant="getPromptVariant(prompt.category)"
            :glow="selectedPrompt === prompt.value"
            :sparkle="selectedPrompt === prompt.value"
          />
          <div class="prompt-option-title">
            <h4>{{ prompt.name }}</h4>
            <p>{{ prompt.description }}</p>
          </div>
        </div>

        <div class="prompt-option-footer">
          <div class="prompt-tags">
            <span
              v-for="tag in prompt.tags"
              :key="tag"
              class="prompt-tag"
              :style="{ backgroundColor: getTagColor(tag) }"
            >
              {{ tag }}
            </span>
          </div>
          <NeoBaroqueIcon
            v-if="selectedPrompt === prompt.value"
            symbol="✓"
            size="medium"
            variant="emerald"
            :glow="true"
          />
        </div>
      </div>
    </div>

    <div class="selected-info" v-if="selectedPrompt">
      <NeoBaroqueIcon symbol="✧" size="small" variant="gold" :glow="true" />
      <span>已选择: {{ getPromptDisplayName(selectedPrompt) }}</span>
    </div>
  </div>
</template>

<script>
import NeoBaroqueIcon from './NeoBaroqueIcon.vue'

export default {
  name: 'NeoBaroquePromptSelector',
  components: {
    NeoBaroqueIcon
  },
  props: {
    availablePrompts: {
      type: Array,
      default: () => []
    },
    selectedPrompt: {
      type: String,
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      activeCategory: 'learning'
    }
  },
  computed: {
    categorizedPrompts() {
      const categories = {
        learning: {
          name: '学习成长',
          icon: '📚',
          variant: 'gold',
          prompts: [
            {
              value: 'learn_word',
              name: '单词词源分析',
              description: '深度分析单词词源、词根词缀，建立记忆网络',
              icon: '📖',
              category: 'learning',
              tags: ['语言学习', '词源学', '记忆技巧']
            },
            {
              value: 'explain_math_concept',
              name: '数学概念原理解析',
              description: '挖掘数学概念的直觉起源，还原发现时的惊喜',
              icon: '🔢',
              category: 'learning',
              tags: ['数学', '概念理解', '直觉思维']
            },
            {
              value: 'coding_mentor',
              name: '编程概念导师',
              description: '用生动类比讲解编程概念，降低学习门槛',
              icon: '💻',
              category: 'learning',
              tags: ['编程', '技术', '教学']
            }
          ]
        },
        thinking: {
          name: '思维训练',
          icon: '🧠',
          variant: 'royal',
          prompts: [
            {
              value: 'first_principles',
              name: '第一性原理分析',
              description: '回归本质，从第一性原理重新思考问题',
              icon: '⚡',
              category: 'thinking',
              tags: ['思维方法', '创新', '本质思考']
            },
            {
              value: 'turmin_argumentative_structure',
              name: '图尔敏论证模型',
              description: '运用图尔敏模型分析论证结构，提升逻辑思维',
              icon: '🏛️',
              category: 'thinking',
              tags: ['逻辑学', '论证', '批判思维']
            },
            {
              value: 'logical_thinker',
              name: '逻辑思维训练',
              description: '运用逻辑框架分析问题，推导合理结论',
              icon: '🧠',
              category: 'thinking',
              tags: ['逻辑分析', '问题解决', '推理']
            }
          ]
        },
        creative: {
          name: '创意表达',
          icon: '🎨',
          variant: 'ruby',
          prompts: [
            {
              value: 'concept_svg',
              name: '禅意概念图解',
              description: '用极简主义美学解释复杂概念，生成禅意SVG图',
              icon: '🎨',
              category: 'creative',
              tags: ['可视化', '设计', '美学']
            },
            {
              value: 'creative_writer',
              name: '创意写作大师',
              description: '激发创作灵感，提供个性化写作指导',
              icon: '✍️',
              category: 'creative',
              tags: ['写作', '创意', '文学']
            },
            {
              value: 'sugeladi_talk',
              name: '苏格拉底对话',
              description: '苏格拉底式对话，通过追问探寻问题的本质',
              icon: '🎭',
              category: 'creative',
              tags: ['对话', '哲学', '深度思考']
            }
          ]
        },
        technical: {
          name: '技术架构',
          icon: '🏗️',
          variant: 'sapphire',
          prompts: [
            {
              value: 'project_architect',
              name: '数字架构师',
              description: '设计完整的技术架构和项目实施路径',
              icon: '🏗️',
              category: 'technical',
              tags: ['架构设计', '技术选型', '项目管理']
            }
          ]
        }
      }

      // Filter prompts based on available prompts
      Object.keys(categories).forEach(category => {
        categories[category].prompts = categories[category].prompts.filter(
          prompt => this.availablePrompts.includes(prompt.value)
        )
      })

      return categories
    }
  },
  methods: {
    selectPrompt(promptValue) {
      if (!this.disabled) {
        this.$emit('select', promptValue)
      }
    },
    getPromptVariant(category) {
      const variantMap = {
        learning: 'gold',
        thinking: 'royal',
        creative: 'ruby',
        technical: 'sapphire'
      }
      return variantMap[category] || 'gold'
    },
    getTagColor(tag) {
      const colorMap = {
        '语言学习': 'rgba(212, 175, 55, 0.2)',
        '词源学': 'rgba(212, 175, 55, 0.2)',
        '记忆技巧': 'rgba(212, 175, 55, 0.2)',
        '数学': 'rgba(15, 76, 129, 0.2)',
        '概念理解': 'rgba(15, 76, 129, 0.2)',
        '直觉思维': 'rgba(15, 76, 129, 0.2)',
        '编程': 'rgba(80, 200, 120, 0.2)',
        '技术': 'rgba(80, 200, 120, 0.2)',
        '教学': 'rgba(80, 200, 120, 0.2)',
        '思维方法': 'rgba(75, 0, 130, 0.2)',
        '创新': 'rgba(75, 0, 130, 0.2)',
        '本质思考': 'rgba(75, 0, 130, 0.2)',
        '逻辑学': 'rgba(75, 0, 130, 0.2)',
        '论证': 'rgba(75, 0, 130, 0.2)',
        '批判思维': 'rgba(75, 0, 130, 0.2)',
        '逻辑分析': 'rgba(75, 0, 130, 0.2)',
        '问题解决': 'rgba(75, 0, 130, 0.2)',
        '推理': 'rgba(75, 0, 130, 0.2)',
        '可视化': 'rgba(224, 17, 95, 0.2)',
        '设计': 'rgba(224, 17, 95, 0.2)',
        '美学': 'rgba(224, 17, 95, 0.2)',
        '写作': 'rgba(224, 17, 95, 0.2)',
        '创意': 'rgba(224, 17, 95, 0.2)',
        '文学': 'rgba(224, 17, 95, 0.2)',
        '对话': 'rgba(224, 17, 95, 0.2)',
        '哲学': 'rgba(224, 17, 95, 0.2)',
        '深度思考': 'rgba(224, 17, 95, 0.2)',
        '架构设计': 'rgba(15, 76, 129, 0.2)',
        '技术选型': 'rgba(15, 76, 129, 0.2)',
        '项目管理': 'rgba(15, 76, 129, 0.2)'
      }
      return colorMap[tag] || 'rgba(212, 175, 55, 0.2)'
    },
    getPromptDisplayName(prompt) {
      const names = {
        'learn_word': '单词词源分析',
        'concept_svg': '禅意概念图解',
        'turmin_argumentative_structure': '图尔敏论证模型',
        'explain_math_concept': '数学概念原理解析',
        'sugeladi_talk': '苏格拉底对话',
        'first_principles': '第一性原理分析',
        'project_architect': '数字架构师',
        'coding_mentor': '编程概念导师',
        'creative_writer': '创意写作大师',
        'logical_thinker': '逻辑思维训练'
      }
      return names[prompt] || prompt
    }
  }
}
</script>

<style scoped>
.neo-baroque-prompt-selector {
  background: rgba(255, 255, 255, 0.9);
  border-radius: var(--border-radius-ornate);
  border: var(--border-gold);
  padding: 30px;
  box-shadow: var(--shadow-ornate);
}

.selector-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 30px;
}

.selector-header h3 {
  font-family: var(--decorative-font);
  font-size: 1.8rem;
  color: var(--deep-blue);
  margin: 0;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

.prompt-categories {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
  flex-wrap: wrap;
  justify-content: center;
}

.prompt-category {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(244, 228, 193, 0.3);
  border: 1px solid var(--silver);
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold;
  color: var(--charcoal);
}

.prompt-category:hover {
  background: rgba(244, 228, 193, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
}

.prompt-category.active {
  background: var(--gold-gradient);
  color: var(--deep-blue);
  border-color: var(--primary-gold);
  box-shadow: var(--shadow-gold);
}

.prompt-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.prompt-option {
  background: rgba(255, 255, 255, 0.8);
  border: 2px solid var(--silver);
  border-radius: var(--border-radius-ornate);
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.prompt-option:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-deep);
  border-color: var(--primary-gold);
}

.prompt-option.selected {
  border-color: var(--primary-gold);
  background: rgba(244, 228, 193, 0.2);
  box-shadow: var(--shadow-gold);
}

.prompt-option.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.prompt-option.disabled:hover {
  transform: none;
  box-shadow: none;
}

.prompt-option-header {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
}

.prompt-option-title h4 {
  margin: 0 0 8px 0;
  color: var(--deep-blue);
  font-size: 1.2rem;
  font-family: var(--secondary-font);
}

.prompt-option-title p {
  margin: 0;
  color: var(--charcoal);
  font-size: 0.9rem;
  line-height: 1.4;
  opacity: 0.9;
}

.prompt-option-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
}

.prompt-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.prompt-tag {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: bold;
  color: var(--charcoal);
  white-space: nowrap;
}

.selected-info {
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: center;
  padding: 15px;
  background: rgba(212, 175, 55, 0.1);
  border-radius: var(--border-radius-ornate);
  color: var(--deep-blue);
  font-weight: bold;
}

/* Responsive Design */
@media (max-width: 768px) {
  .neo-baroque-prompt-selector {
    padding: 20px;
  }

  .selector-header {
    gap: 15px;
  }

  .selector-header h3 {
    font-size: 1.5rem;
  }

  .prompt-categories {
    gap: 10px;
  }

  .prompt-category {
    padding: 10px 15px;
    font-size: 0.9rem;
  }

  .prompt-options {
    grid-template-columns: 1fr;
    gap: 15px;
  }

  .prompt-option-header {
    flex-direction: column;
    text-align: center;
  }

  .prompt-option-footer {
    flex-direction: column;
    gap: 10px;
  }
}

/* Accessibility */
.prompt-option:focus {
  outline: 3px solid var(--primary-gold);
  outline-offset: 2px;
}

/* High Contrast Mode */
@media (prefers-contrast: high) {
  .prompt-option {
    border-width: 3px;
    border-color: var(--primary-gold);
  }

  .prompt-category {
    border-width: 2px;
  }
}
</style>