# Supsrc TUI UX Mockups

## Layout Categories

### A. Repository List Focused (Mockups 1-5)
These focus on repository status with different information density levels.

### B. Dashboard/Metrics Focused (Mockups 6-10)
These emphasize global metrics and activity monitoring.

### C. Selection Detail Views (Mockups 11-15)
These show detailed information when a repository is selected.

### D. Activity/Log Focused (Mockups 16-20)
These prioritize real-time activity and logging information.

---

## Mockup 1: Compact Repository Grid (No Selection)
**Data**: Basic repo status, minimal details
**Use Case**: Quick overview of many repositories

```
┌─ Supsrc Watcher ─ Monitoring 12 repos ─ 3 active ──────────────────────────────┐
│🏠 my-project    ✅ IDLE      ⏱️  2m ago    💾 3     📝 feat: auto-sync        │
│🔬 experiments   🔄 CHANGED   ⏱️  5s ago    💾 1     🚫 uncommitted changes    │
│📚 docs-site     ⚙️  STAGING  ⏱️  now       💾 7     ⏳ staging files...      │
│🎮 game-engine   ❌ ERROR     ⏱️  1h ago    💾 12    💥 push failed: auth      │
│📱 mobile-app    ✅ IDLE      ⏱️  15m ago   💾 0     🎉 v2.1.0 release         │
├─────────────────────────────────────────────────────────────────────────────────┤
│ GLOBAL ACTIVITY                     │ METRICS           │ RECENT COMMITS      │
│ 🔄 3 repos changed in last 5m      │ 📈 47 commits/day │ 🕐 2m ago: my-proj │
│ ⚡ 2 auto-commits in progress       │ 💾 156 saves/hr   │ 🕑 5m ago: docs    │
│ 🚨 1 error requiring attention     │ ⏱️  avg 3.2m cycle│ 🕒 12m ago: mobile │
│ 📊 Network: 4 pushes pending       │ 🎯 99.2% success  │ 🕓 18m ago: engine │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Mockup 2: Detailed Repository Table (No Selection)
**Data**: Comprehensive repo information in table format
**Use Case**: Professional/technical users wanting full details

```
┌─ Supsrc Watcher ─ Active Monitoring ────────────────────────────────────────────┐
│ REPO          │ST│ RULE        │ LAST CHG │ SAVES│ BRANCH   │ LAST ACTION      │
│──────────────────────────────────────────────────────────────────────────────────│
│🏠 my-project  │✅│ 5m inactiv  │ 2m ago   │   3  │ main     │ ✅ pushed        │
│🔬 experiments │🔄│ 10 saves    │ 5s ago   │   1  │ feature  │ 📝 detected chg  │
│📚 docs-site   │⚙️│ 2m inactiv  │ now      │   7  │ main     │ ⏳ staging...    │
│🎮 game-engine │❌│ manual      │ 1h ago   │  12  │ develop  │ 💥 auth failed   │
│📱 mobile-app  │✅│ 3m inactiv  │ 15m ago  │   0  │ main     │ 🎉 v2.1.0        │
│🧪 test-suite  │💤│ disabled    │ -        │   -  │ -        │ 🚫 disabled      │
├──────────────────────────────────────────────────────────────────────────────────┤
│ SYSTEM STATUS                                                                    │
│ 📊 Watching: 5/6 repos  🔄 Active: 2  ❌ Errors: 1  💤 Disabled: 1             │
│ 🌐 Network: Connected   🔧 Git: OK    📁 Paths: Valid   ⚡ Performance: Normal   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Mockup 3: Card-Based Repository View (No Selection)
**Data**: Repository cards with visual status indicators
**Use Case**: Visual/designer-friendly interface

```
┌─ Supsrc Watcher ─ Visual Mode ──────────────────────────────────────────────────┐
│ ╭─ 🏠 my-project ──────────────╮ ╭─ 🔬 experiments ─────────────╮            │
│ │ ✅ IDLE          ⏱️ 2m ago   │ │ 🔄 CHANGED       ⏱️ 5s ago   │            │
│ │ 💾 3 saves       📝 main     │ │ 💾 1 save        📝 feature   │            │
│ │ 🎯 5m inactivity rule        │ │ 🎯 10 saves rule             │            │
│ │ ✅ Last: feat: auto-sync     │ │ 📝 Last: uncommitted         │            │
│ ╰──────────────────────────────╯ ╰───────────────────────────────╯            │
│                                                                                │
│ ╭─ 📚 docs-site ───────────────╮ ╭─ 🎮 game-engine ─────────────╮            │
│ │ ⚙️ STAGING       ⏱️ now      │ │ ❌ ERROR         ⏱️ 1h ago   │            │
│ │ 💾 7 saves       📝 main     │ │ 💾 12 saves      📝 develop   │            │
│ │ 🎯 2m inactivity rule        │ │ 🎯 manual rule               │            │
│ │ ⏳ Status: staging files...  │ │ 💥 Error: push auth failed   │            │
│ ╰──────────────────────────────╯ ╰───────────────────────────────╯            │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 📈 ACTIVITY PULSE                    🔧 QUICK ACTIONS                          │
│ ▁▃▇█▅▂▁ Commits today               [Pause All] [Resume All] [Force Sync]      │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Mockup 4: Minimal Status Bar View (No Selection)
**Data**: Ultra-compact status overview
**Use Case**: Background monitoring with minimal screen real estate

```
┌─ Supsrc ─────────────────────────────────────────────────────────────────────────┐
│ 🏠✅ 🔬🔄 📚⚙️ 🎮❌ 📱✅ │ Active: 2/5 │ Saves: 21 │ Last: 5s │ Errors: 1 │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│ DETAILED ACTIVITY LOG                                                            │
│ 🕐 12:34:56 🔬 experiments    🔄 File changed: src/main.py                      │
│ 🕐 12:34:52 📚 docs-site      ⚙️ Staging 3 files for commit                    │
│ 🕐 12:34:48 🏠 my-project     ✅ Pushed successfully to origin/main             │
│ 🕐 12:32:15 🎮 game-engine    ❌ Push failed: authentication required          │
│ 🕐 12:31:45 📱 mobile-app     🎉 Committed: v2.1.0 release                     │
│ 🕐 12:30:12 🔬 experiments    📝 Auto-commit: progress on feature               │
│                                                                                  │
│ [CTRL+D] Details [SPACE] Pause [R] Refresh [Q] Quit                            │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Mockup 5: Tree/Hierarchical View (No Selection)
**Data**: Repositories organized by groups/status
**Use Case**: Large numbers of repositories with categorization

