// @ts-check
// Note: type annotations allow type checking and IDE autocompletion

import { themes as prismThemes } from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'AI Ecosystem Architecture & Governance',
  tagline: 'Conceptual models of the AI ecosystem, governance boundaries, and value flows.',
  favicon: 'img/Sezoo-favicon.ico',

  // Production URL settings for Sezoo GitHub Pages
  url: 'https://ai-ecosystem.sezoo.digital',
  baseUrl: '/',

  // GitHub pages deployment configuration
  organizationName: 'Sezoo',
  projectName: 'ai-ecosystem-model',
  trailingSlash: false,

  onBrokenLinks: 'throw',

  // 1. Native Mermaid Diagram Configuration
  // Move onBrokenMarkdownLinks inside markdown.hooks
  markdown: {
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
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
          src: 'img/Sezoo_Logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'ecosystemSidebar',
            position: 'left',
            label: 'AI Ecosystem Model',
          },
          {
            href: 'pathname:///viewer/',
            label: 'Interactive Explorer',
            position: 'left',
          },
          {
            href: 'https://sezoo.digital',
            label: 'sezoo.digital',
            position: 'right',
          },
          {
            href: 'https://github.com/sezoo-digital/ai-ecosystem-model',
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
              {
                label: 'Licence & Attribution',
                to: '/licence', // Links directly to src/pages/licence.md
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Sezoo. Content licensed under <a href="/licence" style="color: var(--sezoo-brand-blue); text-decoration: underline;">CC BY-SA 4.0</a>. Code under MIT.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
      mermaid: {
        theme: { light: 'neutral', dark: 'dark' },
      },
    }),
};

export default config;
