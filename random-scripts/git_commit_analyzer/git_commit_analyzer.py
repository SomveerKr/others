#!/usr/bin/env python3
"""
Git Commit Analyzer
===================
A comprehensive tool to analyze your Git commit history and provide insights about:
- Commit patterns and frequency
- Most productive hours/days
- Commit message quality
- File change statistics
- Author contributions
- Language/file type distribution

Usage:
    python git_commit_analyzer.py [--repo-path PATH] [--days DAYS] [--author AUTHOR]
"""

import subprocess
import re
import json
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from pathlib import Path
import argparse
import sys


class GitCommitAnalyzer:
    def __init__(self, repo_path='.', days=30, author=None):
        self.repo_path = Path(repo_path)
        self.days = days
        self.author = author
        self.commits = []
        
    def run_git_command(self, command):
        """Execute a git command and return the output."""
        try:
            result = subprocess.run(
                command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error running git command: {e}")
            return ""
    
    def fetch_commits(self):
        """Fetch commit data from the repository."""
        since_date = (datetime.now() - timedelta(days=self.days)).strftime('%Y-%m-%d')
        
        # Format: hash|author|date|message
        cmd = [
            'git', 'log',
            f'--since={since_date}',
            '--pretty=format:%H|%an|%ai|%s',
            '--numstat'
        ]
        
        if self.author:
            cmd.append(f'--author={self.author}')
        
        output = self.run_git_command(cmd)
        
        current_commit = None
        for line in output.split('\n'):
            if '|' in line and len(line.split('|')) == 4:
                # New commit
                if current_commit:
                    self.commits.append(current_commit)
                
                hash_val, author, date, message = line.split('|')
                current_commit = {
                    'hash': hash_val,
                    'author': author,
                    'date': datetime.fromisoformat(date.replace(' +', '+')),
                    'message': message,
                    'files': [],
                    'additions': 0,
                    'deletions': 0
                }
            elif line.strip() and current_commit:
                # File change stats
                parts = line.split('\t')
                if len(parts) == 3:
                    additions, deletions, filename = parts
                    try:
                        add = int(additions) if additions != '-' else 0
                        delete = int(deletions) if deletions != '-' else 0
                        current_commit['additions'] += add
                        current_commit['deletions'] += delete
                        current_commit['files'].append({
                            'name': filename,
                            'additions': add,
                            'deletions': delete
                        })
                    except ValueError:
                        pass
        
        if current_commit:
            self.commits.append(current_commit)
    
    def analyze_commit_frequency(self):
        """Analyze commit frequency by hour and day of week."""
        hours = defaultdict(int)
        days = defaultdict(int)
        dates = defaultdict(int)
        
        for commit in self.commits:
            hour = commit['date'].hour
            day = commit['date'].strftime('%A')
            date = commit['date'].strftime('%Y-%m-%d')
            
            hours[hour] += 1
            days[day] += 1
            dates[date] += 1
        
        return {
            'by_hour': dict(sorted(hours.items())),
            'by_day': dict(days),
            'by_date': dict(sorted(dates.items()))
        }
    
    def analyze_commit_messages(self):
        """Analyze commit message quality and patterns."""
        message_lengths = []
        conventional_commits = 0
        patterns = {
            'feat': 0, 'fix': 0, 'docs': 0, 'style': 0,
            'refactor': 0, 'test': 0, 'chore': 0
        }
        
        for commit in self.commits:
            msg = commit['message']
            message_lengths.append(len(msg))
            
            # Check for conventional commits
            match = re.match(r'^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?:', msg)
            if match:
                conventional_commits += 1
                commit_type = match.group(1)
                patterns[commit_type] += 1
        
        return {
            'total_commits': len(self.commits),
            'avg_message_length': sum(message_lengths) / len(message_lengths) if message_lengths else 0,
            'conventional_commits': conventional_commits,
            'conventional_percentage': (conventional_commits / len(self.commits) * 100) if self.commits else 0,
            'commit_types': patterns
        }
    
    def analyze_file_changes(self):
        """Analyze file change statistics."""
        total_additions = 0
        total_deletions = 0
        file_extensions = Counter()
        most_changed_files = Counter()
        
        for commit in self.commits:
            total_additions += commit['additions']
            total_deletions += commit['deletions']
            
            for file in commit['files']:
                filename = file['name']
                most_changed_files[filename] += 1
                
                # Extract file extension
                ext = Path(filename).suffix
                if ext:
                    file_extensions[ext] += 1
        
        return {
            'total_additions': total_additions,
            'total_deletions': total_deletions,
            'net_lines': total_additions - total_deletions,
            'avg_additions_per_commit': total_additions / len(self.commits) if self.commits else 0,
            'avg_deletions_per_commit': total_deletions / len(self.commits) if self.commits else 0,
            'file_extensions': dict(file_extensions.most_common(10)),
            'most_changed_files': dict(most_changed_files.most_common(10))
        }
    
    def analyze_authors(self):
        """Analyze author contributions."""
        authors = Counter()
        author_stats = defaultdict(lambda: {'commits': 0, 'additions': 0, 'deletions': 0})
        
        for commit in self.commits:
            author = commit['author']
            authors[author] += 1
            author_stats[author]['commits'] += 1
            author_stats[author]['additions'] += commit['additions']
            author_stats[author]['deletions'] += commit['deletions']
        
        return {
            'total_authors': len(authors),
            'author_commits': dict(authors.most_common()),
            'author_stats': dict(author_stats)
        }
    
    def get_productivity_score(self):
        """Calculate a productivity score based on various metrics."""
        if not self.commits:
            return 0
        
        # Factors: commit frequency, message quality, code changes
        commit_score = min(len(self.commits) / self.days * 10, 40)  # Max 40 points
        
        msg_analysis = self.analyze_commit_messages()
        message_score = msg_analysis['conventional_percentage'] * 0.3  # Max 30 points
        
        file_analysis = self.analyze_file_changes()
        change_score = min(file_analysis['avg_additions_per_commit'] / 10, 30)  # Max 30 points
        
        return round(commit_score + message_score + change_score, 2)
    
    def generate_report(self):
        """Generate a comprehensive analysis report."""
        if not self.commits:
            return "No commits found in the specified time range."
        
        frequency = self.analyze_commit_frequency()
        messages = self.analyze_commit_messages()
        files = self.analyze_file_changes()
        authors = self.analyze_authors()
        productivity = self.get_productivity_score()
        
        # Find most productive hour and day
        most_productive_hour = max(frequency['by_hour'].items(), key=lambda x: x[1])
        most_productive_day = max(frequency['by_day'].items(), key=lambda x: x[1])
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║           GIT COMMIT ANALYSIS REPORT                         ║
╚══════════════════════════════════════════════════════════════╝

📊 OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Repository: {self.repo_path.absolute()}
  Analysis Period: Last {self.days} days
  Total Commits: {messages['total_commits']}
  Productivity Score: {productivity}/100

👤 AUTHOR STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Authors: {authors['total_authors']}
"""
        
        for author, count in list(authors['author_commits'].items())[:5]:
            stats = authors['author_stats'][author]
            report += f"  • {author}: {count} commits (+{stats['additions']} -{stats['deletions']})\n"
        
        report += f"""
⏰ COMMIT PATTERNS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Most Productive Hour: {most_productive_hour[0]}:00 ({most_productive_hour[1]} commits)
  Most Productive Day: {most_productive_day[0]} ({most_productive_day[1]} commits)

📝 COMMIT MESSAGE QUALITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Average Message Length: {messages['avg_message_length']:.1f} characters
  Conventional Commits: {messages['conventional_commits']}/{messages['total_commits']} ({messages['conventional_percentage']:.1f}%)
  
  Commit Type Breakdown:
"""
        
        for commit_type, count in messages['commit_types'].items():
            if count > 0:
                report += f"    {commit_type}: {count}\n"
        
        report += f"""
📁 FILE CHANGES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Lines Added: {files['total_additions']:,}
  Total Lines Deleted: {files['total_deletions']:,}
  Net Change: {files['net_lines']:+,}
  Avg Changes per Commit: +{files['avg_additions_per_commit']:.1f} -{files['avg_deletions_per_commit']:.1f}

  Top File Types:
"""
        
        for ext, count in list(files['file_extensions'].items())[:5]:
            report += f"    {ext or '(no extension)'}: {count} files\n"
        
        report += f"""
  Most Changed Files:
"""
        
        for filename, count in list(files['most_changed_files'].items())[:5]:
            report += f"    {filename}: {count} changes\n"
        
        report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        return report
    
    def export_json(self, output_file):
        """Export analysis data to JSON file."""
        data = {
            'metadata': {
                'repo_path': str(self.repo_path.absolute()),
                'analysis_date': datetime.now().isoformat(),
                'days_analyzed': self.days,
                'author_filter': self.author
            },
            'frequency': self.analyze_commit_frequency(),
            'messages': self.analyze_commit_messages(),
            'files': self.analyze_file_changes(),
            'authors': self.analyze_authors(),
            'productivity_score': self.get_productivity_score()
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Analysis exported to {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze Git commit history and generate insights',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze current repository for last 30 days
  python git_commit_analyzer.py
  
  # Analyze specific repository for last 90 days
  python git_commit_analyzer.py --repo-path /path/to/repo --days 90
  
  # Analyze commits by specific author
  python git_commit_analyzer.py --author "John Doe"
  
  # Export results to JSON
  python git_commit_analyzer.py --export analysis.json
        """
    )
    
    parser.add_argument(
        '--repo-path',
        default='.',
        help='Path to the Git repository (default: current directory)'
    )
    
    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Number of days to analyze (default: 30)'
    )
    
    parser.add_argument(
        '--author',
        help='Filter commits by author name'
    )
    
    parser.add_argument(
        '--export',
        help='Export analysis to JSON file'
    )
    
    args = parser.parse_args()
    
    # Check if the path is a git repository
    repo_path = Path(args.repo_path)
    if not (repo_path / '.git').exists():
        print(f"❌ Error: {repo_path} is not a Git repository")
        sys.exit(1)
    
    print(f"🔍 Analyzing Git repository at {repo_path.absolute()}...")
    print(f"📅 Looking at the last {args.days} days...")
    
    analyzer = GitCommitAnalyzer(
        repo_path=args.repo_path,
        days=args.days,
        author=args.author
    )
    
    analyzer.fetch_commits()
    
    # Generate and print report
    report = analyzer.generate_report()
    print(report)
    
    # Export to JSON if requested
    if args.export:
        analyzer.export_json(args.export)


if __name__ == '__main__':
    main()