```
┌─ Supsrc Watcher ─ Tree View ────────────────────────────────────────────────────┐
│ 📁 ACTIVE REPOSITORIES (4)                                                      │
│   ├─ ✅ IDLE (2)                                                                │
│   │   ├─ 🏠 my-project      ⏱️ 2m ago    💾 3     📝 feat: auto-sync          │
│   │   └─ 📱 mobile-app      ⏱️ 15m ago   💾 0     🎉 v2.1.0 release           │
│   ├─ 🔄 ACTIVE (2)                                                             │
│   │   ├─ 🔬 experiments     ⏱️ 5s ago    💾 1     📝 uncommitted               │
│   │   └─ 📚 docs-site       ⏱️ now       💾 7     ⏳ staging...               │
│   └─ ❌ ERRORS (1)                                                             │
│       └─ 🎮 game-engine     ⏱️ 1h ago    💾 12    💥 push auth failed          │
│ 📁 DISABLED REPOSITORIES (1)                                                    │
│   └─ 💤 🧪 test-suite       (monitoring disabled)                             │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 🎯 RULES OVERVIEW           │ ⚡ PERFORMANCE            │ 🔔 ALERTS            │
│ ⏱️ Inactivity: 3 repos      │ 📊 CPU: 2.1%             │ 🚨 1 auth failure     │
│ 💾 Save count: 1 repo       │ 💾 Memory: 45MB          │ ⚠️ 0 warnings         │
│ 🔧 Manual: 1 repo           │ 🌐 Network: OK           │ ℹ️ 3 info messages     │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Mockup 6: Dashboard with Charts (No Selection)
**Data**: Metrics, graphs, and performance data
**Use Case**: Management/overview focus with analytics

```
┌─ Supsrc Dashboard ───────────────────────────────────────────────────────────────┐
│ 🏠my-project ✅ │ 🔬experiments 🔄 │ 📚docs-site ⚙️ │ 🎮game-engine ❌ │     │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 📊 COMMIT ACTIVITY (24h)     │ 💾 SAVE PATTERNS          │ 🎯 RULE EFFICIENCY  │
│ Hour  ▁▃▇█▅▂▁▃▇█▅▂▁▃▇█▅▂▁▃▇ │ Freq ▁▃▅▇█▅▃▁            │ Inactiv: 94% ✅     │
│ 00-06: 4 commits             │ Avg saves/commit: 3.2     │ Save ct: 87% ✅     │
│ 06-12: 12 commits            │ Peak: 14:30 (burst)       │ Manual:  100% ✅    │
│ 12-18: 8 commits             │ Low:  02:15 (quiet)       │                     │
│ 18-24: 6 commits             │                           │ 🔄 Auto-sync: ON    │
├──────────────────────────────┼───────────────────────────┼─────────────────────┤
│ 🌐 NETWORK STATUS            │ 📈 SUCCESS METRICS        │ ⚠️ ISSUES TRACKER   │
│ ✅ GitHub: Connected (2.1s)  │ Total commits: 1,247      │ 🚨 Auth failures: 1 │
│ ✅ GitLab: Connected (1.8s)  │ Success rate: 99.2%       │ ⚠️ Slow pushes: 0   │
│ ✅ BitBucket: Connected      │ Avg cycle: 3.2min         │ ℹ️ Path warnings: 0  │
│ 📡 Last sync: 30s ago        │ Fastest: 45s              │                     │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Mockup 7: Real-time Activity Stream (No Selection)
**Data**: Live activity feed with filtering
**Use Case**: Monitoring active development sessions

