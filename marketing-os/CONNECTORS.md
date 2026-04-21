# Connectors - Marketing OS

This plugin integrates with external tools via MCP (Model Context Protocol).

## Available Connectors

| Connector | Purpose | Authentication |
|-----------|---------|----------------|
| **Notion** | Content calendar, planning, documentation | OAuth via Notion |
| **Figma** | Design assets, UI components, mockups | OAuth via Figma |
| **Canva** | Graphics, social media designs, templates | OAuth via Canva |
| **Slack** | Team notifications, content approvals | OAuth via Slack |
| **Similarweb** | Competitor analysis, traffic data, trends | API key required |
| **Meta Ads (Especializei)** | Create/manage Meta ad campaigns, audiences, creatives | OAuth via Meta |
| **Playwright** | Browser automation, screenshot capture, web testing | Local (no auth) |

## Connector Usage

### Notion
Use for content calendars, editorial planning, and storing brand guidelines.
- Create and manage content databases
- Track publication status
- Store reference materials

### Figma
Access design files and export assets for social media.
- Get design specs and dimensions
- Export images for posts
- Review design mockups

### Canva
Create and edit graphics directly.
- Generate social media graphics
- Access brand templates
- Create carousel slides

### Slack
Send notifications and get approvals.
- Notify team of new content
- Request reviews and approvals
- Share published content links

### Similarweb
Analyze competitors and market trends.
- Traffic analysis
- Competitor benchmarking
- Trend identification

### Meta Ads (Especializei)
Create and manage advertising campaigns on Meta platforms.
- Create campaigns, ad sets, and ads
- Target audiences with interests, demographics, and behaviors
- Generate ad creatives and copy
- Monitor ad performance and insights
- Search Meta Ads archive for competitor research

### Playwright
Automate browser interactions for testing and content capture.
- Take screenshots of web pages
- Navigate and interact with websites
- Capture competitor page layouts
- Test landing pages

## Setup

Each connector requires authentication. When you first use a connector, you'll be prompted to authorize access through the respective service.

## Local Scripts

This plugin also includes Python scripts that run locally:

| Script | Purpose |
|--------|---------|
| `seo_analyzer.py` | Analyze content for SEO |
| `hashtag_generator.py` | Generate relevant hashtags |
| `hook_generator.py` | Generate viral hooks |
| `trend_tracker.py` | Track trending topics |
| `competitor_analyzer.py` | Analyze competitor profiles |

Run scripts from the `scripts/` directory.
