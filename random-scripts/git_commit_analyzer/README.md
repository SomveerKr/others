# Git Commit Analyzer 📊

A comprehensive Python tool that analyzes your Git commit history and provides detailed insights about your coding patterns, productivity, and commit quality.

## Features ✨

- **Commit Frequency Analysis**: Discover your most productive hours and days
- **Message Quality Metrics**: Analyze commit message patterns and conventional commit usage
- **File Change Statistics**: Track additions, deletions, and most frequently changed files
- **Author Contributions**: View detailed statistics for all contributors
- **Productivity Score**: Get an overall productivity score based on multiple factors
- **JSON Export**: Export analysis data for further processing
- **Language Distribution**: See which file types you work with most

## Installation 🚀

No external dependencies required! This script uses only Python standard library modules.

```bash
# Clone or download the script
git clone <your-repo-url>
cd random-scripts

# Make it executable (Linux/Mac)
chmod +x git_commit_analyzer.py
```

## Usage 💻

### Basic Usage

Analyze the current repository for the last 30 days:
```bash
python git_commit_analyzer.py
```

### Advanced Options

```bash
# Analyze a specific repository
python git_commit_analyzer.py --repo-path /path/to/your/repo

# Analyze last 90 days
python git_commit_analyzer.py --days 90

# Filter by specific author
python git_commit_analyzer.py --author "John Doe"

# Export results to JSON
python git_commit_analyzer.py --export analysis.json

# Combine options
python git_commit_analyzer.py --repo-path ~/projects/myapp --days 60 --author "Jane" --export report.json
```

## Sample Output 📈

```
╔══════════════════════════════════════════════════════════════╗
║           GIT COMMIT ANALYSIS REPORT                         ║
╚══════════════════════════════════════════════════════════════╝

📊 OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Repository: /home/user/projects/myapp
  Analysis Period: Last 30 days
  Total Commits: 45
  Productivity Score: 72.5/100

👤 AUTHOR STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Authors: 3
  • John Doe: 25 commits (+1250 -340)
  • Jane Smith: 15 commits (+890 -210)
  • Bob Johnson: 5 commits (+120 -45)

⏰ COMMIT PATTERNS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Most Productive Hour: 14:00 (12 commits)
  Most Productive Day: Wednesday (15 commits)

📝 COMMIT MESSAGE QUALITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Average Message Length: 52.3 characters
  Conventional Commits: 32/45 (71.1%)
  
  Commit Type Breakdown:
    feat: 15
    fix: 10
    refactor: 5
    docs: 2
```

## What It Analyzes 🔍

### Commit Patterns
- Commits by hour of day (find your peak productivity time)
- Commits by day of week
- Commit frequency over time

### Message Quality
- Average commit message length
- Conventional commit format compliance
- Breakdown by commit type (feat, fix, docs, etc.)

### Code Changes
- Total lines added and deleted
- Net change in codebase
- Average changes per commit
- Most frequently changed files
- File type distribution

### Team Insights
- Number of contributors
- Commits per author
- Lines changed per author

### Productivity Metrics
- Overall productivity score (0-100)
- Based on commit frequency, message quality, and code changes

## Use Cases 💡

1. **Personal Productivity Tracking**: Understand when you're most productive
2. **Team Reviews**: Analyze team contribution patterns
3. **Code Quality Metrics**: Track commit message quality over time
4. **Project Health**: Monitor codebase activity and changes
5. **Time Management**: Identify your peak coding hours
6. **Portfolio Building**: Generate statistics for your resume or portfolio

## Requirements 📋

- Python 3.6 or higher
- Git installed and accessible from command line
- A Git repository to analyze

## Tips 💭

- Use `--days 365` to get a full year overview
- Export to JSON for creating custom visualizations
- Run regularly to track productivity trends
- Use with CI/CD to monitor team metrics
- Combine with other tools for comprehensive project analytics

## Contributing 🤝

Feel free to fork, modify, and submit pull requests. Some ideas for enhancements:
- Add graphical charts using matplotlib
- Create HTML report output
- Add more commit message pattern analysis
- Include branch analysis
- Add comparison between time periods

## License 📄

Free to use and modify for personal and commercial projects.

---

**Happy Analyzing! 🎉**