```
┌─ Supsrc Live Monitor ───────────────────────────────────────────────────────────┐
│ [Filter: All▼] [Auto-scroll: ON] [Sound: OFF] [Time: 12:35:42]    Active: 3    │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 🔄 LIVE ACTIVITY STREAM                                                         │
│                                                                                  │
│ ⏱️ 12:35:42 🔬 experiments    🔄 CHANGED    src/neural_net.py modified          │
│ ⏱️ 12:35:38 📚 docs-site      ⚙️ STAGING    Adding 3 files to index             │
│ ⏱️ 12:35:35 📚 docs-site      🔄 CHANGED    content/tutorial.md modified        │
│ ⏱️ 12:35:30 🏠 my-project     ✅ PUSHED     Successfully pushed to origin/main  │
│ ⏱️ 12:35:28 🏠 my-project     💾 COMMITTED  feat: implement user authentication  │
│ ⏱️ 12:35:25 🏠 my-project     ⚙️ STAGING    Staging modified files               │
│ ⏱️ 12:35:22 🏠 my-project     🔄 CHANGED    auth/login.py, auth/session.py      │
│ ⏱️ 12:34:55 🎮 game-engine    ❌ ERROR      Push failed: authentication required │
│ ⏱️ 12:34:45 📱 mobile-app     ✅ IDLE       All changes committed and pushed    │
│                                                                                  │
├──────────────────────────────────────────────────────────────────────────────────┤
│ SUMMARY: 47 events │ ERRORS: 1 │ COMMITS: 12 │ PUSHES: 8 │ [Clear] [Export]    │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Mockup 8: Control Panel Focus (No Selection)
**Data**: Repository controls and configuration
**Use Case**: Administrative control and rule management

```
┌─ Supsrc Control Panel ──────────────────────────────────────────────────────────┐
│ REPOSITORY CONTROLS                    │ GLOBAL SETTINGS                        │
│ ┌─ 🏠 my-project ─────────────────┐    │ ┌─ MONITORING ────────────────────┐    │
│ │ Status: ✅ IDLE                 │    │ │ ✅ Auto-monitoring enabled      │    │
│ │ Rule: ⏱️ 5min inactivity        │    │ │ ✅ Auto-commit enabled          │    │
│ │ [Pause] [Force Commit] [Reset]  │    │ │ ✅ Auto-push enabled            │    │
│ └─────────────────────────────────┘    │ │ 🔊 Notifications: Silent        │    │
│ ┌─ 🔬 experiments ────────────────┐    │ └─────────────────────────────────┘    │
│ │ Status: 🔄 CHANGED              │    │ ┌─ PERFORMANCE ───────────────────┐    │
│ │ Rule: 💾 10 saves               │    │ │ CPU Usage: ▁▃▅ 2.1%            │    │
│ │ [Pause] [Force Commit] [Reset]  │    │ │ Memory: ▁▂▃ 45MB               │    │
│ └─────────────────────────────────┘    │ │ File Watchers: 23 active        │    │
│ ┌─ 📚 docs-site ──────────────────┐    │ │ Network: 🟢 Healthy            │    │
│ │ Status: ⚙️ STAGING              │    │ └─────────────────────────────────┘    │
│ │ Rule: ⏱️ 2min inactivity        │    │                                        │
│ │ [⏸️ PROCESSING...] [Reset]       │    │ [⚙️ Settings] [📊 Reports] [❓ Help] │
│ └─────────────────────────────────┘    │                                        │
├─────────────────────────────────────────┴────────────────────────────────────────┤
│ 🚨 ALERTS & ACTIONS                                                              │
│ ❌ game-engine: Push authentication failed - [Fix Auth] [Disable Push] [Ignore] │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Mockup 9: Metrics-Heavy Dashboard (No Selection)
**Data**: Detailed statistics and performance metrics
**Use Case**: Data analysis and optimization

