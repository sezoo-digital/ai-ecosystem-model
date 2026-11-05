// @ts-check
// `@type {import('@docusaurus/types').Config}`

const config = {
  title: 'AI Ecosystem Architecture & Governance',
  tagline: 'Conceptual models of the AI ecosystem, governance boundaries, and value flows.',
  favicon: 'img/favicon.ico',

  // 1. URL Configuration
  // If using default GitHub Pages:
  url: 'https://sezoo.github.io',
  baseUrl: '/ai-ecosystem-model/',

  // (Optional: If you want a custom subdomain like https://ai-model.sezoo.digital,
  // set url: 'https://ai-model.sezoo.digital' and baseUrl: '/')

  organizationName: 'Sezoo',
  projectName: 'ai-ecosystem-model',
  trailingSlash: false,

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // 2. Enable Native Mermaid
  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          routeBasePath: '/', // Makes docs the root of the site (optional)
        },
        blog: false, // Turn off blog unless needed
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Configure Mermaid theme appearance
      mermaid: {
        theme: { light: 'neutral', dark: 'forest' },
      },
      navbar: {
        title: 'Sezoo AI Model',
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Ecosystem Models',
          },
          {
            href: 'https://github.com/Sezoo/ai-ecosystem-model',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
    }),
};

module.exports = config;