// @ts-check
// Note: type annotations allow type checking and IDE autocompletion

import { themes as prismThemes } from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'AI Ecosystem Architecture & Governance',
  tagline: 'Conceptual models of the AI ecosystem, governance boundaries, and value flows.',
  favicon: 'img/favicon.ico',

  // Production URL settings for Sezoo GitHub Pages
  url: 'https://sezoo.github.io',
  baseUrl: '/ai-ecosystem-model/',

  // GitHub pages deployment configuration
  organizationName: 'Sezoo',
  projectName: 'ai-ecosystem-model',
  trailingSlash: false,

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // 1. Native Mermaid Diagram Configuration
  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          routeBasePath: '/', // "Docs-only" mode: Serves ecosystem docs at root URL
        },
        blog: false, // Disabled template blog
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Sezoo',
        logo: {
          alt: 'Sezoo Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'AI Ecosystem Models',
          },
          {
            href: 'https://sezoo.digital',
            label: 'sezoo.digital',
            position: 'right',
          },
          {
            href: 'https://github.com/Sezoo/ai-ecosystem-model',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Models',
            items: [
              {
                label: 'Ecosystem Architecture',
                to: '/',
              },
            ],
          },
          {
            title: 'Organization',
            items: [
              {
                label: 'Sezoo Digital',
                href: 'https://sezoo.digital',
              },
            ],
          },
          {
            title: 'Source Code',
            items: [
              {
                label: 'GitHub Repository',
                href: 'https://github.com/Sezoo/ai-ecosystem-model',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Sezoo. Built with Docusaurus & Mermaid.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
      mermaid: {
        theme: { light: 'neutral', dark: 'forest' },
      },
    }),
};

export default config;