```
┌─ Supsrc Analytics ──────────────────────────────────────────────────────────────┐
│ REPOSITORY METRICS                                                               │
│ ┌─ ACTIVITY HEATMAP ─────────────────────┐ ┌─ EFFICIENCY SCORES ──────────────┐ │
│ │     Mon Tue Wed Thu Fri Sat Sun        │ │ 🏠 my-project:     ████████ 94%  │ │
│ │ 00h ▁▁▁ ▁▁▁ ▃▃▃ ▁▁▁ ▁▁▁ ▁▁▁ ▁▁▁        │ │ 🔬 experiments:    ██████▁▁ 78%  │ │
│ │ 06h ▃▃▃ ▅▅▅ ▇▇▇ ▅▅▅ ▃▃▃ ▁▁▁ ▁▁▁        │ │ 📚 docs-site:      ███████▁ 89%  │ │
│ │ 12h ▇▇▇ █▁█ ███ ▇▇▇ ▅▅▅ ▃▃▃ ▁▁▁        │ │ 🎮 game-engine:    ██▁▁▁▁▁▁ 34%  │ │
│ │ 18h ▅▅▅ ▃▃▃ ▅▅▅ ▃▃▃ ▁▁▁ ▁▁▁ ▁▁▁        │ │ 📱 mobile-app:     ████████ 96%  │ │
│ └────────────────────────────────────────┘ └───────────────────────────────────┘ │
│ ┌─ COMMIT FREQUENCY ─────────────────────┐ ┌─ RULE PERFORMANCE ───────────────┐ │
│ │ Daily avg: 23.4 commits                │ │ ⏱️ Inactivity rules: 892 triggers │ │
│ │ Peak day: Thursday (31 commits)        │ │ 💾 Save count rules: 156 triggers │ │
│ │ Peak hour: 14:00-15:00 (avg 4.2)      │ │ 🔧 Manual rules: 12 triggers      │ │
│ │ Trend: ↗️ +12% this week               │ │ False positives: 2.3%             │ │
│ └────────────────────────────────────────┘ └───────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────────────────────┤
│ FILE CHANGE PATTERNS                    │ REPOSITORY HEALTH                     │
│ Most changed: src/                      │ Disk usage: 2.3GB (Normal)           │
│ File types: .py(45%), .md(23%), .js(18%)│ Git status: All clean                │
│ Largest commits: 127 files (refactor)  │ Network latency: 1.2s avg            │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Mockup 10: System Status Focus (No Selection)
**Data**: System health, connectivity, and diagnostics
**Use Case**: Troubleshooting and system administration

```
┌─ Supsrc System Status ──────────────────────────────────────────────────────────┐
│ SYSTEM HEALTH                          │ CONNECTIVITY STATUS                    │
│ ┌─ CORE SERVICES ────────────────────┐ │ ┌─ GIT REMOTES ──────────────────────┐ │
│ │ 🟢 File Monitor: Running           │ │ │ 🟢 github.com: 1.2s (Excellent)   │ │
│ │ 🟢 Event Queue: 0 pending          │ │ │ 🟢 gitlab.com: 2.1s (Good)        │ │
│ │ 🟢 Git Engine: Operational         │ │ │ 🟡 bitbucket.org: 4.3s (Slow)     │ │
│ │ 🟢 Rule Engine: Active             │ │ │ 🔴 custom.git: Timeout             │ │
│ │ 🟢 State Manager: Synchronized     │ │ └────────────────────────────────────┘ │
│ └────────────────────────────────────┘ │ ┌─ AUTHENTICATION ───────────────────┐ │
│ ┌─ RESOURCE USAGE ───────────────────┐ │ │ 🟢 SSH Agent: 3 keys loaded        │ │
│ │ CPU: ▁▂▃▁▂ 2.1% (Normal)           │ │ │ 🟢 Git Config: Valid                │ │
│ │ Memory: ▁▃▅▃▂ 45MB (Normal)        │ │ │ 🟡 Token: Expires in 23d           │ │
│ │ Disk I/O: ▁▁▃▁▁ 12KB/s (Low)       │ │ │ 🔴 game-engine: Auth failed         │ │
│ │ Network: ▁▂▁▁▂ 0.8KB/s (Low)       │ │ └────────────────────────────────────┘ │
│ └────────────────────────────────────┘ │                                        │
├─────────────────────────────────────────┴────────────────────────────────────────┤
│ RECENT SYSTEM EVENTS                                                             │
│ 🕐 12:35:42 INFO: Monitoring service started successfully                       │
│ 🕐 12:35:40 INFO: Loaded configuration from supsrc.conf                        │
│ 🕐 12:35:38 WARN: Slow network response from bitbucket.org (4.3s)              │
│ 🕐 12:34:55 ERROR: Authentication failed for game-engine remote                 │
│ 🕐 12:30:15 INFO: System startup completed in 2.3s                             │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Mockup 11: Split View - Basic Selection (Repository Selected)
**Data**: Repository list + basic selected repo details
**Use Case**: Standard detail view for selected repository

```
┌─ Supsrc Watcher ──────────────┬─ 🏠 my-project Details ───────────────────────────┐
│ 🏠 my-project    ✅ IDLE      │ STATUS: ✅ IDLE                                    │
│ 🔬 experiments   🔄 CHANGED   │ RULE: ⏱️ 5 minute inactivity                      │
│ 📚 docs-site     ⚙️ STAGING   │ BRANCH: 📝 main                                   │
│ 🎮 game-engine   ❌ ERROR     │ LAST CHANGE: ⏱️ 2 minutes ago                     │
│ 📱 mobile-app    ✅ IDLE      │ SAVE COUNT: 💾 3                                  │
│                               │                                                   │
├───────────────────────────────┤ RECENT COMMITS:                                   │
│ GLOBAL ACTIVITY               │ • 2m ago: feat: implement user authentication    │
│ 🔄 Active: 2 repos            │ • 15m ago: fix: resolve login validation bug     │
│ 📊 Commits: 47 today          │ • 1h ago: docs: update README with new features  │
│ ⚡ Avg cycle: 3.2min          │ • 2h ago: refactor: clean up authentication code │
│ 🚨 Errors: 1                  │                                                   │
│                               │ CURRENT FILES:                                    │
│ [Pause All] [Resume All]      │ • Modified: src/auth/login.py (+23 -5)           │
│                               │ • Modified: tests/auth_test.py (+45 -12)         │
│                               │ • Added: docs/auth_guide.md                       │
│                               │                                                   │
│                               │ [Force Commit] [Reset State] [Configure]         │
└───────────────────────────────┴───────────────────────────────────────────────────┘
```

## Mockup 12: Split View - Detailed Selection (Repository Selected)
**Data**: Repository list + comprehensive repo analysis
**Use Case**: Power users wanting full repository insights

