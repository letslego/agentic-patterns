import { defineConfig } from 'vitepress'

const repo = 'agentic-patterns'
const owner = 'letslego'

export default defineConfig({
  title: 'Agentic Patterns',
  description: 'Companion guide and reference code for 21 agentic design patterns',
  base: `/${repo}/`,
  lang: 'en-US',
  cleanUrls: true,
  head: [['link', { rel: 'icon', href: `${`/${repo}/`}favicon.svg` }]],
  themeConfig: {
    logo: '/favicon.svg',
    nav: [
      { text: 'Guide', link: '/introduction' },
      { text: 'Patterns', link: '/part-1-foundational/01-prompt-chaining' },
      { text: 'Adapters', link: '/appendix/framework-adapters' },
      {
        text: 'GitHub',
        link: `https://github.com/${owner}/${repo}`,
      },
    ],
    sidebar: [
      {
        text: 'Introduction',
        items: [
          { text: 'Overview', link: '/' },
          { text: 'What makes a system agentic?', link: '/introduction' },
        ],
      },
      {
        text: 'Part 1 — Foundational',
        items: [
          { text: '01 Prompt Chaining', link: '/part-1-foundational/01-prompt-chaining' },
          { text: '02 Routing', link: '/part-1-foundational/02-routing' },
          { text: '03 Parallelization', link: '/part-1-foundational/03-parallelization' },
          { text: '04 Reflection', link: '/part-1-foundational/04-reflection' },
          { text: '05 Tool Use', link: '/part-1-foundational/05-tool-use' },
          { text: '06 Planning', link: '/part-1-foundational/06-planning' },
          { text: '07 Multi-Agent', link: '/part-1-foundational/07-multi-agent' },
        ],
      },
      {
        text: 'Part 2 — Advanced',
        items: [
          { text: '08 Memory Management', link: '/part-2-advanced/08-memory-management' },
          { text: '09 Learning & Adaptation', link: '/part-2-advanced/09-learning-adaptation' },
          { text: '10 MCP', link: '/part-2-advanced/10-mcp' },
          { text: '11 Goal Monitoring', link: '/part-2-advanced/11-goal-monitoring' },
        ],
      },
      {
        text: 'Part 3 — Production',
        items: [
          { text: '12 Exception Handling', link: '/part-3-production/12-exception-handling' },
          { text: '13 Human-in-the-Loop', link: '/part-3-production/13-human-in-the-loop' },
          { text: '14 RAG', link: '/part-3-production/14-rag' },
        ],
      },
      {
        text: 'Part 4 — Multi-Agent',
        items: [
          { text: '15 Inter-Agent Communication', link: '/part-4-multi-agent/15-inter-agent-communication' },
          { text: '16 Resource Optimization', link: '/part-4-multi-agent/16-resource-optimization' },
          { text: '17 Reasoning', link: '/part-4-multi-agent/17-reasoning' },
          { text: '18 Guardrails', link: '/part-4-multi-agent/18-guardrails' },
          { text: '19 Evaluation', link: '/part-4-multi-agent/19-evaluation' },
          { text: '20 Prioritization', link: '/part-4-multi-agent/20-prioritization' },
          { text: '21 Exploration', link: '/part-4-multi-agent/21-exploration' },
        ],
      },
      {
        text: 'Appendix',
        items: [
          { text: 'Framework notes', link: '/appendix/frameworks' },
          { text: 'LangChain / LangGraph adapters', link: '/appendix/framework-adapters' },
        ],
      },
    ],
    socialLinks: [{ icon: 'github', link: `https://github.com/${owner}/${repo}` }],
    editLink: {
      pattern: `https://github.com/${owner}/${repo}/edit/main/docs/:path`,
      text: 'Edit this page on GitHub',
    },
    footer: {
      message: 'Open-source guide and reference code for agentic design patterns.',
      copyright: 'MIT License',
    },
    search: { provider: 'local' },
  },
})