```
┌─ Repositories ────────────────┬─ 🔬 experiments - Detailed Analysis ──────────────┐
│ 🏠 my-project    ✅           │ ┌─ STATUS ──────────┬─ CONFIGURATION ─────────────┐ │
│ ❱🔬 experiments  🔄           │ │ State: 🔄 CHANGED │ Rule: 💾 10 saves           │ │
│ 📚 docs-site     ⚙️           │ │ Files: 12 tracked │ Auto-push: ✅ Enabled       │ │
│ 🎮 game-engine   ❌           │ │ Branch: feature   │ Remote: origin              │ │
│ 📱 mobile-app    ✅           │ │ Clean: ❌ No     │ Message: {{timestamp}}      │ │
│                               │ └───────────────────┴─────────────────────────────┘ │
├───────────────────────────────┤ ┌─ RECENT CHANGES ─────────────────────────────────┐ │
│ QUICK ACTIONS                 │ │ 📝 5s ago: src/neural_net.py (+15 -3)           │ │
│ [⏸️ Pause Selected]           │ │ 📝 2m ago: data/training.json (+234 -0)         │ │
│ [🔄 Force Sync]               │ │ 📝 5m ago: config/model.yaml (+5 -2)            │ │
│ [⚙️ Configure]                │ │ 📝 8m ago: README.md (+12 -1)                   │ │
│ [🗑️ Reset]                    │ └─────────────────────────────────────────────────┘ │
│                               │ ┌─ COMMIT HISTORY ─────────────────────────────────┐ │
│ GLOBAL STATS                  │ │ 🕐 10m ago: [abc123] feat: improve accuracy      │ │
│ Total repos: 5                │ │ 🕐 1h ago:  [def456] fix: memory leak in training│ │
│ Active: 2 🔄                  │ │ 🕐 3h ago:  [ghi789] data: add validation set    │ │
│ Errors: 1 ❌                  │ │ 🕐 1d ago:  [jkl012] init: neural network setup  │ │
│ Success rate: 94%             │ └─────────────────────────────────────────────────┘ │
└───────────────────────────────┴───────────────────────────────────────────────────┘
```

## Mockup 13: Split View - File Explorer Style (Repository Selected)
**Data**: Repository list + file tree view of selected repo
**Use Case**: File-focused workflow with directory navigation

```
┌─ Repositories ────────────────┬─ 📚 docs-site File Explorer ──────────────────────┐
│ 🏠 my-project    ✅           │ 📁 docs-site/                                      │
│ 🔬 experiments   🔄           │ ├─ 📁 content/                   [3 modified]      │
│ ❱📚 docs-site    ⚙️           │ │  ├─ 📄 tutorial.md             [modified] ●     │
│ 🎮 game-engine   ❌           │ │  ├─ 📄 getting-started.md      [clean]           │
│ 📱 mobile-app    ✅           │ │  └─ 📄 api-reference.md        [modified] ●     │
│                               │ ├─ 📁 static/                   [1 modified]      │
│                               │ │  ├─ 📁 css/                                     │
│                               │ │  │  └─ 📄 styles.css          [modified] ●     │
│                               │ │  └─ 📁 images/                                  │
│                               │ ├─ 📄 config.yaml               [clean]           │
│                               │ ├─ 📄 README.md                 [clean]           │
│                               │ └─ 📄 .gitignore                [clean]           │
├───────────────────────────────┤                                                   │
│ FILE OPERATIONS               │ STAGING AREA:                                     │
│ Modified: 3 files             │ ✅ content/tutorial.md                            │
│ Added: 0 files                │ ✅ content/api-reference.md                       │
│ Deleted: 0 files              │ ⏳ static/css/styles.css (staging...)             │
│ Untracked: 0 files            │                                                   │
│                               │ COMMIT MESSAGE:                                   │
│ [Stage All] [Unstage All]     │ ┌─────────────────────────────────────────────────┐ │
│ [Commit Now] [Reset]          │ │ docs: update tutorial and API reference        │ │
│                               │ └─────────────────────────────────────────────────┘ │
└───────────────────────────────┴───────────────────────────────────────────────────┘
```

## Mockup 14: Split View - Timeline/Activity (Repository Selected)
**Data**: Repository list + chronological activity view
**Use Case**: Tracking development timeline and activity patterns

```
┌─ Repositories ────────────────┬─ 🏠 my-project Activity Timeline ─────────────────┐
│ ❱🏠 my-project   ✅           │                                                   │
│ 🔬 experiments   🔄           │ TODAY ─── 📅 March 15, 2024 ──────────────────── │
│ 📚 docs-site     ⚙️           │                                                   │
│ 🎮 game-engine   ❌           │ ⏰ 12:35 🟢 PUSHED     Successfully pushed to main │
│ 📱 mobile-app    ✅           │   │                    ↳ 3 files, +47 -12 lines   │
│                               │ ⏰ 12:33 🔵 COMMITTED  feat: user authentication  │
│                               │   │                    ↳ commit: abc123def        │
│                               │ ⏰ 12:30 🟡 STAGED     Added modified files       │
│                               │   │                    ↳ auth/login.py, tests/   │
│                               │ ⏰ 12:28 🔄 CHANGED    File modifications         │
│                               │   │                    ↳ Auto-save detected       │
│                               │                                                   │
│                               │ ⏰ 11:45 🟢 PUSHED     Hotfix release             │
│                               │   │                    ↳ 1 file, +5 -2 lines     │
│                               │ ⏰ 11:42 🔵 COMMITTED  fix: critical login bug    │
│                               │                                                   │
├───────────────────────────────┤ YESTERDAY ─── 📅 March 14, 2024 ─────────────── │
│ TIMELINE CONTROLS             │                                                   │
│ View: [Today] [Week] [Month]  │ ⏰ 16:20 🟢 PUSHED     Feature branch merge       │
│ Filter: [All] [Commits] [Push]│ ⏰ 16:18 🔵 COMMITTED  feat: dashboard widgets   │
│ Auto-refresh: [ON] [OFF]      │ ⏰ 14:35 🔵 COMMITTED  refactor: clean up code   │
│                               │ ⏰ 09:15 🔄 CHANGED    Morning development start  │
│ [Export Timeline] [Archive]   │                                                   │
└───────────────────────────────┴───────────────────────────────────────────────────┘
```

## Mockup 15: Split View - Error/Diagnostic Focus (Repository Selected)
**Data**: Repository list + error analysis and diagnostics
**Use Case**: Troubleshooting repository issues and errors

```
┌─ Repositories ────────────────┬─ 🎮 game-engine Error Analysis ───────────────────┐
│ 🏠 my-project    ✅           │ ❌ CURRENT ERROR: Authentication Failed             │
│ 🔬 experiments   🔄           │                                                   │
│ 📚 docs-site     ⚙️           │ ┌─ ERROR DETAILS ─────────────────────────────────┐ │
│ ❱🎮 game-engine  ❌           │ │ 🕐 Time: 2024-03-15 11:34:55 UTC               │ │
│ 📱 mobile-app    ✅           │ │ 🔍 Type: GitAuthenticationError                 │ │
│                               │ │ 📍 Stage: PUSH operation                        │ │
│                               │ │ 🌐 Remote: git@github.com:user/game-engine.git │ │
│                               │ │ 📝 Message: Permission denied (publickey)      │ │
│                               │ └─────────────────────────────────────────────────┘ │
│                               │                                                   │
├───────────────────────────────┤ ┌─ DIAGNOSTIC CHECKS ─────────────────────────────┐ │
│ ERROR SUMMARY                 │ │ 🔑 SSH Key: ❌ Not found in SSH agent          │ │
│ Total errors: 3               │ │ 🌐 Network: ✅ GitHub reachable                │ │
│ Active: 1 🚨                  │ │ 📋 Git Config: ✅ User configured               │ │
│ Resolved: 2 ✅                │ │ 🔐 Permissions: ❌ Key not authorized           │ │
│                               │ │ 📁 Local Repo: ✅ Git repository valid         │ │
│ RECENT PATTERNS               │ └─────────────────────────────────────────────────┘ │
│ Auth failures: 3 today        │                                                   │
│ Network timeouts: 0           │ ┌─ SUGGESTED ACTIONS ─────────────────────────────┐ │
│ Config errors: 1 this week    │ │ 🔧 [Add SSH key to agent]                      │ │
│                               │ │ 🔑 [Generate new SSH key]                      │ │
│ [View Error Log] [Clear]      │ │ 🌐 [Test connection to remote]                 │ │
│                               │ │ ⚙️ [Open repository settings]                  │ │
│                               │ │ 🚫 [Disable auto-push for this repo]           │ │
│                               │ └─────────────────────────────────────────────────┘ │
└───────────────────────────────┴───────────────────────────────────────────────────┘
```

## Mockup 16: Activity Stream Focus - Live Feed (No Selection)
**Data**: Real-time activity with detailed event information
**Use Case**: Monitoring live development activity in detail

```
┌─ Supsrc Live Activity Feed ─────────────────────────────────────────────────────┐
│ 🔴 LIVE │ Auto-scroll: ON │ Buffer: 1000 │ Filter: All ▼ │ Sound: 🔕 │ 12:35:42│
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│ 🔄 12:35:42.234 🔬 experiments → CHANGED                                        │
│    ├─ Event: File modified                                                      │
│    ├─ Path: src/neural_net.py                                                   │
│    ├─ Size: +1,247 bytes                                                        │
│    └─ Trigger: Save count rule (1/10 saves)                                    │
│                                                                                  │
│ ⚙️ 12:35:38.891 📚 docs-site → STAGING                                          │
│    ├─ Event: Auto-staging triggered                                             │
│    ├─ Files: 3 (tutorial.md, api-ref.md, styles.css)                          │
│    ├─ Changes: +89 -23 lines                                                    │
│    └─ Trigger: Inactivity rule (2 minutes)                                     │
│                                                                                  │
│ 🔄 12:35:35.567 📚 docs-site → CHANGED                                          │
│    ├─ Event: File modified                                                      │
│    ├─ Path: content/tutorial.md                                                 │
│    ├─ Size: +892 bytes                                                          │
│    └─ Trigger: Save count rule (7/10 saves)                                    │
│                                                                                  │
│ ✅ 12:35:30.123 🏠 my-project → PUSHED                                          │
│    ├─ Event: Push completed successfully                                        │
│    ├─ Remote: origin/main                                                       │
│    ├─ Commit: abc123def "feat: implement user auth"                            │
│    └─ Duration: 2.3 seconds                                                     │
│                                                                                  │
│ [⏸️ Pause] [🔍 Search] [📊 Stats] [💾 Export] [⚙️ Filters] [🗑️ Clear]          │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Mockup 17: Activity Stream - Grouped by Repository (No Selection)
**Data**: Activity organized by repository with expandable sections
**Use Case**: Understanding per-repository activity patterns

```
┌─ Supsrc Repository Activity Groups ─────────────────────────────────────────────┐
│ Group by: [Repository ▼] │ Time: [Last 1 hour ▼] │ Status: [All ▼] │ 12:35:42 │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│ ▼ 🏠 my-project (4 events, last: 2m ago) ──────────────────────────────────────│
│   ✅ 12:35:30 PUSHED      Successfully pushed to origin/main (2.3s)           │
│   💾 12:35:28 COMMITTED   feat: implement user authentication [abc123d]       │
│   ⚙️ 12:35:25 STAGED      3 files staged for commit                            │
│   🔄 12:35:22 CHANGED     auth/login.py, auth/session.py modified              │
│                                                                                  │
│ ▼ 📚 docs-site (6 events, last: 5s ago) ───────────────────────────────────────│
│   ⚙️ 12:35:38 STAGING     Auto-staging triggered (inactivity: 2m)             │
│   🔄 12:35:35 CHANGED     content/tutorial.md modified (+892 bytes)           │
│   🔄 12:35:15 CHANGED     content/api-reference.md modified (+234 bytes)      │
│   🔄 12:34:58 CHANGED     static/css/styles.css modified (+156 bytes)         │
│   💾 12:32:45 COMMITTED   docs: update getting started guide [def456a]        │
│   ✅ 12:32:42 PUSHED      Successfully pushed to origin/main (1.8s)           │
│                                                                                  │
│ ▶ 🔬 experiments (2 events, last: 42s ago) ────────────────────────────────────│
│                                                                                  │
│ ▶ 🎮 game-engine (1 event, last: 1h ago) ──────────────────────────────────────│
│                                                                                  │
│ ▶ 📱 mobile-app (0 events in timeframe) ───────────────────────────────────────│
│                                                                                  │
│ [Expand All] [Collapse All] [Export Selected] [Mark as Read]                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Mockup 18: Activity Stream - Timeline View (No Selection)
**Data**: Chronological timeline with visual time indicators
**Use Case**: Understanding temporal patterns and sequences

```
┌─ Supsrc Timeline View ──────────────────────────────────────────────────────────┐
│ ⏰ Timeline: [Last Hour ▼] │ Zoom: [1min ▼] │ Now: 12:35:42 │ [⏪] [⏸️] [⏩] │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│ 12:35 ┤                                                                          │
│       │ 🔄 :42 🔬 experiments    File: neural_net.py modified                   │
│       │ ⚙️ :38 📚 docs-site       Staging triggered (inactivity)                │
│       │ 🔄 :35 📚 docs-site       File: tutorial.md modified                    │
│       │ ✅ :30 🏠 my-project      Pushed to origin/main                         │
│       │ 💾 :28 🏠 my-project      Committed: feat: user auth                    │
│       │ ⚙️ :25 🏠 my-project      Staging files                                 │
│       │ 🔄 :22 🏠 my-project      Files changed: auth/*.py                      │
│       │                                                                          │
│ 12:34 ┤                                                                          │
│       │ ❌ :55 🎮 game-engine     Push failed: authentication                   │
│       │ 🔄 :45 📱 mobile-app      Status: all changes committed                 │
│       │                                                                          │
│ 12:33 ┤                                                                          │
│       │ 💾 :12 🔬 experiments     Committed: improve model accuracy              │
│       │ ⚙️ :08 🔬 experiments     Staging modifications                          │
│       │ 🔄 :05 🔬 experiments     Multiple files changed                        │
│       │                                                                          │
│ 12:32 ┤                                                                          │
│       │ ✅ :45 📚 docs-site       Pushed documentation updates                  │
│       │ 💾 :42 📚 docs-site       Committed: update guides                      │
│       │                                                                          │
│ [🔍 Search Timeline] [📊 Activity Pattern] [💾 Export] [⚙️ Settings]           │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Mockup 19: Focused Log Viewer (No Selection)
**Data**: Detailed log messages with filtering and search
**Use Case**: Debugging and detailed monitoring

```
┌─ Supsrc Log Viewer ─────────────────────────────────────────────────────────────┐
│ Level: [DEBUG ▼] │ Component: [All ▼] │ Repo: [All ▼] │ Search: [________] 🔍  │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 🔍 LOG MESSAGES                                                                  │
│                                                                                  │
│ 🐛 12:35:42.234 [git.push     ] my-project     Remote callback: using SSH key  │
│ ℹ️ 12:35:42.156 [orchestrator ] my-project     Push operation started          │
│ 🐛 12:35:42.089 [git.commit   ] my-project     Created commit object abc123def │
│ ℹ️ 12:35:42.023 [orchestrator ] my-project     Commit operation started        │
│ 🐛 12:35:41.967 [git.stage    ] my-project     Staged file: auth/login.py      │
│ 🐛 12:35:41.934 [git.stage    ] my-project     Staged file: auth/session.py    │
│ ℹ️ 12:35:41.890 [orchestrator ] my-project     Stage operation started         │
│ 🐛 12:35:41.834 [rules        ] my-project     Inactivity rule triggered (5m)  │
│ 🐛 12:35:41.790 [monitor      ] my-project     Timer callback executed         │
│ ⚠️ 12:34:55.123 [git.push     ] game-engine    Authentication failed: no key   │
│ ❌ 12:34:55.089 [git.push     ] game-engine    Push operation failed           │
│ 🐛 12:34:55.045 [git.push     ] game-engine    Attempting push to origin       │
│ ℹ️ 12:34:55.012 [orchestrator ] game-engine    Push operation started          │
│ 🐛 12:34:54.978 [git.commit   ] game-engine    Created commit object def456ab │
│ ℹ️ 12:34:54.934 [orchestrator ] game-engine    Commit operation started        │
│ 🐛 12:34:54.890 [rules        ] game-engine    Manual rule triggered           │
│ 🐛 12:34:12.234 [monitor      ] experiments    File change: neural_net.py      │
│ ℹ️ 12:34:12.189 [monitor      ] experiments    Event received: FILE_MODIFIED   │
│                                                                                  │
│ [⏸️ Pause] [🗑️ Clear] [💾 Export] [⚙️ Configure Levels] [📋 Copy Selected]     │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Mockup 20: Hybrid Dashboard with Mini-Log (No Selection)
**Data**: Combined dashboard view with integrated activity stream
**Use Case**: Balanced view of status, metrics, and recent activity

```
┌─ Supsrc Hybrid Dashboard ───────────────────────────────────────────────────────┐
│ ┌─ REPOSITORY STATUS ──────────────┐ ┌─ QUICK METRICS ────────────────────────┐ │
│ │ 🏠 my-project   ✅ IDLE  💾 3    │ │ 📊 Today: 23 commits │ ⚡ Active: 2/5  │ │
│ │ 🔬 experiments  🔄 CHNGD 💾 1    │ │ 🎯 Success: 94.2%    │ ❌ Errors: 1    │ │
│ │ 📚 docs-site    ⚙️ STAGE 💾 7    │ │ ⏱️ Avg cycle: 3.2m   │ 🌐 Network: OK  │ │
│ │ 🎮 game-engine  ❌ ERROR 💾 12   │ │ 💾 Saves/hr: 156     │ 📈 Trend: ↗️    │ │
│ │ 📱 mobile-app   ✅ IDLE  💾 0    │ └────────────────────────────────────────┘ │
│ └──────────────────────────────────┘                                           │
├──────────────────────────────────────────────────────────────────────────────────┤
│ ⚡ LIVE ACTIVITY STREAM                                                          │
│ 🔄 12:35:42 🔬 experiments → File changed: neural_net.py (+15 -3)              │
│ ⚙️ 12:35:38 📚 docs-site → Auto-staging 3 files (inactivity trigger)           │
│ ✅ 12:35:30 🏠 my-project → Successfully pushed to origin/main (2.3s)          │
│ ❌ 12:34:55 🎮 game-engine → Push failed: authentication required               │
│ 💾 12:34:45 📱 mobile-app → Committed: v2.1.0 release preparation               │
│                                                                                  │
│ ┌─ ALERTS ─────────────────────────┐ ┌─ PERFORMANCE ─────────────────────────┐ │
│ │ 🚨 game-engine: Auth failure     │ │ CPU: ▁▂▃ 2.1%    Memory: ▁▃▅ 45MB   │ │
│ │ ⚠️ bitbucket: Slow response (4s) │ │ I/O: ▁▁▃ Low      Network: ▁▂▁ Low   │ │
│ │ [Fix] [Ignore] [Configure]       │ │ Watchers: 23      Queue: 0 pending   │ │
│ └──────────────────────────────────┘ └───────────────────────────────────────┘ │
│                                                                                  │
│ [⚙️ Settings] [📊 Full Dashboard] [🔍 Search] [⏸️ Pause All] [❓ Help]          │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## Data/Functionality Groupings

### Same Data, Different Layouts:
- **Mockups 1-3**: Repository status overview with varying information density
- **Mockups 11-12**: Basic vs detailed repository selection views
- **Mockups 16-18**: Activity streams with different organization (live, grouped, timeline)

### Unique Data Focus Areas:
- **Status-focused** (1-5): Repository states and basic operations
- **Metrics-focused** (6, 9-10): Analytics, performance, and system health
- **Activity-focused** (7, 16-19): Real-time monitoring and event tracking
- **Control-focused** (8): Administrative and configuration interfaces
- **Detail-focused** (11-15): Deep-dive into individual repositories
- **Hybrid** (20): Balanced overview combining multiple data types

Each mockup represents different user personas and use cases, from quick monitoring to detailed analysis and troubleshooting.
